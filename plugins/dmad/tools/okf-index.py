#!/usr/bin/env python3
"""Indexe le run et contrôle sa conformité OKF.

**Le run EST le bundle** (D27) : les agents écrivent des concepts, il n'y a plus
d'export à faire. Cet outil génère les `index.md` par répertoire et le journal,
puis contrôle ce que la spécification impose et ce que la production exige.

La règle dure d'OKF — tout concept porte un `type` non vide — est une exigence
de conformité. Les orphelins et les liens morts sont, eux, une exigence de
**production** : la spécification demande au consommateur de les tolérer. On les
refuse quand même, parce qu'un concept qu'aucun chemin n'atteint manque par
construction.

    python3 tools/okf-index.py <run> [--check]
"""
import argparse
import datetime as dt
import pathlib
import re
import sys

try:
    import yaml
except ImportError:  # pragma: no cover
    sys.exit("dépendance manquante : pip install pyyaml")

RESERVES = {"index.md", "log.md", "README.md"}
IGNORES = {"documents", "conduite"}


def frontmatter(chemin):
    t = chemin.read_text(encoding="utf-8")
    if not t.startswith("---"):
        return None
    fin = t.find("\n---", 3)
    if fin == -1:
        return None
    try:
        fm = yaml.safe_load(t[3:fin])
    except yaml.YAMLError:
        return None
    return fm if isinstance(fm, dict) else None


def concepts(run):
    for f in sorted(run.rglob("*.md")):
        rel = f.relative_to(run)
        # Une figure rendue est un intermédiaire du moteur de diagrammes, pas un
        # concept : elle est régénérée à chaque passe et n'a rien à indexer.
        if (f.name in RESERVES or rel.parts[0] in IGNORES
                or rel.parts[0].startswith(".") or f.name.endswith(".figure.txt")):
            continue
        yield f


TITRES = {"claims": "Affirmations", "contrats": "Contrats sortants",
          "business-objects": "Business objects", "challenges": "Réfutations",
          "questions": "Questions ouvertes", "capacites": "Capacités",
          "metier": "Socle métier", "technique": "Socle technique",
          "std": "Strate STD", "sfd": "Strate SFD", "sfg": "Strate SFG",
          "cas-usage": "Cas d'usage"}


RELATIONS = [("relates_to", "en relation avec"), ("open_questions", "question ouverte"),
             ("challenged_by", "réfuté par"), ("related_claims", "porte sur"),
             ("sub_objects", "compose"), ("claims_rendered", "publie")]


def relier(run):
    """Maintient le bloc de navigation de chaque concept.

    Un concept qu'aucun lien n'atteint manque par construction : c'est
    l'indexeur qui tient la navigation, pas le rédacteur.
    """
    import os
    par_id = {}
    for f in concepts(run):
        fm = frontmatter(f) or {}
        for cle in ("id", "dmad_id"):
            if fm.get(cle):
                par_id[str(fm[cle])] = f
    for f in concepts(run):
        fm = frontmatter(f) or {}
        cibles = []
        for cle, libelle in RELATIONS:
            for v in (fm.get(cle) or []):
                cibles.append((str(v), libelle))
        for feuille in (fm.get("own_leaves") or []):
            if isinstance(feuille, dict) and feuille.get("kind") == "contract":
                cibles.append((str(feuille.get("ref")), "appelle le contrat"))
        if fm.get("claim"):
            cibles.append((str(fm["claim"]), "attaque"))
        if fm.get("capability"):
            cibles.append((str(fm["capability"]), "relève de"))
        lignes = []
        for cible_id, libelle in cibles:
            cible = par_id.get(cible_id)
            if cible is None or cible == f:
                continue
            rel = os.path.relpath(cible, f.parent).replace("\\", "/")
            lignes.append(f"- {libelle} : [{cible_id}]({rel})")
        txt = re.split(r"^# Liens\s*$", f.read_text(encoding="utf-8"), maxsplit=1, flags=re.M)[0].rstrip()
        if lignes:
            txt += "\n\n# Liens\n\n" + "\n".join(dict.fromkeys(lignes))
        f.write_text(txt + "\n", encoding="utf-8")


def indexer(run):
    par_dossier = {}
    for f in concepts(run):
        par_dossier.setdefault(f.parent, []).append(f)
    # La racine déclare la version du format : c'est là et nulle part ailleurs
    # qu'un consommateur apprend à quelle révision d'OKF le bundle se conforme.
    sections = sorted({str(f.relative_to(run).parts[0]) for f in concepts(run)})
    (run / "index.md").write_text(
        '---\nokf_version: "0.2"\n---\n\n# Run DMAD\n\n'
        "La couche de preuve et les strates documentaires de ce run, en bundle Open\n"
        "Knowledge Format. Les documents composés vivent dans `documents/` et la conduite\n"
        "du run dans `conduite/` : ni l'une ni l'autre ne sont de la connaissance qu'un\n"
        "agent lit, et la garde d'OKF les laisse dehors.\n\n# Sections\n\n"
        + "\n".join(f"- [{TITRES.get(s, s)}]({s}/)" for s in sections) + "\n",
        encoding="utf-8")
    # Un index qui survit à ses concepts pointe dans le vide : on le retire.
    for index in run.rglob("index.md"):
        if index.parent != run and index.parent not in par_dossier:
            index.unlink()

    for d, fichiers in sorted(par_dossier.items()):
        titre = TITRES.get(d.name, d.name.replace("-", " ").capitalize())
        lignes = [f"# {titre}", ""]
        for f in fichiers:
            fm = frontmatter(f) or {}
            lignes.append(f'- [{fm.get("title", f.stem)}]({f.name}) — {fm.get("description", "")}'.rstrip(" —"))
        (d / "index.md").write_text("\n".join(lignes) + "\n", encoding="utf-8")
    return par_dossier


RE_LIEN = re.compile(r"\[[^\]]*\]\(([^)]+)\)")


def controler(run):
    erreurs = []
    tous = list(concepts(run))
    ensemble = {f.resolve() for f in tous}
    entrants, sortants = set(), set()

    for f in tous:
        fm = frontmatter(f)
        if fm is None:
            erreurs.append(f"{f.relative_to(run)} — concept sans frontmatter lisible")
            continue
        if not fm.get("type"):
            erreurs.append(f"{f.relative_to(run)} — la règle dure d'OKF : un « type » non vide")
        for m in RE_LIEN.finditer(f.read_text(encoding="utf-8")):
            cible = m.group(1).split("#")[0]
            if not cible or cible.startswith(("http", "mailto:", "#")):
                continue
            resolu = (f.parent / cible).resolve()
            if resolu.name in RESERVES:
                continue
            if resolu in ensemble:
                sortants.add(f.resolve()); entrants.add(resolu)
            elif not resolu.exists():
                erreurs.append(f"{f.relative_to(run)} — lien mort vers {cible}")

    for f in tous:
        if f.resolve() not in entrants and f.resolve() not in sortants:
            erreurs.append(
                f"{f.relative_to(run)} — orphelin : aucun lien entrant ni sortant. "
                "Un agent qui traverse le bundle ne l'atteindra jamais"
            )
    return erreurs, tous


def journal(run, n):
    f = run / "conduite" / "log.md"
    f.parent.mkdir(parents=True, exist_ok=True)
    jour = dt.date.today().isoformat()
    puce = f"- Indexation — {n} concepts (dmad-okf-index/0.4.0)"
    rubriques, ordre = {}, []
    if f.exists():
        for bloc in re.split(r"^## ", f.read_text(encoding="utf-8"), flags=re.M)[1:]:
            date, _, reste = bloc.partition("\n")
            date = date.strip()
            rubriques.setdefault(date, []); ordre.append(date)
            rubriques[date] += [l for l in reste.splitlines() if l.strip()]
    rubriques.setdefault(jour, [])
    if puce not in rubriques[jour]:
        rubriques[jour].insert(0, puce)
    out = ["# Journal du run", ""]
    for date in sorted(set(ordre) | {jour}, reverse=True):
        out += [f"## {date}", ""] + rubriques[date] + [""]
    f.write_text("\n".join(out), encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("run", type=pathlib.Path)
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()

    relier(args.run)
    par_dossier = indexer(args.run)
    n = sum(len(v) for v in par_dossier.values())
    journal(args.run, n)
    print(f"✓ {n} concept(s) indexé(s) dans {len(par_dossier)} répertoire(s)")

    if args.check:
        erreurs, _ = controler(args.run)
        if erreurs:
            print(f"\n✗ {len(erreurs)} défaut(s)\n")
            for e in erreurs:
                print(f"  {e}")
            return 1
        print("✓ conformant : tout concept porte son type, aucun orphelin, aucun lien mort")
    return 0


if __name__ == "__main__":
    sys.exit(main())
