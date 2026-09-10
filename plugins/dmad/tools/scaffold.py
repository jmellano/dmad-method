#!/usr/bin/env python3
"""Matérialise, depuis un plan, les concepts vides que le rédacteur remplira.

Le gabarit d'un document DMAD n'est pas un fichier à copier : c'est **le plan**.
La consigne de rédaction y vit à côté du numéro de section qu'elle concerne —
deux copies d'une consigne divergent, et c'est la copie qu'on lit qui est la
mauvaise.

Cet outil crée un concept par section du plan, avec son frontmatter et sa
consigne en commentaire. Le rédacteur remplit et **supprime la consigne au fur
et à mesure** ; `check-corpus.py` refuse un document qui en porte encore.

Il **n'écrase jamais** un concept existant : un scaffold rejoué après une passe
de rédaction ne détruit rien, et sert à créer les sections qu'on a ajoutées.

    python3 tools/scaffold.py <plan.yaml> --bundle <bundle> [--dry-run]
"""
import argparse
import pathlib
import re
import sys
import unicodedata

try:
    import yaml
except ImportError:  # pragma: no cover
    sys.exit("dépendance manquante : pip install pyyaml")

AUDIENCE = {"STD": "MOE", "SFD": "hybride MOA/MOE", "SFG": "Utilisateurs métier"}


def slug(x):
    """Translittère avant de remplacer : « modèle de données » donne
    « modele-de-donnees », pas « mod-le-de-donn-es »."""
    t = unicodedata.normalize("NFKD", str(x))
    t = "".join(c for c in t if not unicodedata.combining(c)).lower()
    return re.sub(r"[^a-z0-9]+", "-", t).strip("-")


def squelette(plan, section, chemin_bundle):
    kind = plan["kind"]
    num = section["number"]
    fm = plan.get("frontmatter") or {}
    consigne = section.get("guidance", "").strip()

    lignes = [
        "---",
        f'type: "{section.get("type", "Technical Section")}"',
        f'title: "{section["title"]}"',
        f'description: "{{{{une phrase — ce que ce concept dit, pas ce qu\'il couvre}}}}"',
        f'tags: ["{kind}"]',
        "generated:",
        f'  by: "dmad-writer-{kind.lower()}/0.4.0"',
        '  at: "{{AAAA-MM-JJTHH:MM:SSZ}}"',
        'status: "draft"',
        "# — extensions du profil DMAD : voir docs/14-okf.md",
        f'module: "{fm.get("module", "{{module}}")}"',
        f'audience: "{fm.get("audience", AUDIENCE.get(kind, "{{audience}}"))}"',
        'confidence: "{{high | medium}}"',
        'last_code_sync: "{{sha du commit analysé}}"',
        "renders: []",
        "---",
        "",
    ]
    if consigne:
        lignes += ["<!-- [gabarit]", f"  § {num or 'chapeau'} — {section['title']}", ""]
        lignes += ["  " + l for l in _replier(consigne)]
        lignes += ["", "  Supprimer ce bloc une fois la section écrite.", "-->", ""]
    lignes += ["{{à écrire}}", ""]
    return "\n".join(lignes)


def _replier(txt, largeur=88):
    mots, ligne, out = txt.split(), "", []
    for m in mots:
        if len(ligne) + len(m) + 1 > largeur:
            out.append(ligne); ligne = m
        else:
            ligne = f"{ligne} {m}".strip()
    if ligne:
        out.append(ligne)
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("plan", type=pathlib.Path)
    ap.add_argument("--bundle", type=pathlib.Path, required=True)
    ap.add_argument("--prefix", default="", help="préfixe de chemin dans le bundle, ex. processus/facturation")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    plan = yaml.safe_load(args.plan.read_text(encoding="utf-8"))
    strate = plan["kind"].lower()
    base = args.bundle / args.prefix / strate if args.prefix else args.bundle / strate

    crees, existants, maj_plan = [], [], False
    for section in plan["sections"]:
        if section.get("concept"):
            chemin = args.bundle / section["concept"]
            if chemin.exists():
                existants.append(section["concept"]); continue
        else:
            if section.get("free_subsections"):
                continue          # section de structure : son corps vient des sous-sections
            nom = slug(f'{section["number"] or "chapeau"}-{section["title"]}')[:60]
            rel = str((base / f"{nom}.md").relative_to(args.bundle))
            section["concept"] = rel
            maj_plan = True
            chemin = args.bundle / rel

        crees.append(str(chemin.relative_to(args.bundle)))
        if not args.dry_run:
            chemin.parent.mkdir(parents=True, exist_ok=True)
            chemin.write_text(squelette(plan, section, chemin), encoding="utf-8")

    if maj_plan and not args.dry_run:
        args.plan.write_text(yaml.safe_dump(plan, allow_unicode=True, sort_keys=False, width=100),
                             encoding="utf-8")

    verbe = "à créer" if args.dry_run else "créé(s)"
    print(f'{plan["kind"]} — {len(crees)} concept(s) {verbe}, {len(existants)} déjà écrit(s)')
    for c in crees:
        print(f"  + {c}")
    if crees and not args.dry_run:
        print("\nChaque concept porte sa consigne en bloc [gabarit]. La supprimer au fur et à "
              "mesure :\ncheck-corpus.py refuse un document qui en porte encore.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
