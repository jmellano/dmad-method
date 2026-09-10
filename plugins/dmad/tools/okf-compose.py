#!/usr/bin/env python3
"""Compose un document du corpus depuis le bundle OKF et son plan.

**Le bundle est la sortie primaire, le document en est dérivé** (D26). Un
rédacteur écrit des concepts ; le plan dit quel concept occupe quel numéro de
section ; ce composeur assemble. Une correction se fait **dans le concept**,
jamais dans le fichier composé — une édition faite ici est perdue à la
régénération suivante.

Ce qui décide du contenu et de l'ordre est le **plan numéroté**, et le niveau de
titre se déduit du numéro : profondeur + 1. Le § 3.2.1 est un `h4`, des deux
côtés.

Le composeur REFUSE de produire — il ne produit pas un document approximatif :

  1. un concept du plan introuvable dans le bundle
  2. un concept documentaire du bundle absent du plan — du contenu écrit que
     personne ne lira, et que rien d'autre ne signalerait
  3. une section imposée sans concept ni sous-section : le constat d'absence
     manque, et une section absente se lit « oubliée »
  4. un saut de niveau de titre
  5. un lien mort — fichier ou ancre

    python3 tools/okf-compose.py <bundle> <plan.yaml> [--out <fichier>] [--check-only]
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

RE_TITRE = re.compile(r"^(#{1,6}) +(.+?)\s*$", re.M)
RE_LIEN = re.compile(r"\[([^\]]*)\]\(([^)]+)\)")
RE_RENVOI = re.compile(r"§ ?([0-9]+(?:\.[0-9]+)*)")


def ancre(titre):
    """Ancre GitHub : minuscules, diacritiques retirés, non-alphanumériques en tirets."""
    t = unicodedata.normalize("NFKD", titre)
    t = "".join(c for c in t if not unicodedata.combining(c)).lower()
    t = re.sub(r"[^\w\s-]", "", t).strip()
    return re.sub(r"[\s_]+", "-", t)


def profondeur(numero):
    return 0 if not numero else numero.count(".") + 1


def corps(chemin):
    """Le corps d'un concept, frontmatter et titre h1 retirés."""
    t = chemin.read_text(encoding="utf-8")
    if t.startswith("---"):
        fin = t.find("\n---", 3)
        if fin != -1:
            t = t[fin + 4:]
    t = re.sub(r"\A\s*# .+?\n", "", t)
    # « # Liens » est la navigation interne au bundle : elle relie les concepts
    # entre eux pour qu'aucun ne soit orphelin. Le document composé n'en a pas
    # besoin — et son titre de niveau 1 fausserait le calcul de décalage.
    t = re.split(r"^# Liens\s*$", t, maxsplit=1, flags=re.M)[0]
    return t.strip("\n")


def rebaser_liens(corps_txt, depuis, vers):
    """Un lien écrit depuis un concept ne résout pas depuis le fichier composé.

    C'est le pendant de la règle inverse chez le producteur : un lien vers un
    concept absent de l'export n'est pas cassé, il est réécrit vers le bundle.
    """
    import os
    def rep(m):
        libelle, cible = m.group(1), m.group(2)
        if cible.startswith(("http", "mailto:", "#")) or ":" in cible.split("/")[0]:
            return m.group(0)
        chemin, _, ancre_ = cible.partition("#")
        if not chemin:
            return m.group(0)
        absolu = (depuis.parent / chemin).resolve()
        rel = os.path.relpath(absolu, vers.parent).replace("\\", "/")
        return f'[{libelle}]({rel}{"#" + ancre_ if ancre_ else ""})'
    return RE_LIEN.sub(rep, corps_txt)


def decaler(corps_txt, base):
    """Décale les titres du corps pour qu'ils tiennent sous la section."""
    if not corps_txt:
        return corps_txt
    niveaux = [len(m.group(1)) for m in RE_TITRE.finditer(corps_txt)]
    if not niveaux:
        return corps_txt
    delta = (base + 1) - min(niveaux)
    if delta == 0:
        return corps_txt
    def rep(m):
        n = max(1, min(6, len(m.group(1)) + delta))
        return "#" * n + " " + m.group(2)
    return RE_TITRE.sub(rep, corps_txt)


def composer(bundle, plan, erreurs, sortie=None):
    sortie = sortie or pathlib.Path(plan["output"])
    lignes = []
    fm = dict(plan.get("frontmatter") or {})
    if fm:
        fm.setdefault("type", plan["kind"])
        fm.setdefault("title", plan.get("title", plan["unit_ref"]))
        fm.setdefault("unit", plan["unit"])
        fm.setdefault("unit_ref", plan["unit_ref"])
        if plan.get("derives_from"):
            fm.setdefault("derives_from", plan["derives_from"])
        lignes += ["---",
                   yaml.safe_dump(fm, allow_unicode=True, sort_keys=False).rstrip(),
                   "---", ""]
    lignes += [f'# {plan.get("title", plan["unit_ref"])}', ""]
    ancres, utilises, dernier = set(), set(), 0

    for s in plan["sections"]:
        num, titre = s["number"], s["title"]
        niveau = profondeur(num) + 1

        if num:
            if niveau > dernier + 1 and dernier:
                erreurs.append(
                    f'§ {num} « {titre} » : saut de niveau de titre (h{dernier} → h{niveau}). '
                    "Le sommaire et l'export s'en trouvent cassés"
                )
            dernier = niveau
            point = "." if "." not in num else ""
            entete = f'{"#" * niveau} {num}{point} {titre}'
            ancres.add(ancre(f"{num}-{titre}"))
        else:
            entete = None

        chemin_concept = s.get("concept")
        texte = ""
        if chemin_concept:
            f = bundle / chemin_concept
            if not f.exists():
                erreurs.append(
                    f'§ {num or "chapeau"} : concept introuvable — {chemin_concept}. '
                    "Le plan cite ce que le bundle ne porte pas"
                )
            else:
                utilises.add(chemin_concept)
                texte = decaler(rebaser_liens(corps(f), f, sortie), niveau)
        elif s.get("required", True) and not s.get("free_subsections"):
            enfants = [x for x in plan["sections"]
                       if x["number"].startswith(num + ".") and num]
            if not enfants:
                erreurs.append(
                    f'§ {num} « {titre} » : ni concept ni sous-section. Une section imposée '
                    "sans objet porte son constat d'absence et son périmètre — elle ne reste "
                    "pas vide, et elle ne se supprime pas"
                )

        if entete:
            lignes += [entete, ""]
        if texte:
            lignes += [texte, ""]

    return "\n".join(lignes).rstrip() + "\n", ancres, utilises


def controler_couverture(bundle, plan, utilises, erreurs):
    """L'inverse du contrôle habituel : du contenu écrit que le plan n'inclut pas."""
    strate = plan["kind"].lower()
    racines = {pathlib.Path(c).parent for c in
               (s.get("concept") for s in plan["sections"]) if c}
    for racine in racines:
        d = bundle / racine
        if not d.is_dir():
            continue
        for f in sorted(d.glob("*.md")):
            if f.name in ("index.md", "log.md"):
                continue
            rel = str(f.relative_to(bundle))
            if rel not in utilises:
                erreurs.append(
                    f"{rel} — concept de la strate {strate} absent du plan. "
                    "Il est écrit et personne ne le lira : soit le plan l'oublie, "
                    "soit le concept n'a pas lieu d'être"
                )


def controler_liens(doc, ancres, bundle, sortie, erreurs, freres=()):
    """Les documents du corpus se citent mutuellement : un frère annoncé par un
    autre plan du même run est une cible valide, même s'il n'est pas encore écrit."""
    attendus = {str(f) for f in freres} | {pathlib.Path(f).name for f in freres}
    for m in RE_LIEN.finditer(doc):
        cible = m.group(2)
        if cible.startswith(("http", "mailto:", "#")):
            if cible.startswith("#") and cible[1:] not in ancres:
                erreurs.append(f"ancre morte : {cible} (« {m.group(1)} »)")
            continue
        fichier = cible.split("#")[0]
        if fichier in attendus or pathlib.Path(fichier).name in attendus:
            continue
        if not (sortie.parent / fichier).resolve().exists():
            erreurs.append(f"lien de fichier cassé : {cible}")

    numeros = {a.split("-")[0] for a in ancres}
    for m in RE_RENVOI.finditer(doc):
        if m.group(1) not in numeros:
            erreurs.append(
                f"renvoi mort : § {m.group(1)}. Un renvoi mort se résout "
                "silencieusement au parent et passe pour valide"
            )


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("bundle", type=pathlib.Path)
    ap.add_argument("plan", nargs="?", type=pathlib.Path)
    ap.add_argument("--all", type=pathlib.Path, metavar="RUN",
                    help="composer tous les plan-*.yaml du run. Les documents du corpus se citent "
                         "mutuellement : ils ne se composent correctement qu'ensemble")
    ap.add_argument("--out", type=pathlib.Path)
    ap.add_argument("--check-only", action="store_true")
    args = ap.parse_args()

    if args.all:
        chemins = sorted((args.all).glob("plan-*.y*ml"))
        if not chemins:
            print("aucun plan dans ce run"); return 0
        plans = [(c, yaml.safe_load(c.read_text(encoding="utf-8"))) for c in chemins]
        freres = [pl["output"] for _, pl in plans]
        erreurs, rendus = [], []
        for chemin, plan in plans:
            sortie = args.all / plan["output"]
            errs = []
            doc, ancres, utilises = composer(args.bundle, plan, errs, sortie)
            controler_couverture(args.bundle, plan, utilises, errs)
            controler_liens(doc, ancres, args.bundle, sortie, errs, freres)
            if errs:
                erreurs += [f'{plan["kind"]} — {e}' for e in errs]
            else:
                rendus.append((sortie, doc, plan, utilises))
        if erreurs:
            print(f"✗ {len(erreurs)} refus — rien n'a été produit\n")
            for e in erreurs:
                print(f"  {e}")
            return 1
        for sortie, doc, plan, utilises in rendus:
            if not args.check_only:
                sortie.parent.mkdir(parents=True, exist_ok=True)
                sortie.write_text(doc, encoding="utf-8")
            print(f'  ✓ {plan["kind"]:<4} {len(utilises):>2} concept(s), '
                  f'{len(plan["sections"]):>2} section(s) → {plan["output"]}')
        print(f"\n✓ {len(rendus)} document(s) composé(s)")
        return 0

    if not args.plan:
        ap.error("donner un plan, ou --all <run>")
    plan = yaml.safe_load(args.plan.read_text(encoding="utf-8"))
    sortie = args.out or pathlib.Path(plan["output"])

    erreurs = []
    doc, ancres, utilises = composer(args.bundle, plan, erreurs, sortie)
    controler_couverture(args.bundle, plan, utilises, erreurs)
    controler_liens(doc, ancres, args.bundle, sortie, erreurs)

    if erreurs:
        print(f"✗ {len(erreurs)} refus — rien n'a été produit\n")
        for e in erreurs:
            print(f"  {e}")
        return 1

    if args.check_only:
        print(f'✓ {plan["kind"]} composable — {len(utilises)} concept(s), '
              f'{len(plan["sections"])} section(s)')
        return 0

    sortie.parent.mkdir(parents=True, exist_ok=True)
    sortie.write_text(doc, encoding="utf-8")
    print(f'✓ {sortie} — {len(utilises)} concept(s), {len(plan["sections"])} section(s)')
    return 0


if __name__ == "__main__":
    sys.exit(main())
