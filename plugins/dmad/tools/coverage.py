#!/usr/bin/env python3
"""Calcule le rapport de couverture d'un run.

La couverture est **la seule métrique honnête et calculable** de la méthode, par
opposition à un pourcentage de confiance qui serait une opinion déguisée en
chiffre. Elle doit donc être calculée, pas rédigée.

Ce que cet outil calcule depuis l'evidence store : la répartition des niveaux de
preuve, la résolution des contrats par barreau, l'effet du Challenger, le corpus
produit. Ce qu'il **lit** dans `facts/coverage.json` s'il existe : fichiers,
fonctions, points d'entrée, hotspots, tables. Ce qu'il n'invente jamais : le
reste — un indicateur absent est écrit « non mesuré ».

**Les chiffres se calculent, leur interprétation s'écrit.** `--commentaire` ajoute
la lecture rédigée par le Curator : dire que 22 % de couverture avec 90 % des
hotspots est un bon résultat n'est pas un calcul, c'est un argument.

    python3 tools/coverage.py <dossier-run> [--out couverture.md]
"""
import argparse
import collections
import json
import pathlib
import sys

try:
    import yaml
except ImportError:  # pragma: no cover
    sys.exit("dépendance manquante : pip install pyyaml")

# Poids de lecture, pas de calcul : ils disent au lecteur ce qui compte.
POIDS = {
    "files": "faible", "functions": "moyen", "entrypoints": "**fort**",
    "hotspots": "**fort**", "tables": "moyen",
}
LIBELLES = {
    "files": "Fichiers atteints", "functions": "Fonctions cartographiées",
    "entrypoints": "Points d'entrée couverts", "hotspots": "Hotspots couverts",
    "tables": "Tables documentées",
}
DEGRADE = {"confirmed": 0, "demoted": 1, "contradicted": 1, "split": 1, "reformulate": 1}


def charger(racine, *sous):
    """Cherche dans chaque processus, puis à la racine. Le sujet avant la nature."""
    out = []
    for chemin in sous:
        for d in list((racine / "processus").glob(f"*/{chemin}")) + [racine / chemin]:
            if not d.is_dir():
                continue
            for path in sorted(list(d.glob("*.y*ml")) + list(d.glob("*.md"))):
                txt = path.read_text(encoding="utf-8")
                if path.suffix == ".md":
                    if not txt.startswith("---"):
                        continue
                    fin = txt.find("\n---", 3)
                    txt = txt[3:fin] if fin != -1 else ""
                try:
                    doc = yaml.safe_load(txt) or {}
                except yaml.YAMLError:
                    continue
                if isinstance(doc, dict):
                    out.append(doc)
    return out


def rendre(run, commentaire=None):
    claims = charger(run, "preuves/claims")
    contrats = charger(run, "preuves/contrats")
    challenges = charger(run, "preuves/challenges")
    documents = []
    questions = charger(run, "preuves/questions")

    l = [f"# Couverture de l'analyse — {run.name}", ""]

    # --- ce qui vient des faits, ou rien
    faits = next(iter(sorted(run.rglob("faits/coverage.json"))), run / "_absent")
    l += ["## Ce qui a été atteint", "", "| Indicateur | Valeur | Poids |", "|---|---|---|"]
    if faits.exists():
        mesures = json.loads(faits.read_text(encoding="utf-8"))
        for cle, libelle in LIBELLES.items():
            m = mesures.get(cle)
            if not m:
                l.append(f"| {libelle} | **non mesuré** | {POIDS[cle]} |")
                continue
            pct = round(100 * m["reached"] / m["total"]) if m.get("total") else 0
            l.append(f'| {libelle} | {m["reached"]} / {m["total"]} ({pct} %) | {POIDS[cle]} |')
    else:
        for cle, libelle in LIBELLES.items():
            l.append(f"| {libelle} | **non mesuré** — `facts/coverage.json` absent | {POIDS[cle]} |")

    # --- contrats par barreau : la qualité des sources, pas le nombre
    if contrats:
        par_barreau = collections.Counter(c.get("resolution_rung") for c in contrats)
        resolus = sum(n for b, n in par_barreau.items() if b in (1, 2, 3))
        detail = " · ".join(f"barreau {b} : {par_barreau[b]}" for b in sorted(par_barreau) if b)
        l.append(f"| **Contrats sortants résolus** | {resolus} / {len(contrats)} — {detail} | **fort** |")
    l.append("")

    if contrats:
        l += ["> **La ligne des contrats mesure la qualité des sources, pas le nombre.** Un run",
              "> à 47/47 dont trente sont au barreau 3 — le commentaire manuscrit, qui survit aux",
              "> refactorings et ment alors sans le dire — est un moins bon run qu'un 41/47",
              "> majoritairement au barreau 1. Sans cette ligne, les deux se ressemblent.", ""]

    # --- corpus produit
    if documents:
        l += ["## Corpus produit", "", "| Document | Unité | État |", "|---|---|---|"]
        for d in sorted(documents, key=lambda x: x.get("kind", "")):
            fige = d.get("frozen_at")
            etat = f'figé le {fige[:10]}' if fige else "**non figé**"
            corrections = len((d.get("frozen_by") or {}).get("corrections") or [])
            if corrections:
                etat += f", {corrections} correction(s) en revue"
            l.append(f'| `{d.get("path")}` | {d.get("unit_ref")} | {etat} |')
        l += ["", "**Une revue qui ne demande aucune correction est un signal d'alarme**, pas un",
              "succès : elle signifie que le relecteur n'a pas cherché, ou que le document est",
              "trop vague pour être contesté.", ""]

    # --- niveaux de preuve
    if claims:
        n = collections.Counter(c.get("confidence") for c in claims)
        total = sum(n.values())
        pct = {k: round(100 * v / total) for k, v in n.items()}
        l += ["## Répartition des niveaux de preuve", "", "```",
              "  ·  ".join(f'{k} {pct.get(k, 0)} %' for k in ("V", "C", "I", "H")), "```", ""]
        alertes = []
        if pct.get("V", 0) > 60:
            alertes.append("`V` > 60 % — suspect : peu de legacy se prouve à ce point")
        if pct.get("H", 0) > 25:
            alertes.append("`H` > 25 % — historique manquant ou intentions non validées")
        if pct.get("I", 0) > 50:
            alertes.append("`I` > 50 % — outillage probablement dégradé")
        l += (["**Signaux d'alerte**", ""] + [f"- {a}" for a in alertes] + [""]) if alertes else \
             ["Aucun signal d'alerte : la répartition est dans les bornes attendues.", ""]

    # --- effet du Challenger
    if challenges:
        touches = sum(DEGRADE.get(c.get("outcome"), 0) for c in challenges)
        taux = round(100 * touches / len(challenges))
        verdict = ("dans la fourchette attendue (15–30 %)" if 15 <= taux <= 30 else
                   "**hors fourchette** — sous 15 % le Challenger est complaisant, "
                   "au-dessus de 30 % l'Elucidator produit trop de bruit")
        l += [f"**Effet du Challenger :** {len(challenges)} claim(s) examinée(s), {touches} "
              f"dégradée(s), scindée(s) ou contredite(s) — soit **{taux} %**, {verdict}.", ""]

    # --- questions ouvertes
    if questions:
        p = collections.Counter(q.get("priority") for q in questions)
        l += [f'**Questions ouvertes :** {len(questions)} — '
              + " · ".join(f"{k} : {p[k]}" for k in sorted(p) if k), ""]

    if commentaire and commentaire.exists():
        l += ["## Lecture", "", commentaire.read_text(encoding="utf-8").strip(), ""]

    return "\n".join(l)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("run", type=pathlib.Path)
    ap.add_argument("--out", type=pathlib.Path)
    ap.add_argument("--commentaire", type=pathlib.Path,
                    help="fichier de lecture, ajouté en fin de rapport. Les chiffres se "
                         "calculent, leur interprétation s'écrit — c'est le travail du Curator")
    args = ap.parse_args()
    rapport = rendre(args.run, args.commentaire)
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(rapport + "\n", encoding="utf-8")
        print(f"✓ {args.out}")
    else:
        print(rapport)
    return 0


if __name__ == "__main__":
    sys.exit(main())
