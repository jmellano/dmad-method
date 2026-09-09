#!/usr/bin/env python3
"""Vérifie les invariants du corpus DMAD sur les documents eux-mêmes.

`validate.py` valide des artefacts structurés contre des schémas. Cet outil-ci
valide des **documents Markdown** : la STD, la SFD et la SFG. Les deux échouent
pour des raisons différentes, et mélanger « ta claim viole le schéma » avec
« ta SFD contient un bloc SQL » n'aiderait personne.

Chaque message nomme la décision qu'il applique. Ce n'est pas de la cosmétique :
un message qui ne dit pas quelle règle il fait respecter se fait contourner,
puis supprimer, au premier agacement — et la règle disparaît avec lui.

    python3 tools/check-corpus.py <dossier-run>
"""
import argparse
import pathlib
import re
import sys

try:
    import yaml
except ImportError:  # pragma: no cover
    sys.exit("dépendance manquante : pip install pyyaml")

# D16 — le corpus porte des références, jamais du code. Un diagramme n'est pas
# du code : c'est le rendu d'un sous-graphe, et il reste autorisé.
FENCES_AUTORISEES = {"mermaid"}

# D20 — chaque document a son unité, et une seule.
UNITE_ATTENDUE = {"STD": "entrypoint", "SFD": "business_object_tree", "SFG": "use_case"}

# Les dix-sept sections de la STD ne s'omettent jamais : une section sans objet
# porte son constat d'absence et son périmètre.
STD_SECTIONS = 17

# Les sept blocs d'un cas d'usage de SFG. Reconnus par mot-clé, pour tolérer
# les variantes de formulation d'un titre.
SFG_BLOCS = [
    ("situation", "Situation"),
    ("acteur", "Acteurs et rôles métier"),
    ("déclencheur", "Déclencheur et cadence"),
    ("règles", "Règles applicables"),
    ("utilisateur voit", "Ce que l'utilisateur voit"),
    ("n'est pas couvert", "Ce qui n'est pas couvert"),
    ("traçabilité", "Traçabilité"),
]

RE_FENCE = re.compile(r"^\s*```([A-Za-z0-9_+-]+)\s*$", re.M)
RE_REGLE = re.compile(r"\b((?:RG|BR|INV)-[A-Z0-9]+(?:-[0-9]+)?)\b")
# Une règle est DÉCLARÉE quand elle ouvre une ligne de tableau. Une règle
# seulement citée dans le corps d'une autre — « sans appliquer RG-003 » — est
# un renvoi, pas une déclaration : l'exiger en traçabilité produirait du bruit.
RE_REGLE_DECLAREE = re.compile(r"^\s*\|\s*((?:RG|BR|INV)-[A-Z0-9]+(?:-[0-9]+)?)\b", re.M)


def lire(path):
    """Rend (frontmatter, corps, lignes). Frontmatter vide si absent ou illisible."""
    texte = path.read_text(encoding="utf-8")
    fm, corps = {}, texte
    if texte.startswith("---"):
        fin = texte.find("\n---", 3)
        if fin != -1:
            brut = texte[3:fin]
            try:
                fm = yaml.safe_load(brut) or {}
            except yaml.YAMLError as e:
                fm = {"__erreur__": str(e).splitlines()[0]}
            corps = texte[fin + 4:]
    return fm, corps, texte.splitlines()


def sections(corps, niveau="##"):
    """Découpe un corps en (titre, texte) sur les titres du niveau demandé."""
    motif = re.compile(rf"^{re.escape(niveau)} +(.+)$", re.M)
    bornes = [(m.start(), m.group(1).strip()) for m in motif.finditer(corps)]
    out = []
    for i, (debut, titre) in enumerate(bornes):
        fin = bornes[i + 1][0] if i + 1 < len(bornes) else len(corps)
        out.append((titre, corps[debut:fin]))
    return out


# ----------------------------------------------------------------- contrôles

def check_d16(rel, corps, erreurs):
    """D16 — aucun bloc de code, de requête ou de configuration."""
    for m in RE_FENCE.finditer(corps):
        langage = m.group(1).lower()
        if langage in FENCES_AUTORISEES:
            continue
        ligne = corps[:m.start()].count("\n") + 1
        erreurs.append(
            f"{rel}:{ligne} — D16 : bloc ```{langage} dans un document du corpus. "
            "Le corpus porte des références — fichier:lignes, signatures, noms de "
            "tables — jamais un extrait. Tant qu'un extrait est permis, aller lire "
            "le code a un motif légitime, et l'échelle de lecture devient poreuse"
        )


def check_frontmatter(rel, fm, erreurs):
    """Le frontmatter est la carte d'identité du document. Illisible, il n'existe pas."""
    if "__erreur__" in fm:
        erreurs.append(
            f"{rel} — frontmatter illisible : {fm['__erreur__']}. "
            "Les champs en phrase libre vont entre guillemets doubles : un « : » "
            "dans un scalaire nu se lit comme un mapping imbriqué et casse tout"
        )
        return False
    if not fm.get("type"):
        erreurs.append(f"{rel} — frontmatter sans « type ». STD, SFD ou SFG ?")
        return False
    return True


def check_cascade(rel, kind, fm, erreurs):
    """D17 et D20 — la position du document dans la cascade."""
    parents = fm.get("derives_from") or []
    if kind in ("SFD", "SFG") and not parents:
        erreurs.append(
            f"{rel} — D17 : une {kind} sans derives_from. Chaque document est "
            "l'abstraction du précédent ; sans ancrage, c'est une lecture "
            "indépendante — et deux lectures indépendantes divergent"
        )
    unite = fm.get("unit")
    attendue = UNITE_ATTENDUE.get(kind)
    if unite and attendue and unite != attendue:
        erreurs.append(
            f"{rel} — D20 : une {kind} a pour unité « {attendue} », pas « {unite} »"
        )
    return parents


def check_diagrammes(rel, corps, erreurs):
    """R1 — pas de question formulable, pas de diagramme."""
    for m in re.finditer(r"^\s*```mermaid\s*$", corps, re.M):
        amont = corps[:m.start()].splitlines()[-6:]
        if not any("?" in l for l in amont):
            ligne = corps[:m.start()].count("\n") + 1
            erreurs.append(
                f"{rel}:{ligne} — R1 : diagramme sans question. La question "
                "s'affiche au-dessus du diagramme ; un diagramme qui ne répond à "
                "rien occupe de la place, vieillit, et fait douter du reste"
            )


def check_std(rel, corps, erreurs):
    """Les dix-sept sections ne s'omettent jamais."""
    numeros = set()
    for titre, _ in sections(corps):
        m = re.match(r"^(\d{1,2})[.)]", titre.strip())
        if m:
            numeros.add(int(m.group(1)))
    manquantes = [n for n in range(1, STD_SECTIONS + 1) if n not in numeros]
    if manquantes:
        erreurs.append(
            f"{rel} — sections manquantes : {', '.join(map(str, manquantes))}. "
            "Une section sans objet ne se supprime pas : elle porte son constat "
            "d'absence et son périmètre. Une section absente se lit « oubliée » "
            "et pousse le lecteur à chercher lui-même"
        )


def check_sfd(rel, corps, parents, erreurs):
    """D17 — toute section de niveau s'ancre dans la STD dont elle dérive."""
    ancres = {pathlib.Path(str(p)).stem for p in parents if isinstance(p, str)}
    ancres.discard("claims")
    if not ancres:
        return
    for titre, texte in sections(corps):
        if not re.match(r"^\s*(N\d|\d+\.\s*N\d)", titre) and "—" not in titre:
            continue
        if not re.search(r"\bN\d", titre):
            continue
        if not any(a in texte for a in ancres):
            erreurs.append(
                f"{rel} — D17 : la section « {titre} » ne référence aucun ancrage "
                f"de {', '.join(sorted(ancres))}. Une section sans ancrage est une "
                "information apparue de nulle part"
            )


def check_sfg(rel, corps, erreurs):
    """Les sept blocs, la traçabilité, et l'index inverse."""
    cas = [(t, x) for t, x in sections(corps) if re.match(r"^CU-", t.strip())]
    if not cas:
        return

    toutes_regles = set()

    for titre, texte in cas:
        blocs = [b.lower() for b, _ in sections(texte, "###")]
        for cle, nom in SFG_BLOCS:
            if not any(cle in b for b in blocs):
                erreurs.append(
                    f"{rel} — « {titre} » : bloc « {nom} » manquant. "
                    "Sept blocs par cas d'usage, sans exception"
                )

        for bloc_titre, bloc_texte in sections(texte, "###"):
            if "n'est pas couvert" in bloc_titre.lower():
                contenu = re.sub(r"^###.*$", "", bloc_texte, flags=re.M).strip()
                if not contenu:
                    erreurs.append(
                        f"{rel} — « {titre} » : « Ce qui n'est pas couvert » est vide. "
                        "Un cas d'usage dont la frontière n'est pas écrite ne peut "
                        "être l'unité d'évolution de rien : personne ne saura si une "
                        "demande tombe dedans ou à côté"
                    )

        corps_regles, tracabilite = set(), set()
        for bloc_titre, bloc_texte in sections(texte, "###"):
            if "traçabilité" in bloc_titre.lower():
                tracabilite.update(RE_REGLE.findall(bloc_texte))
            else:
                corps_regles.update(RE_REGLE_DECLAREE.findall(bloc_texte))
        toutes_regles |= corps_regles

        for regle in sorted(corps_regles - tracabilite):
            erreurs.append(
                f"{rel} — « {titre} » : {regle} sans ligne de traçabilité. "
                "Une règle non sourcée est une invention jusqu'à preuve du contraire"
            )

    index = next(
        (x for t, x in sections(corps) if "index inverse" in t.lower()), None
    )
    if index is None:
        if toutes_regles:
            erreurs.append(f"{rel} — index inverse absent, alors que le corps porte des règles")
    else:
        indexees = set(RE_REGLE.findall(index))
        manquantes = toutes_regles - indexees
        if manquantes:
            erreurs.append(
                f"{rel} — index inverse incomplet : {len(manquantes)} règle(s) du corps "
                f"absente(s) ({', '.join(sorted(manquantes)[:5])}). L'index se génère, "
                "il ne s'édite pas — un écart est un défaut, pas un arrondi"
            )


def check_blocage_sfg(run, docs, erreurs):
    """Une contradiction non résolue dans la SFD bloque la SFG."""
    ouvertes = []
    for path in sorted((run / "challenges").glob("*.y*ml")):
        try:
            doc = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        except yaml.YAMLError:
            continue
        if doc.get("outcome") == "contradicted" and not doc.get("resolved_at"):
            ouvertes.append(doc.get("id", path.name))
    if ouvertes and any(k == "SFG" for _, k, _ in docs):
        erreurs.append(
            f"{run}/sfg — contradiction non résolue ({', '.join(ouvertes)}) : la SFG "
            "ne se produit pas. Une contradiction laissée en SFD devient une promesse "
            "fausse faite à l'utilisateur, et son lecteur n'a aucun moyen de la "
            "détecter. Elle ne dégrade pas la SFG, elle la bloque"
        )


# --------------------------------------------------------------------- main

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("run", type=pathlib.Path)
    args = ap.parse_args()

    erreurs: list[str] = []
    docs: list[tuple[pathlib.Path, str, dict]] = []

    for dossier, kind in (("std", "STD"), ("sfd", "SFD"), ("sfg", "SFG")):
        for path in sorted((args.run / dossier).glob("*.md")):
            rel = path.relative_to(args.run)
            fm, corps, _ = lire(path)

            check_d16(rel, corps, erreurs)
            if not check_frontmatter(rel, fm, erreurs):
                continue

            declare = str(fm.get("type", "")).upper()
            if declare and declare != kind:
                erreurs.append(
                    f"{rel} — type « {declare} » dans le dossier {dossier}/. "
                    "Le dossier et le frontmatter doivent dire la même chose"
                )
            docs.append((path, kind, fm))

            parents = check_cascade(rel, kind, fm, erreurs)
            check_diagrammes(rel, corps, erreurs)
            if kind == "STD":
                check_std(rel, corps, erreurs)
            elif kind == "SFD":
                check_sfd(rel, corps, parents, erreurs)
            else:
                check_sfg(rel, corps, erreurs)

    check_blocage_sfg(args.run, [(p, k, f) for p, k, f in docs], erreurs)

    if not docs and not erreurs:
        print("aucun document de corpus trouvé (std/, sfd/, sfg/)")
        return 0

    if erreurs:
        print(f"✗ {len(erreurs)} erreur(s) sur {len(docs)} document(s)\n")
        for e in erreurs:
            print(f"  {e}")
        return 1

    print(f"✓ {len(docs)} document(s) de corpus conformes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
