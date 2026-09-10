#!/usr/bin/env python3
"""Vérifie les invariants du corpus DMAD sur les documents eux-mêmes.

`validate.py` valide des artefacts structurés contre des schémas. Cet outil-ci
valide des **documents Markdown** : la STD, la SFD et la SFG. Les deux échouent
pour des raisons différentes, et mélanger « ta claim viole le schéma » avec
« ta SFD contient un bloc SQL » n'aiderait personne.

Chaque message nomme la décision qu'il applique. Ce n'est pas de la cosmétique :
un message qui ne dit pas quelle règle il fait respecter se fait contourner,
puis supprimer, au premier agacement — et la règle disparaît avec lui.

Les documents contrôlés sont ceux que déclarent les `plan-*.yaml` du run : le
bundle est la source, le document composé en est la dérivation (D26).

    python3 tools/check-corpus.py <dossier-run>
"""
import argparse
import importlib.util
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

# D20, révisé par D25 — chaque document a son unité, et une seule.
# Un processus a rarement un seul point d'entrée : la STD et la SFD en documentent
# un, et cataloguent ses points d'entrée. La SFG documente un domaine.
UNITE_ATTENDUE = {"STD": "process", "SFD": "process", "SFG": "domain"}

# Le plan de niveau 1 est imposé par le gabarit et déclaré dans plan-*.yaml.
# Une section sans objet ne se supprime pas : elle porte son constat d'absence
# et son périmètre (D26).

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

# Notation Mermaid → nom de la légende qui doit l'accompagner. Une notation
# employée sans sa légende laisse un lecteur devant un dessin qu'il interprète ;
# une légende sans son diagramme survit au retrait du dernier qui l'employait.
NOTATIONS = {
    "flowchart": "activité", "graph": "activité",
    "sequencediagram": "séquence",
    "statediagram": "état-transition", "statediagram-v2": "état-transition",
    "erdiagram": "entité-relation",
    "classdiagram": "classe",
}
RE_MARQUEUR = re.compile(r"^<!-- diagram: ([A-Z0-9-]+) ·[^>]*-->$", re.M)
RE_BLOC_MERMAID = re.compile(r"^```mermaid\n(.*?)^```$", re.M | re.S)


def charger_moteur():
    """Le moteur de rendu, chargé par chemin — son nom de fichier porte un tiret."""
    chemin = pathlib.Path(__file__).with_name("diagram-engine.py")
    if not chemin.exists():
        return None
    spec = importlib.util.spec_from_file_location("diagram_engine", chemin)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod
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
    """Découpe un corps en (titre, texte) sur les titres du niveau demandé.

    Une section s'arrête au prochain titre de niveau ÉGAL OU SUPÉRIEUR — sinon
    un cas d'usage avale tout ce qui le suit, et les contrôles portent sur le
    mauvais texte.
    """
    n = len(niveau)
    tous = [(m.start(), len(m.group(1)), m.group(2).strip())
            for m in re.finditer(r"^(#{1,6}) +(.+)$", corps, re.M)]
    out = []
    for i, (debut, lvl, titre) in enumerate(tous):
        if lvl != n:
            continue
        fin = len(corps)
        for suivant, lvl2, _ in tous[i + 1:]:
            if lvl2 <= n:
                fin = suivant
                break
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


def check_gabarit(rel, corps, erreurs):
    """Un gabarit livré à moitié rempli. Un seul contrôle, donc un seul message."""
    trouves = []
    for motif, quoi in ((r"\[gabarit\]", "consigne de rédaction"),
                        (r"\{\{[^}\n]{0,80}\}\}", "placeholder")):
        m = re.search(motif, corps)
        if m:
            ligne = corps[:m.start()].count("\n") + 1
            trouves.append(f"{quoi} l.{ligne} (`{m.group(0)[:40]}`)")
    if trouves:
        erreurs.append(
            f"{rel} — marqueur de gabarit résiduel : {' · '.join(trouves)}. "
            "Le marqueur se supprime au fur et à mesure que la section est écrite ; "
            "celui-ci a survécu jusqu'à la livraison"
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


def check_diagrammes(rel, corps, erreurs, run, moteur, seuils):
    """R1 et R3 — une question, et un rendu depuis le graphe plutôt qu'une main."""
    dossier_plans = run / "diagrams"

    for m in re.finditer(r"^```mermaid\s*$", corps, re.M):
        amont = corps[:m.start()].splitlines()
        ligne = len(amont) + 1
        contexte = amont[-8:]

        if not any("?" in l for l in contexte):
            erreurs.append(
                f"{rel}:{ligne} — R1 : diagramme sans question. La question "
                "s'affiche au-dessus du diagramme ; un diagramme qui ne répond à "
                "rien occupe de la place, vieillit, et fait douter du reste"
            )

        marqueur = next((RE_MARQUEUR.match(l) for l in reversed(contexte)
                         if RE_MARQUEUR.match(l)), None)
        if marqueur is None:
            erreurs.append(
                f"{rel}:{ligne} — R3 : diagramme sans marqueur de rendu, donc écrit "
                "à la main. Les agents décrivent un sous-graphe et une intention, le "
                "moteur rend — c'est ce qui rend impossible qu'un diagramme contredise "
                "le texte, et c'est ce qui fait que ses nœuds sont comptés"
            )
            continue

        if not dossier_plans.is_dir():
            continue
        plan_id = marqueur.group(1)
        plan_path = next((p for p in (dossier_plans / f"{plan_id}.yaml",
                                      dossier_plans / f"{plan_id}.yml") if p.exists()), None)
        if plan_path is None:
            erreurs.append(
                f"{rel}:{ligne} — R3 : le marqueur cite {plan_id}, dont le plan est "
                "introuvable. Un diagramme sans plan ne peut pas être re-rendu, donc "
                "pas vérifié"
            )
            continue

        if moteur is None:
            continue
        try:
            plan = yaml.safe_load(plan_path.read_text(encoding="utf-8"))
            attendu, _ = moteur.rendre_figure(plan, seuils)
        except (ValueError, yaml.YAMLError) as e:
            erreurs.append(f"{rel}:{ligne} — R3 : le plan {plan_id} ne se rend pas : {e}")
            continue

        bloc = RE_BLOC_MERMAID.search(corps, m.start())
        attendu_bloc = RE_BLOC_MERMAID.search(attendu)
        if bloc and attendu_bloc and bloc.group(1).strip() != attendu_bloc.group(1).strip():
            erreurs.append(
                f"{rel}:{ligne} — R3 : le diagramme {plan_id} diverge de son plan. "
                "Il a été retouché à la main après rendu — et il peut désormais "
                "contredire le graphe dont il est censé sortir"
            )


def check_annexes(rel, corps, erreurs):
    """Contrôles 6 et 7 — les légendes des notations, et les compteurs annoncés.

    Ils ne s'appliquent qu'aux documents qui portent un chapitre d'annexes : une
    SFG cadre un arbitrage métier, pas une analyse technique, et n'en a pas.
    """
    annexes = next((x for t_, x in sections(corps) if "annexe" in t_.lower()), None)
    if annexes is None:
        return

    employees = set()
    for m in re.finditer(r"^```mermaid\n\s*([A-Za-z-]+)", corps, re.M):
        n = NOTATIONS.get(m.group(1).lower())
        if n:
            employees.add(n)

    declarees = set()
    for titre, _ in sections(annexes, "###"):
        for nom in set(NOTATIONS.values()):
            if nom in titre.lower():
                declarees.add(nom)

    for manque in sorted(employees - declarees):
        erreurs.append(
            f"{rel} — notation « {manque} » employée sans sa légende. Un lecteur "
            "devant un dessin dont la convention n'est pas écrite l'interprète"
        )
    for orpheline in sorted(declarees - employees):
        erreurs.append(
            f"{rel} — légende « {orpheline} » orpheline : plus aucun diagramme ne "
            "l'emploie. Elle a survécu au retrait du dernier qui s'en servait"
        )

    chapeau = re.split(r"^###", annexes, maxsplit=1, flags=re.M)[0]
    reels = {"diagramme": len(re.findall(r"^```mermaid\s*$", corps, re.M)),
             "légende": len(declarees)}
    for mot, reel in reels.items():
        m = re.search(rf"(\d+)\s+{mot}", chapeau, re.I)
        if m and int(m.group(1)) != reel:
            erreurs.append(
                f"{rel} — le chapeau des annexes annonce {m.group(1)} {mot}(s), "
                f"il y en a {reel}. Un compteur faux se recopie d'une version à l'autre"
            )


def check_plan(rel, corps, plan, erreurs):
    """Le plan de niveau 1 est imposé : mêmes numéros, mêmes titres, même ordre."""
    attendu = [(s["number"], s["title"]) for s in plan["sections"]
               if s["number"] and "." not in s["number"]]
    trouve = []
    for titre, _ in sections(corps):
        m = re.match(r"^(\d+)\.? +(.+)$", titre.strip())
        if m:
            trouve.append((m.group(1), m.group(2).strip()))

    manquants = [n for n, _ in attendu if n not in {x for x, _ in trouve}]
    if manquants:
        erreurs.append(
            f"{rel} — chapitres manquants : {', '.join(manquants)}. Une section sans "
            "objet ne se supprime pas : elle porte son constat d'absence et son "
            "périmètre. Une section absente se lit « oubliée » et pousse le lecteur "
            "à chercher lui-même"
        )
    # L'ordre ne se contrôle que si rien ne manque : sinon un chapitre absent
    # produirait deux erreurs pour un seul défaut.
    if not manquants and [n for n, _ in trouve] != [n for n, _ in attendu[:len(trouve)]]:
        erreurs.append(
            f"{rel} — l'ordre des chapitres s'écarte du plan. Le plan de niveau 1 est "
            "ce qui rend la décomposition en concepts possible : un document qui s'en "
            "écarte se décompose mal"
        )
    for (na, ta), (nt, tt) in zip(attendu, trouve):
        if na == nt and ta.lower() != tt.lower():
            erreurs.append(f"{rel} — § {na} : titre « {tt} », le plan dit « {ta} »")


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
    niveau_cu = "###"
    cas = [(t, x) for t, x in sections(corps, niveau_cu) if "CU-" in t]
    if not cas:
        niveau_cu = "##"
        cas = [(t, x) for t, x in sections(corps, niveau_cu) if "CU-" in t]
    sous = "#" * (len(niveau_cu) + 1)
    if not cas:
        return

    toutes_regles = set()

    for titre, texte in cas:
        blocs = [b.lower() for b, _ in sections(texte, sous)]
        for cle, nom in SFG_BLOCS:
            if not any(cle in b for b in blocs):
                erreurs.append(
                    f"{rel} — « {titre} » : bloc « {nom} » manquant. "
                    "Sept blocs par cas d'usage, sans exception"
                )

        for bloc_titre, bloc_texte in sections(texte, sous):
            if "n'est pas couvert" in bloc_titre.lower():
                contenu = re.sub(r"^#+ .*$", "", bloc_texte, flags=re.M).strip()
                if not contenu:
                    erreurs.append(
                        f"{rel} — « {titre} » : « Ce qui n'est pas couvert » est vide. "
                        "Un cas d'usage dont la frontière n'est pas écrite ne peut "
                        "être l'unité d'évolution de rien : personne ne saura si une "
                        "demande tombe dedans ou à côté"
                    )

        corps_regles, tracabilite = set(), set()
        for bloc_titre, bloc_texte in sections(texte, sous):
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
    moteur = charger_moteur()
    seuils = moteur.charger_seuils(args.run / "scope.yaml") if moteur else {}

    plans = sorted(args.run.glob("plan-*.y*ml"))
    if not plans:
        print("aucun plan de document (plan-*.yaml) — rien à contrôler")
        return 0

    for chemin_plan in plans:
        plan = yaml.safe_load(chemin_plan.read_text(encoding="utf-8"))
        kind = plan["kind"]
        path = args.run / plan["output"]
        if not path.exists():
            erreurs.append(
                f'{plan["output"]} — déclaré par {chemin_plan.name} mais absent. '
                "Composer avec okf-compose.py avant de contrôler"
            )
            continue

        rel = path.relative_to(args.run)
        fm, corps, _ = lire(path)

        check_d16(rel, corps, erreurs)
        check_gabarit(rel, corps, erreurs)
        if not check_frontmatter(rel, fm, erreurs):
            continue
        declare = str(fm.get("type", "")).upper()
        if declare and declare != kind:
            erreurs.append(f"{rel} — type « {declare} », le plan dit « {kind} »")
        docs.append((path, kind, fm))

        parents = check_cascade(rel, kind, fm, erreurs)
        check_diagrammes(rel, corps, erreurs, args.run, moteur, seuils)
        check_plan(rel, corps, plan, erreurs)
        check_annexes(rel, corps, erreurs)
        if kind == "SFD":
            check_sfd(rel, corps, parents, erreurs)
        elif kind == "SFG":
            check_sfg(rel, corps, erreurs)

    check_blocage_sfg(args.run, [(p, k, f) for p, k, f in docs], erreurs)

    if erreurs:
        print(f"✗ {len(erreurs)} erreur(s) sur {len(docs)} document(s)\n")
        for e in erreurs:
            print(f"  {e}")
        return 1

    print(f"✓ {len(docs)} document(s) de corpus conformes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
