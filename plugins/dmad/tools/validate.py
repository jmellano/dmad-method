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
import sys

try:
    import yaml
    from jsonschema import Draft202012Validator
except ImportError:  # pragma: no cover
    sys.exit("dépendances manquantes : pip install pyyaml jsonschema")

# Le nom du dossier détermine le schéma appliqué.
# Le routage se fait par nom de dossier. `07-livrables.md` place ces dossiers
# sous `preuves/` ; les runs les créent parfois à la racine. Les deux sont
# acceptés — sinon les artefacts sont ignorés SANS ERREUR, ce qui donne un faux
# « 1 artefact validé » et masque des dizaines de fichiers non contrôlés.
_KINDS = {
    "claims": "claim.schema.json",
    "challenges": "challenge.schema.json",
    "open-questions": "open-question.schema.json",
    "capabilities": "capability.schema.json",
}
ROUTES = {**_KINDS, **{f"preuves/{k}": v for k, v in _KINDS.items()}}
SINGLE_FILES = {"scope.yaml": "scope.schema.json"}

CONFIDENCE_ORDER = {"H": 0, "I": 1, "C": 2, "V": 3}

# Claims dont le contenu résulte d'une interprétation : atteindre V exige une
# preuve exécutée (test vert) ou déclarative (schéma, migration, runtime).
# Les autres types sont des constats d'outil et se prouvent par l'outil lui-même.
INTERPRETIVE_TYPES = {"BusinessRule", "UseCase", "Invariant", "StateMachine", "Actor"}


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
    claims: list[tuple[str, dict]] = []

    for folder, schema in ROUTES.items():
        for path in sorted((args.run / folder).glob("*.y*ml")):
            checked += 1
            doc = load(path)
            for err in validators[schema].iter_errors(doc):
                loc = "/".join(str(p) for p in err.path) or "<racine>"
                errors.append(f"{path}: {loc}: {err.message}")
            if folder == "claims":
                claims.append((str(path), doc))

    for filename, schema in SINGLE_FILES.items():
        path = args.run / filename
        if path.exists():
            checked += 1
            for err in validators[schema].iter_errors(load(path)):
                loc = "/".join(str(p) for p in err.path) or "<racine>"
                errors.append(f"{path}: {loc}: {err.message}")

    check_cross_rules(claims, errors)

    # Un run sans aucun artefact reconnu est presque toujours une erreur
    # d'arborescence, pas un run vide. Le signaler plutôt qu'afficher « 0 ».
    if checked == 0:
        print(
            "✗ aucun artefact trouvé — vérifier l'arborescence du run "
            "(claims/, open-questions/… à la racine ou sous preuves/)"
        )
        return 1

    if errors:
        print(f"✗ {len(errors)} erreur(s) sur {checked} artefact(s)\n")
        for e in errors:
            print(f"  {e}")
        return 1

    print(f"✓ {checked} artefact(s) valides")
    return 0


if __name__ == "__main__":
    sys.exit(main())
