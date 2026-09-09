#!/usr/bin/env python3
"""Valide les artefacts d'un run DMAD contre les schémas.

Ce n'est pas un utilitaire de confort : c'est le point d'application mécanique
des principes du manifeste. Une claim sans preuve, une exclusion sans
justification ou une question sans destinataire sont refusées ici, pas
signalées en relecture.

    python3 tools/validate.py <dossier-run> [--schemas dmad/schemas]
"""
import argparse
import json
import pathlib
import re
import sys

try:
    import yaml
    from jsonschema import Draft202012Validator
except ImportError:  # pragma: no cover
    sys.exit("dépendances manquantes : pip install pyyaml jsonschema")

# Le nom du dossier détermine le schéma appliqué.
ROUTES = {
    "claims": "claim.schema.json",
    "challenges": "challenge.schema.json",
    "open-questions": "open-question.schema.json",
    "capabilities": "capability.schema.json",
    "contracts": "external-contract.schema.json",
    "business-objects": "business-object.schema.json",
    "documents": "document.schema.json",
}
SINGLE_FILES = {"scope.yaml": "scope.schema.json"}

CONFIDENCE_ORDER = {"H": 0, "I": 1, "C": 2, "V": 3}

# Claims dont le contenu résulte d'une interprétation : atteindre V exige une
# preuve exécutée (test vert) ou déclarative (schéma, migration, runtime).
# Les autres types sont des constats d'outil et se prouvent par l'outil lui-même.
INTERPRETIVE_TYPES = {"BusinessRule", "UseCase", "Invariant", "StateMachine", "Actor"}

# D18 : la confiance d'un contrat sortant est DÉRIVÉE du barreau de résolution.
# Un code faux ressemble exactement à un code vrai ; seule sa source les distingue.
RUNG_CONFIDENCE = {1: "V", 2: "C", 3: "I"}

# D20 : chaque document du corpus a son unité, et une seule.
DOCUMENT_UNIT = {"STD": "entrypoint", "SFD": "business_object_tree", "SFG": "use_case"}


def load(path: pathlib.Path):
    text = path.read_text(encoding="utf-8")
    return yaml.safe_load(text) if path.suffix in (".yaml", ".yml") else json.loads(text)


def check_cross_rules(claims, errors):
    """Règles inter-documents que le JSON Schema ne peut pas exprimer."""
    for path, claim in claims:
        # P5 : l'intention ne peut sortir de H que par une validation humaine tracée.
        intent = claim.get("intent") or {}
        if intent.get("confidence") == "C" and not intent.get("validated_by"):
            errors.append(f"{path}: intent en C sans validated_by (principe P5)")

        # Seul test-forger promeut, et seulement en V.
        promoter = claim.get("promoted_by")
        if promoter and promoter != "test-forger":
            errors.append(f"{path}: promoted_by={promoter} — seul test-forger peut promouvoir")
        if promoter and claim.get("confidence") != "V":
            errors.append(f"{path}: promoted_by renseigné mais confidence != V")

        # V exige une preuve exécutée ou déclarative — pour les claims INTERPRÉTATIVES.
        # Une lecture de code par le modèle ne suffit jamais à les prouver.
        # Les claims purement structurelles (Risk, Term) sont établies par un outil
        # déterministe : un git log ou un LSP les prouve, il n'y a rien à interpréter.
        if claim.get("confidence") == "V" and claim["type"] in INTERPRETIVE_TYPES:
            kinds = {e.get("kind") for e in claim.get("evidence", [])}
            outcomes = {e.get("outcome") for e in claim.get("evidence", [])}
            if not (kinds & {"schema", "migration", "runtime"} or "passing" in outcomes):
                errors.append(
                    f"{path}: confidence V sur une claim {claim['type']} sans preuve "
                    "exécutée ni fait déclaratif (test passing, schema, migration ou "
                    "runtime requis)"
                )
        if claim.get("confidence") == "V" and claim["type"] not in INTERPRETIVE_TYPES:
            if not any(e.get("tool") for e in claim.get("evidence", [])):
                errors.append(
                    f"{path}: confidence V sur une claim structurelle sans evidence.tool "
                    "— un fait mécanique doit nommer l'outil qui l'a produit"
                )

        # Un plafond de capability dégradée ne se contourne pas.
        ceiling = claim.get("confidence_ceiling_applied")
        if ceiling and CONFIDENCE_ORDER[claim["confidence"]] > CONFIDENCE_ORDER[ceiling]:
            errors.append(
                f"{path}: confidence {claim['confidence']} dépasse le plafond {ceiling}"
            )

        # Une règle conditionnée à un flag doit le dire dans son énoncé.
        if claim.get("conditional_on"):
            key = claim["conditional_on"].get("key", "")
            if key and key not in claim.get("statement", ""):
                errors.append(
                    f"{path}: conditional_on={key} absent du statement — "
                    "la règle serait lue comme inconditionnelle"
                )


def looks_like_code_identifier(name: str) -> bool:
    """Un nom de business object doit dire ce que l'objet EST pour le métier.

    « traiterLigne » nomme la méthode dont l'objet a été tiré, pas l'objet — et
    c'est la règle qu'un agent pressé enfreint en premier.
    """
    if "(" in name or ")" in name:
        return True
    if " " in name:                      # un nom composé n'est pas un identifiant
        return False
    if name[:1].islower():               # traiterLigne
        return True
    return bool(re.search(r"[a-z][A-Z]", name))   # DocumentFacturation


def check_contracts(contracts, errors):
    """D18 — un contrat sortant porte sa source et la version où il l'a lue."""
    for path, c in contracts:
        rung = c.get("resolution_rung")
        conf = c.get("confidence")

        if rung in (1, 2):
            for field in ("artifact", "artifact_version"):
                if not c.get(field):
                    errors.append(
                        f"{path}: D18 — {field} manquant au barreau {rung}. "
                        "L'artefact lu est figé à la version que le module consomme ; "
                        "sans elle la preuve devient fausse au prochain bump, en silence"
                    )

        if rung in RUNG_CONFIDENCE:
            if not c.get("code"):
                errors.append(f"{path}: D18 — barreau {rung} sans code de contrat")
            attendu = RUNG_CONFIDENCE[rung]
            if conf and conf != attendu:
                errors.append(
                    f"{path}: D18 — confidence {conf} au barreau {rung}, attendu {attendu}. "
                    "La confiance d'un contrat est dérivée de sa source, pas choisie"
                )
        elif rung == 4:
            if conf:
                errors.append(
                    f"{path}: D18 — confidence {conf} au barreau 4. Un placeholder "
                    "n'affirme rien, et c'est sa vertu"
                )
            if not c.get("open_questions"):
                errors.append(
                    f"{path}: D18 — contrat non résolu sans question ouverte. "
                    "Un placeholder visible se corrige ; un placeholder muet se propage"
                )


def check_business_objects(objects, errors):
    """Le nommage et la cohérence de l'arbre."""
    known = {o.get("id") for _, o in objects}
    for path, bo in objects:
        name = bo.get("functional_name", "")
        if looks_like_code_identifier(name):
            errors.append(
                f"{path}: functional_name « {name} » ressemble à un identifiant de code. "
                "Un business object se nomme par son sens fonctionnel, jamais par la "
                "méthode dont il est issu"
            )

        subs = bo.get("sub_objects") or []
        for sub in subs:
            if sub not in known:
                errors.append(f"{path}: sub_objects référence {sub}, qui n'existe pas")

        depth = bo.get("recursive_depth")
        if depth == 0 and subs:
            errors.append(
                f"{path}: recursive_depth 0 avec des sous-objets — "
                "un objet de profondeur 0 n'invoque que des feuilles externes"
            )
        if depth and depth > 0 and not subs:
            errors.append(
                f"{path}: recursive_depth {depth} sans sous-objet — "
                "la profondeur est celle de l'arbre, pas une étiquette libre"
            )


def check_documents(documents, errors):
    """D17, D19, D20 — la cascade tient ou elle ne tient pas."""
    by_id = {d.get("id"): d for _, d in documents}
    for path, doc in documents:
        kind = doc.get("kind")

        attendu = DOCUMENT_UNIT.get(kind)
        if attendu and doc.get("unit") != attendu:
            errors.append(
                f"{path}: D20 — une {kind} a pour unité « {attendu} », "
                f"pas « {doc.get('unit')} »"
            )

        parents = doc.get("derives_from") or []
        if kind in ("SFD", "SFG") and not parents:
            errors.append(
                f"{path}: D17 — une {kind} sans derives_from. Chaque document est "
                "l'abstraction du précédent ; sans ancrage, c'est une lecture "
                "indépendante, et deux lectures indépendantes divergent"
            )
        if kind == "STD" and parents:
            errors.append(
                f"{path}: D17 — une STD ne dérive d'aucun document : elle lit le "
                "graphe et les claims"
            )

        for parent in parents:
            amont = by_id.get(parent)
            if amont is None:
                continue          # document hors du run validé : hors de portée ici
            if not amont.get("frozen_at"):
                errors.append(
                    f"{path}: D19 — dérive de {parent}, qui n'est pas figé. "
                    "Le cycle suivant ne démarre pas sur un document non figé"
                )


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("run", type=pathlib.Path)
    ap.add_argument("--schemas", type=pathlib.Path, default=pathlib.Path(__file__).parent.parent / "schemas")
    args = ap.parse_args()

    validators = {
        name: Draft202012Validator(json.loads((args.schemas / name).read_text()))
        for name in set(ROUTES.values()) | set(SINGLE_FILES.values())
    }

    errors: list[str] = []
    checked = 0
    collected: dict[str, list[tuple[str, dict]]] = {folder: [] for folder in ROUTES}

    for folder, schema in ROUTES.items():
        for path in sorted((args.run / folder).glob("*.y*ml")):
            checked += 1
            doc = load(path)
            for err in validators[schema].iter_errors(doc):
                loc = "/".join(str(p) for p in err.path) or "<racine>"
                errors.append(f"{path}: {loc}: {err.message}")
            collected[folder].append((str(path), doc))

    claims = collected["claims"]

    for filename, schema in SINGLE_FILES.items():
        path = args.run / filename
        if path.exists():
            checked += 1
            for err in validators[schema].iter_errors(load(path)):
                loc = "/".join(str(p) for p in err.path) or "<racine>"
                errors.append(f"{path}: {loc}: {err.message}")

    check_cross_rules(claims, errors)
    check_contracts(collected["contracts"], errors)
    check_business_objects(collected["business-objects"], errors)
    check_documents(collected["documents"], errors)

    if errors:
        print(f"✗ {len(errors)} erreur(s) sur {checked} artefact(s)\n")
        for e in errors:
            print(f"  {e}")
        return 1

    print(f"✓ {checked} artefact(s) valides")
    return 0


if __name__ == "__main__":
    sys.exit(main())
