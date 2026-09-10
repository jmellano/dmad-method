#!/usr/bin/env python3
"""Rend un diagramme depuis un sous-graphe et une question.

La règle R3 dit : « généré depuis le graphe, jamais rédigé ». Tant que le rendu
n'existe pas, elle est un vœu pieux — un diagramme écrit à la main peut
contredire le texte qui l'entoure, son badge de confiance est recopié plutôt
que calculé, et **personne ne compte ses nœuds**, ce qui rend D15 inopérant :
on aurait paramétré un seuil que rien ne mesure.

Les agents décrivent un plan ; cet outil rend. Il **refuse** de rendre au-delà
du seuil, parce que la règle est de découper, pas de simplifier.

    python3 tools/diagram-engine.py <plan.yaml> [--thresholds scope.yaml] [--out dossier]
    python3 tools/diagram-engine.py --all <dossier-run>
"""
import argparse
import pathlib
import sys

try:
    import yaml
except ImportError:  # pragma: no cover
    sys.exit("dépendance manquante : pip install pyyaml")

SEUILS_DEFAUT = {
    "max_nodes": 12,
    "max_edges": 15,
    "max_mccabe": 10,
    "max_sequence_participants": 12,
}

BADGES = {"V": "vérifié", "C": "corroboré", "I": "inféré", "H": "hypothèse"}


# --------------------------------------------------------------- rendus

def rendre_flowchart(plan):
    sens = plan.get("direction", "TD")
    lignes = [f"flowchart {sens}"]
    formes = {"process": ("[", "]"), "decision": ("{", "}"), "data": ("[(", ")]"),
              "external": ("[[", "]]"), "terminal": ("((", "))")}
    for n in plan["nodes"]:
        ouvre, ferme = formes.get(n.get("shape", "process"), ("[", "]"))
        lignes.append(f'  {n["id"]}{ouvre}"{n["label"]}"{ferme}')
    for e in plan["edges"]:
        fleche = "-.->" if e.get("style") == "dashed" else "-->"
        label = f'|"{e["label"]}"|' if e.get("label") else ""
        lignes.append(f'  {e["from"]} {fleche}{label} {e["to"]}')
    return "\n".join(lignes)


def rendre_sequence(plan):
    lignes = ["sequenceDiagram", "  autonumber"]
    for p in plan["participants"]:
        lignes.append(f'  participant {p["id"]} as {p["label"]}')
    profondeur = 0
    for etape in plan["steps"]:
        pad = "  " + "  " * profondeur
        if "msg" in etape:
            m = etape["msg"]
            fleche = "-->>" if m.get("reply") else "->>"
            lignes.append(f'{pad}{m["from"]}{fleche}{m["to"]}: {m["label"]}')
        elif "loop" in etape:
            lignes.append(f'{pad}loop {etape["loop"]}'); profondeur += 1
        elif "alt" in etape:
            lignes.append(f'{pad}alt {etape["alt"]}'); profondeur += 1
        elif "else" in etape:
            lignes.append(f'{"  " + "  " * (profondeur - 1)}else {etape["else"]}')
        elif "end" in etape:
            profondeur -= 1
            lignes.append(f'{"  " + "  " * profondeur}end')
        elif "note" in etape:
            n = etape["note"]
            lignes.append(f'{pad}Note over {n["over"]}: {n["text"]}')
    return "\n".join(lignes)


def rendre_state(plan):
    lignes = ["stateDiagram-v2"]
    for s in plan.get("states", []):
        if s.get("initial"):
            lignes.append(f'  [*] --> {s["id"]}')
    for t in plan["transitions"]:
        lignes.append(f'  {t["from"]} --> {t["to"]}: {t.get("label", "")}'.rstrip(": "))
    for s in plan.get("states", []):
        if s.get("final"):
            lignes.append(f'  {s["id"]} --> [*]')
    return "\n".join(lignes)


def rendre_er(plan):
    lignes = ["erDiagram"]
    for r in plan["relations"]:
        lignes.append(f'  {r["from"]} {r["cardinality"]} {r["to"]} : "{r["label"]}"')
    return "\n".join(lignes)


RENDUS = {"flowchart": rendre_flowchart, "sequence": rendre_sequence,
          "state": rendre_state, "er": rendre_er}


# --------------------------------------------------------------- métriques

def mesurer(plan):
    kind = plan["kind"]
    if kind == "sequence":
        n = len(plan["participants"])
        e = sum(1 for s in plan["steps"] if "msg" in s)
        branches = sum(1 for s in plan["steps"] if "alt" in s or "loop" in s or "else" in s)
        return {"noeuds": n, "aretes": e, "mccabe": branches + 1, "participants": n}
    if kind == "flowchart":
        n, e = len(plan["nodes"]), len(plan["edges"])
        return {"noeuds": n, "aretes": e, "mccabe": max(1, e - n + 2), "participants": 0}
    if kind == "state":
        n, e = len(plan.get("states", [])), len(plan["transitions"])
        return {"noeuds": n, "aretes": e, "mccabe": max(1, e - n + 2), "participants": 0}
    n = len({r["from"] for r in plan["relations"]} | {r["to"] for r in plan["relations"]})
    return {"noeuds": n, "aretes": len(plan["relations"]), "mccabe": 1, "participants": 0}


def depassements(m, seuils, kind):
    out = []
    if m["noeuds"] > seuils["max_nodes"]:
        out.append(f'{m["noeuds"]} nœuds > {seuils["max_nodes"]}')
    if m["aretes"] > seuils["max_edges"]:
        out.append(f'{m["aretes"]} arêtes > {seuils["max_edges"]}')
    if m["mccabe"] > seuils["max_mccabe"]:
        out.append(f'McCabe {m["mccabe"]} > {seuils["max_mccabe"]}')
    if kind == "sequence" and m["participants"] > seuils["max_sequence_participants"]:
        out.append(f'{m["participants"]} participants > {seuils["max_sequence_participants"]}')
    return out


# --------------------------------------------------------------- figure

def rendre_figure(plan, seuils):
    """Rend la figure complète : question, badge, marqueur, bloc.

    La question est AU-DESSUS du diagramme parce que c'est là qu'un lecteur la
    cherche, et le marqueur permet de détecter un diagramme réécrit à la main.
    """
    kind = plan["kind"]
    if kind not in RENDUS:
        raise ValueError(f'type inconnu : {kind}')
    if not plan.get("question", "").strip().endswith("?"):
        raise ValueError("R1 : pas de question formulable, pas de diagramme")

    m = mesurer(plan)
    trop = depassements(m, seuils, kind)
    if trop:
        raise ValueError(
            "D15 : seuils dépassés — " + " · ".join(trop) + ".\n"
            "    Au-delà du seuil on ne simplifie pas : on DÉCOUPE en plusieurs "
            "diagrammes, chacun avec sa propre question."
        )

    conf = plan.get("confidence", "I")
    badge = f'**Confiance : {conf} — {BADGES.get(conf, "?")}**'
    caveats = f' · {plan["caveats"]}' if plan.get("caveats") else ""

    return (
        f'> **Question :** {plan["question"]}\n'
        f'> {badge}{caveats}\n'
        f'\n'
        f'<!-- diagram: {plan["id"]} · N={m["noeuds"]} E={m["aretes"]} McCabe={m["mccabe"]} -->\n'
        f'```mermaid\n{RENDUS[kind](plan)}\n```\n'
    ), m


def charger_seuils(chemin):
    if chemin and pathlib.Path(chemin).exists():
        scope = yaml.safe_load(pathlib.Path(chemin).read_text(encoding="utf-8")) or {}
        return {**SEUILS_DEFAUT, **(scope.get("diagram_thresholds") or {})}
    return dict(SEUILS_DEFAUT)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("plan", nargs="?", type=pathlib.Path)
    ap.add_argument("--all", type=pathlib.Path, metavar="RUN",
                    help="rend tous les plans de <run>/diagrams/ vers <run>/diagrams/*.figure.md")
    ap.add_argument("--thresholds", type=pathlib.Path, help="scope.yaml portant diagram_thresholds")
    ap.add_argument("--out", type=pathlib.Path)
    args = ap.parse_args()

    if args.all:
        seuils = charger_seuils(args.thresholds or args.all / "scope.yaml")
        plans = sorted((args.all / "diagrams").glob("*.y*ml"))
        if not plans:
            print("aucun plan de diagramme")
            return 0
        erreurs = []
        ignores = []
        for chemin in plans:
            plan = yaml.safe_load(chemin.read_text(encoding="utf-8"))
            # Le journal des refus est un livrable légitime et vit au même endroit :
            # un fichier sans `kind` n'est pas un plan, il n'est pas une erreur.
            if not isinstance(plan, dict) or "kind" not in plan:
                ignores.append(chemin.name)
                continue
            try:
                figure, m = rendre_figure(plan, seuils)
            except ValueError as e:
                erreurs.append(f"{chemin.name} — {e}")
                continue
            cible = chemin.with_suffix(".figure.txt")
            cible.write_text(figure, encoding="utf-8")
            print(f'  ✓ {plan["id"]:<16} N={m["noeuds"]:<3} E={m["aretes"]:<3} '
                  f'McCabe={m["mccabe"]:<3} → {cible.name}')
        if ignores:
            print(f"  ({len(ignores)} fichier(s) sans `kind` ignoré(s) : {', '.join(ignores)})")
        if erreurs:
            print(f"\n✗ {len(erreurs)} plan(s) refusé(s)\n")
            for e in erreurs:
                print(f"  {e}")
            return 1
        print(f"\n✓ {len(plans)} diagramme(s) rendu(s)")
        return 0

    if not args.plan:
        ap.error("donner un plan, ou --all <run>")
    seuils = charger_seuils(args.thresholds)
    plan = yaml.safe_load(args.plan.read_text(encoding="utf-8"))
    try:
        figure, _ = rendre_figure(plan, seuils)
    except ValueError as e:
        print(f"✗ {args.plan} — {e}")
        return 1
    if args.out:
        args.out.write_text(figure, encoding="utf-8")
    else:
        print(figure, end="")
    return 0


if __name__ == "__main__":
    sys.exit(main())
