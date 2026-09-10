#!/usr/bin/env python3
"""Exporte l'evidence store d'un run DMAD en bundle Open Knowledge Format.

Le graphe est de la connaissance destinée à un agent : c'est exactement ce
qu'OKF normalise. Les trois documents du corpus, eux, sont lus par des humains
et **restent dehors** — la garde d'OKF le dit, et un bundle n'est pas un
substitut à un document qu'on ouvre lundi matin.

Le recouvrement est presque champ pour champ :

    evidence[]            → sources[]
    evidence.tool         → sources[].author, en process:<outil>
    produced_by           → generated.by, en <producteur>/<version>
    promotion par test    → verified[{by: process:characterization-test}]
    intent.validated_by   → verified[{by: human:<id>}] sur le concept d'intention
    freshness / status    → status + freshness conservé en clé d'extension

Deux choix de conception, expliqués dans docs/14-okf.md :

**L'intention devient un concept propre.** `verified` vouche pour le concept
entier ; le poser sur une claim dont seule l'intention a été validée ferait
croire que le fait a été vérifié. La séparation fait/intention (D6) devient
structurelle au lieu d'être conventionnelle.

**`confidence_reason` reste.** OKF n'a rien de tel, et c'est le champ qui force
un agent à écrire ce qui manque pour monter d'un niveau. Le supprimer au nom de
la conformité serait perdre le meilleur pour gagner l'interopérable.

    python3 tools/okf-export.py <dossier-run> [--out <bundle>] [--check]
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

VERSION_PRODUCTEUR = "0.4.0"

# dossier source → (dossier du bundle, type OKF par défaut, titre de section)
PLAN = {
    "capabilities":     ("capabilities",     "Capability",       "Capacités"),
    "business-objects": ("business-objects", "BusinessObject",   "Business objects"),
    "contracts":        ("contracts",        "ExternalContract", "Contrats sortants"),
    "claims":           ("claims",           None,               "Affirmations"),
    "open-questions":   ("open-questions",   "OpenQuestion",     "Questions ouvertes"),
    "challenges":       ("challenges",       "Challenge",        "Réfutations"),
    "documents":        ("documents",        "Document",         "Documents du corpus"),
    "diagrams":         ("diagrams",         "Diagram",          "Diagrammes"),
}

# DMAD parle de cycle de vie d'une claim ; OKF parle de cycle de vie d'un concept.
STATUT = {"draft": "draft", "challenged": "draft", "validated": "stable", "retired": "deprecated"}

RESERVES = {"index.md", "log.md"}


def slug(x):
    return re.sub(r"[^a-z0-9-]+", "-", str(x).lower()).strip("-")


def acteur(nom):
    """Convention d'acteurs OKF. C'est elle qui rend le niveau de confiance calculable."""
    if not nom:
        return None
    if nom.startswith(("human:", "process:")) or "/" in nom:
        return nom
    return f"dmad-{nom}/{VERSION_PRODUCTEUR}"


def bloc_yaml(fm):
    return "---\n" + yaml.safe_dump(fm, allow_unicode=True, sort_keys=False).rstrip() + "\n---\n"


def sources_depuis(evidence):
    out = []
    for i, ev in enumerate(evidence or [], 1):
        s = {"id": f"ev-{i}", "resource": ev.get("ref", "")}
        if ev.get("commit"):
            s["resource"] = f'{s["resource"]}@{ev["commit"]}'
        if ev.get("tool"):
            s["author"] = f'process:{ev["tool"]}'
        if ev.get("kind"):
            s["kind"] = ev["kind"]
        if ev.get("outcome"):
            s["outcome"] = ev["outcome"]
        out.append(s)
    return out


def lien(depuis, vers):
    """Lien relatif. La forme absolue est servie en 404 par GitHub et ne construit
    aucune arête dans les visualiseurs — Google a converti ses propres bundles."""
    import os
    return os.path.relpath(vers, depuis.parent).replace("\\", "/")


class Bundle:
    def __init__(self, racine, horodatage):
        self.racine = racine
        self.at = horodatage
        self.concepts = {}          # dmad_id -> chemin
        self.liens = []             # (source, cible) en chemins
        self.non_resolus = []       # (source, dmad_id visé)
        self.fichiers = {}          # chemin -> (frontmatter, corps, liens sortants)

    def ajouter(self, dmad_id, dossier, nom, fm, corps, sortants):
        chemin = self.racine / dossier / f"{nom}.md"
        self.concepts[dmad_id] = chemin
        self.fichiers[chemin] = (fm, corps, sortants)

    def ecrire(self):
        for chemin, (fm, corps, sortants) in self.fichiers.items():
            chemin.parent.mkdir(parents=True, exist_ok=True)
            renvois = []
            for cible_id, libelle in sortants:
                cible = self.concepts.get(cible_id)
                if cible is None:
                    # Une cible hors du run est possible ; la perdre en silence
                    # ne l'est pas — c'est une arête du graphe qui disparaît.
                    self.non_resolus.append((chemin, cible_id))
                    continue
                renvois.append(f"- {libelle} : [{cible_id}]({lien(chemin, cible)})")
                self.liens.append((chemin, cible))
            bloc = ("\n# Liens\n\n" + "\n".join(renvois) + "\n") if renvois else ""
            chemin.write_text(bloc_yaml(fm) + "\n" + corps.rstrip() + "\n" + bloc, encoding="utf-8")

    def index(self):
        titres = {v[0]: v[2] for v in PLAN.values()}
        titres["intents"] = "Intentions"
        # Tout répertoire du bundle reçoit son index : sans lui, la divulgation
        # progressive s'arrête, et un agent qui descend ne trouve plus rien.
        # Tous les répertoires du bundle, y compris les strates documentaires
        # écrites par les rédacteurs : l'index racine ne doit pas les effacer.
        dossiers = sorted({c.parent.name for c in self.fichiers} |
                          {d.name for d in self.racine.iterdir()
                           if d.is_dir() and not d.name.startswith(".")})
        for dossier in dossiers:
            titre = titres.get(dossier, dossier.replace("-", " ").capitalize())
            d = self.racine / dossier
            if not d.is_dir():
                continue
            entrees = []
            for f in sorted(d.glob("*.md")):
                if f.name in RESERVES:
                    continue
                fm, _, _ = self.fichiers[f]
                entrees.append(f'- [{fm.get("title", f.stem)}]({f.name}) — {fm.get("description", "")}')
            (d / "index.md").write_text(f"# {titre}\n\n" + "\n".join(entrees) + "\n", encoding="utf-8")

        sections = [f"- [{titres.get(d, d)}]({d}/index.md)" for d in dossiers
                    if (self.racine / d).is_dir()]
        (self.racine / "index.md").write_text(
            '---\nokf_version: "0.2"\n---\n\n'
            "# Evidence store DMAD\n\n"
            "La couche de preuve d'un run DMAD, en bundle Open Knowledge Format.\n\n"
            "Les trois documents du corpus — STD, SFD, SFG — ne sont **pas** dans ce bundle : "
            "ils sont lus par des humains, et la garde d'OKF réserve le format à ce qu'un agent "
            "lit. Le bundle porte ce qui les fonde, et chaque `Document` y garde sa carte "
            "d'identité pour que la cascade reste traversable.\n\n"
            "# Sections\n\n" + "\n".join(sections) + "\n", encoding="utf-8")

    def journal(self, run):
        """Append-only, plus récent en tête, une seule rubrique par date.

        Deux rubriques portant la même date sont un artefact de fusion : un
        consommateur ne sait plus laquelle fait foi.
        """
        f = self.racine / "log.md"
        jour = self.at[:10]
        puce = (f"- Export du run `{run.name}` — {len(self.concepts)} concepts "
                f"(dmad-okf-export/{VERSION_PRODUCTEUR})")
        rubriques, ordre = {}, []
        if f.exists():
            for bloc in re.split(r"^## ", f.read_text(encoding="utf-8"), flags=re.M)[1:]:
                date, _, reste = bloc.partition("\n")
                date = date.strip()
                if date not in rubriques:
                    rubriques[date] = []; ordre.append(date)
                rubriques[date] += [l for l in reste.splitlines() if l.strip()]
        if jour not in rubriques:
            rubriques[jour] = []; ordre.insert(0, jour)
        if puce not in rubriques[jour]:
            rubriques[jour].insert(0, puce)
        out = ["# Journal du bundle", ""]
        for date in sorted(set(ordre), reverse=True):
            out += [f"## {date}", ""] + rubriques[date] + [""]
        f.write_text("\n".join(out), encoding="utf-8")


def premiere_phrase(txt, defaut=""):
    txt = " ".join((txt or "").split())
    if not txt:
        return defaut
    m = re.search(r"^(.{10,200}?[.!?])(\s|$)", txt)
    return m.group(1) if m else (txt[:180] + "…" if len(txt) > 180 else txt)


def charger(d):
    if not d.is_dir():
        return []
    out = []
    for p in sorted(d.glob("*.y*ml")):
        try:
            doc = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
        except yaml.YAMLError as e:
            print(f"  ⚠ {p} illisible : {e}")
            continue
        out.append(doc)
    return out


def exporter(run, sortie, at=None):
    at = at or dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    b = Bundle(sortie, at)

    # Les capacités peuvent être des fichiers du run ou de simples étiquettes sur
    # les claims. On rattache au fichier quand il existe, plutôt que de créer un
    # doublon qui laisserait l'original orphelin.
    caps_fichiers = {a.get("id") for a in charger(run / "capabilities") if a.get("id")}

    for dossier, (cible, type_defaut, _) in PLAN.items():
        for art in charger(run / dossier):
            aid = art.get("id") or art.get("name")
            if not aid:
                continue
            typ = art.get("type") or type_defaut or "Concept"
            titre = art.get("functional_name") or art.get("title") or str(aid)
            desc = premiere_phrase(
                art.get("statement") or art.get("question") or art.get("path") or titre, titre)

            fm = {"type": typ, "title": str(titre), "description": desc, "dmad_id": aid}
            if art.get("capability"):
                fm["tags"] = [art["capability"]]
            src = sources_depuis(art.get("evidence"))
            if src:
                fm["sources"] = src
            fm["generated"] = {"by": acteur(art.get("produced_by") or "exporter"), "at": at}

            verifs = []
            if art.get("promoted_by") == "test-forger":
                verifs.append({"by": "process:characterization-test", "at": at})
            if verifs:
                fm["verified"] = verifs

            statut = STATUT.get(art.get("status"))
            if statut and statut != "stable":
                fm["status"] = statut

            for cle in ("confidence", "confidence_reason", "confidence_ceiling_applied",
                        "conditional_on", "challenge_outcome", "freshness",
                        "resolution_rung", "artifact", "artifact_version", "code",
                        "recursive_depth", "business_layer", "kind", "unit", "frozen_at",
                        "priority", "audience", "outcome"):
                if art.get(cle) is not None:
                    fm[cle] = art[cle]

            corps = art.get("statement") or art.get("question") or ""
            if corps and src:
                # Chaque preuve est citée. Une note définie et jamais appelée
                # laisse croire qu'une preuve fonde une phrase qu'elle ne fonde pas.
                corps = corps.rstrip() + "".join(f'[^{s["id"]}]' for s in src)
            if art.get("why_it_matters"):
                corps += f'\n\n# Pourquoi ça compte\n\n{art["why_it_matters"]}'
            if art.get("context"):
                corps += f'\n\n# Contexte\n\n{art["context"]}'
            if src:
                corps += "\n\n" + "\n".join(
                    f'[^{s["id"]}]: {s["resource"]}' for s in src)

            sortants = []
            for cid in art.get("relates_to") or []:
                sortants.append((cid, "en relation avec"))
            for cid in art.get("open_questions") or []:
                sortants.append((cid, "question ouverte"))
            for cid in art.get("challenged_by") or []:
                sortants.append((cid, "réfuté par"))
            for cid in art.get("related_claims") or []:
                sortants.append((cid, "porte sur"))
            for cid in art.get("sub_objects") or []:
                sortants.append((cid, "compose"))
            for cid in art.get("derives_from") or []:
                sortants.append((cid, "dérive de"))
            for cid in art.get("claims_rendered") or []:
                sortants.append((cid, "publie"))
            for f in art.get("own_leaves") or []:
                if f.get("kind") == "contract":
                    sortants.append((f["ref"], "appelle le contrat"))
            if art.get("claim"):
                sortants.append((art["claim"], "attaque"))
            if art.get("capability"):
                cap = art["capability"]
                sortants.append((cap if cap in caps_fichiers else f"CAP-{slug(cap)}", "relève de"))
            if art.get("document"):
                sortants.append((art["document"], "illustre"))

            b.ajouter(aid, cible, slug(aid), fm, corps, sortants)

            # L'intention devient un concept propre : verified doit dire la vérité.
            intent = art.get("intent")
            if intent and intent.get("statement"):
                iid = f"INT-{aid}"
                ifm = {"type": "Intent", "title": f"Intention — {titre}",
                       "description": premiere_phrase(intent["statement"]),
                       "dmad_id": iid, "confidence": intent.get("confidence", "H")}
                isrc = sources_depuis(intent.get("evidence"))
                if isrc:
                    ifm["sources"] = isrc
                ifm["generated"] = {"by": acteur("archaeologist"), "at": at}
                val = intent.get("validated_by")
                if val and val.get("who"):
                    ifm["verified"] = [{"by": f'human:{slug(val["who"])}', "at": val.get("when", at)}]
                icorps = intent["statement"]
                for h in intent.get("competing_hypotheses") or []:
                    icorps += f"\n\n# Lecture concurrente\n\n{h}"
                b.ajouter(iid, "intents", slug(iid), ifm, icorps, [(aid, "explique")])
                sortants.append((iid, "intention supposée"))

    # Une capacité qui n'est qu'une étiquette est matérialisée en concept : sans
    # elle, les claims qui s'y rattachent perdent leur point de regroupement.
    capacites = {a.get("capability") for d in ("claims", "business-objects")
                 for a in charger(run / d) if a.get("capability")}
    for cap in sorted(c for c in capacites if c and c not in caps_fichiers):
        cid = f"CAP-{slug(cap)}"
        if cid in b.concepts:
            continue
        membres = [(a["id"], "regroupe") for d in ("claims", "business-objects")
                   for a in charger(run / d) if a.get("capability") == cap and a.get("id")]
        b.ajouter(cid, "capabilities", slug(cid),
                  {"type": "Capability", "title": cap.capitalize(),
                   "description": f"Capacité métier « {cap} ».", "dmad_id": cid,
                   "generated": {"by": acteur("carver"), "at": at}},
                  f"Capacité métier « {cap} », validée au gate de découpage.", membres)

    b.ecrire()
    b.index()
    b.journal(run)
    return b


def controler(b):
    """La règle dure d'OKF, plus les deux contrôles du mode strict."""
    erreurs = []
    concepts = set(b.fichiers)

    for chemin, (fm, _, _) in b.fichiers.items():
        if not fm.get("type"):
            erreurs.append(f"{chemin} — la règle dure d'OKF : un concept porte un « type » non vide")

    cibles = {c for _, c in b.liens}
    sources = {s for s, _ in b.liens}
    for chemin in concepts:
        if chemin not in cibles and chemin not in sources:
            erreurs.append(
                f"{chemin} — orphelin : aucun lien entrant ni sortant. Un agent qui "
                "traverse le bundle ne l'atteindra jamais, donc il manque par construction"
            )
    for _, cible in b.liens:
        if cible not in concepts:
            erreurs.append(f"lien mort vers {cible}")
    return erreurs


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("run", type=pathlib.Path)
    ap.add_argument("--out", type=pathlib.Path)
    ap.add_argument("--check", action="store_true", help="contrôler la conformité après export")
    ap.add_argument("--at", help="horodatage de l'export (ISO). Le fixer rend l'export "
                                 "reproductible : sans lui, un bundle versionné change à chaque passe")
    args = ap.parse_args()

    sortie = args.out or (args.run / "okf")
    b = exporter(args.run, sortie, args.at)
    print(f"✓ {len(b.concepts)} concept(s) → {sortie}")

    if b.non_resolus:
        print(f"\n⚠ {len(b.non_resolus)} lien(s) vers un artefact absent du run :")
        for source, cible in b.non_resolus:
            print(f"  {source.name} → {cible}")
        print("  Ce n'est pas forcément une faute — la cible peut être hors périmètre —")
        print("  mais c'est une arête du graphe qui n'existe pas dans le bundle.\n")

    if args.check:
        erreurs = controler(b)
        if erreurs:
            print(f"\n✗ {len(erreurs)} défaut(s) de conformité\n")
            for e in erreurs:
                print(f"  {e}")
            return 1
        print("✓ conformant : tout concept porte son type, aucun orphelin, aucun lien mort")
    return 0


if __name__ == "__main__":
    sys.exit(main())
