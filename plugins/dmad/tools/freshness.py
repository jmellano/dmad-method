#!/usr/bin/env python3
"""Détecte ce qui a péri dans un run, et le propage vers le haut.

Sans cette passe, DMAD produit une photo qui jaunit. Avec elle, une
documentation vivante.

**Ce que la v0.4 ajoute est la propagation.** Une claim périmée périme les
documents qui la publient, et un document périmé périme ceux qui en dérivent :

    claim → STD → SFD → SFG

Sans elle, une SFG peut rester marquée fraîche alors que son socle a bougé.
C'est le pire cas possible : **le document le plus cru est le plus périmé**, et
son lecteur est celui qui a le moins de moyens de s'en apercevoir.

    python3 tools/freshness.py <dossier-run> [--against <dépôt-analysé>]
                                             [--versions <fichier>] [--strict]
"""
import argparse
import pathlib
import subprocess
import sys

try:
    import yaml
except ImportError:  # pragma: no cover
    sys.exit("dépendance manquante : pip install pyyaml")

# Du plus sain au plus atteint. La distinction shifted / stale évite le bruit :
# des lignes qui ont bougé sans changer de sens ne valent pas une re-soumission.
ORDRE = ["fresh", "shifted", "stale", "broken"]
PIRE = {s: i for i, s in enumerate(ORDRE)}

SOURCES = ("preuves/claims", "preuves/contrats", "preuves/business-objects")


def charger(dossier):
    out = []
    for path in sorted(list(dossier.glob("*.y*ml")) + list(dossier.glob("*.md"))):
        txt = path.read_text(encoding="utf-8")
        if path.suffix == ".md":
            if not txt.startswith("---"):
                continue
            fin = txt.find("\n---", 3)
            txt = txt[3:fin] if fin != -1 else ""
        try:
            doc = yaml.safe_load(txt) or {}
        except yaml.YAMLError as e:
            print(f"  ⚠ {path} illisible : {e}")
            continue
        if isinstance(doc, dict):
            out.append((path, doc))
    return out


def statut_git(repo, ref, commit_verifie):
    """Compare une référence fichier#Ldébut-Lfin à l'état actuel du dépôt.

    Rend None quand la vérification est impossible — on ne devine pas.
    """
    if "#" not in ref:
        return None
    fichier, _, plage = ref.partition("#")
    chemin = repo / fichier
    if not chemin.exists():
        return "broken"
    try:
        diff = subprocess.run(
            ["git", "-C", str(repo), "diff", "--name-only", commit_verifie, "--", fichier],
            capture_output=True, text=True, timeout=30,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    if diff.returncode != 0:
        return None
    if not diff.stdout.strip():
        return "fresh"
    # Le fichier a bougé. Distinguer un déplacement de lignes d'un changement de
    # sens demanderait de comparer le contenu cité ; à défaut, on ne tranche pas
    # à la baisse : on signale « shifted » et on laisse l'humain re-soumettre.
    return "shifted"


def check_versions(contrats, versions):
    """A14 — un contrat dont l'artefact a changé de version ment sans le dire."""
    alertes = []
    for path, c in contrats:
        artefact, declaree = c.get("artifact"), c.get("artifact_version")
        if not artefact or not declaree:
            continue
        resolue = versions.get(artefact)
        if resolue and resolue != declaree:
            alertes.append(
                f"{c['id']} — contrat lu en {artefact}:{declaree}, le build résout "
                f"{resolue}. Le code cité reste plausible et peut être faux : "
                "c'est l'anti-pattern A14"
            )
    return alertes


def propager(documents, statut_claim):
    """Le cœur de la v0.4 : la péremption remonte la cascade."""
    par_id = {d.get("id"): d for _, d in documents}
    statut_doc = {}

    for _, doc in documents:
        pire = "fresh"
        for cid in doc.get("claims_rendered") or []:
            s = statut_claim.get(cid, "fresh")
            if PIRE[s] > PIRE[pire]:
                pire = s
        statut_doc[doc["id"]] = pire

    # Point fixe : un document hérite du pire de ses parents.
    for _ in range(len(documents) + 1):
        change = False
        for _, doc in documents:
            for parent in doc.get("derives_from") or []:
                if parent in statut_doc and PIRE[statut_doc[parent]] > PIRE[statut_doc[doc["id"]]]:
                    statut_doc[doc["id"]] = statut_doc[parent]
                    change = True
        if not change:
            break
    return statut_doc, par_id


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("run", type=pathlib.Path)
    ap.add_argument("--against", type=pathlib.Path, help="dépôt analysé, pour comparer au code actuel")
    ap.add_argument("--versions", type=pathlib.Path, help="fichier YAML artefact: version résolu par le build")
    ap.add_argument("--strict", action="store_true", help="sortir en erreur si quelque chose a péri")
    args = ap.parse_args()

    statut_claim, sources = {}, []
    for proc in sorted((args.run / "processus").glob("*")) if (args.run / "processus").is_dir() else []:
        for dossier in SOURCES:
            if (proc / dossier).is_dir():
                sources += charger(proc / dossier)
    for socle in ("socle/capacites", "socle/metier", "socle/technique"):
        if (args.run / socle).is_dir():
            sources += charger(args.run / socle)

    commit_courant = None
    if args.against:
        r = subprocess.run(["git", "-C", str(args.against), "rev-parse", "HEAD"],
                           capture_output=True, text=True)
        commit_courant = r.stdout.strip() if r.returncode == 0 else None
        if commit_courant is None:
            print(f"⚠ {args.against} n'est pas un dépôt git lisible — "
                  "vérification limitée aux statuts déclarés\n")

    non_verifies = 0
    for _, art in sources:
        aid = art.get("id")
        fr = art.get("freshness") or {}
        declare = fr.get("status", "fresh")
        statut_claim[aid] = declare

        if not commit_courant:
            continue
        verifie_a = fr.get("verified_at_commit")
        if not verifie_a:
            non_verifies += 1
            continue
        if verifie_a == commit_courant:
            continue
        pire = declare
        for ev in art.get("evidence") or []:
            s = statut_git(args.against, ev.get("ref", ""), verifie_a)
            if s is None:
                non_verifies += 1
                continue
            if PIRE[s] > PIRE[pire]:
                pire = s
        statut_claim[aid] = pire

    # Le plan porte l'identité du document : plus de carte séparée à maintenir.
    documents = []
    for chemin in sorted(args.run.rglob("plan-*.y*ml")):
        try:
            plan = yaml.safe_load(chemin.read_text(encoding="utf-8")) or {}
        except yaml.YAMLError:
            continue
        if plan.get("id"):
            documents.append((str(chemin), plan))
    statut_doc, par_id = propager(documents, statut_claim)

    perimes = {k: v for k, v in statut_claim.items() if v != "fresh"}
    docs_perimes = {k: v for k, v in statut_doc.items() if v != "fresh"}

    print(f"Fraîcheur — {len(statut_claim)} artefact(s), {len(documents)} document(s)\n")

    if perimes:
        print("Artefacts périmés")
        for k, v in sorted(perimes.items()):
            print(f"  {v:<8} {k}")
        print()

    if documents:
        print("Documents, après propagation")
        for did, s in sorted(statut_doc.items()):
            marque = "  " if s == "fresh" else "⚠ "
            herite = ""
            if s != "fresh" and not any(
                statut_claim.get(c) == s for c in (par_id[did].get("claims_rendered") or [])
            ):
                herite = "  ← hérité de l'étage inférieur"
            print(f"  {marque}{s:<8} {did}{herite}")
        print()

    alertes = []
    if args.versions and args.versions.exists():
        versions = yaml.safe_load(args.versions.read_text(encoding="utf-8")) or {}
        contrats = charger(args.run / "contracts") if (args.run / "contracts").is_dir() else []
        alertes = check_versions(contrats, versions)
        if alertes:
            print("Contrats dont la version d'artefact a bougé")
            for a in alertes:
                print(f"  ⚠ {a}")
            print()

    if non_verifies:
        print(f"⚠ {non_verifies} preuve(s) n'ont pas pu être vérifiées contre le code. "
              "Ce n'est pas « fraîches » : c'est « non vérifiées », et ça se dit.\n")

    if not perimes and not docs_perimes and not alertes:
        print("✓ rien de périmé")
        return 0

    if args.strict:
        print("✗ le run porte des affirmations périmées")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
