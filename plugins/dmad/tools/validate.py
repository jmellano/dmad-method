#!/usr/bin/env python3
"""Valide les artefacts d'un run DMAD contre les schémas.

Ce n'est pas un utilitaire de confort : c'est le point d'application mécanique
des principes du manifeste. Une claim sans preuve, une exclusion sans
justification ou une question sans destinataire sont refusées ici, pas
signalées en relecture.

**Les artefacts de connaissance sont des concepts** — du Markdown à frontmatter
(D27). Le frontmatter se valide contre les mêmes schémas qu'un YAML,
`additionalProperties: false` compris : le garde-fou qui refuse un agent
inventant son propre format reste entier. **Le corps du concept EST son
énoncé** : il est injecté comme `statement` avant validation, pour qu'un même
texte ne vive pas à deux endroits.

Ce qui reste de la donnée reste de la donnée : faits, graphe, frontières et
plans sont lus par des outils, pas par des lecteurs, et gardent leur format.

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
# Chemins relatifs à un processus. Le sujet vient avant la nature : un chemin
# doit dire de quoi parle le fichier avant qu'on l'ouvre (D27).
ROUTES = {
    "preuves/claims": "claim.schema.json",
    "preuves/challenges": "challenge.schema.json",
    "preuves/questions": "open-question.schema.json",
    "preuves/contrats": "external-contract.schema.json",
    "preuves/business-objects": "business-object.schema.json",
}
# Routes de racine, hors processus.
ROUTES_RACINE = {
    "socle/capacites": "capability.schema.json",
    "socle/metier": "claim.schema.json",
    "socle/technique": "claim.schema.json",
}
SINGLE_FILES = {"run.yaml": "scope.schema.json", "scope.yaml": "scope.schema.json"}

# Un dossier routé ne contient QUE des concepts. Un artefact ignoré doit être
# aussi bruyant qu'un artefact invalide : c'est ainsi que neuf claims écrites
# en .json ont traversé un run sans être regardées.
EXTENSIONS_CONCEPT = {".md"}
# Le corps d'un concept EST son énoncé — mais toutes les natures ne l'appellent
# pas « statement » : une question ouverte est une question.
CHAMP_CORPS = {"preuves/questions": "question"}
TOLERES = {"index.md", "log.md", "README.md"}

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
    if path.suffix in (".yaml", ".yml"):
        return yaml.safe_load(text)
    if path.suffix == ".json":
        return json.loads(text)
    return load_concept(text)


def load_concept(text: str, champ: str = "statement"):
    """Un concept : frontmatter YAML, puis un corps qui EST l'énoncé."""
    if not text.startswith("---"):
        raise ValueError("concept sans frontmatter — la règle dure d'OKF")
    fin = text.find("\n---", 3)
    if fin == -1:
        raise ValueError("frontmatter non refermé")
    doc = yaml.safe_load(text[3:fin]) or {}
    if not isinstance(doc, dict):
        raise ValueError("frontmatter qui n'est pas un mapping")
    corps = text[fin + 4:]
    corps = re.split(r"^# Liens\s*$", corps, maxsplit=1, flags=re.M)[0]
    corps = re.sub(r"^\[\^[^\]]+\]:.*$", "", corps, flags=re.M).strip()
    if corps and champ not in doc:
        doc[champ] = corps
    return doc


RE_REF = re.compile(r"^(?P<file>[^#\s]+)#L(?P<start>\d+)(?:-L?(?P<end>\d+))?$")


def check_refs(artefacts, racine_code, errors):
    """Toute plage de lignes citée tient dans son fichier.

    C'est le contrôle qui manquait, et celui qui aurait attrapé une cartographie
    faite dans une copie hors périmètre sans lire une ligne de code : une preuve
    `fichier#L325-333` sur un fichier de 106 lignes passait au vert.

    Il attrape le symptôme, pas la cause : une copie de MÊME longueur passerait.
    C'est la liste fermée du périmètre qui ferme la porte.
    """
    if racine_code is None:
        return
    for chemin, doc in artefacts:
        pile = [doc]
        while pile:
            n = pile.pop()
            if isinstance(n, dict):
                ref = n.get("ref")
                if isinstance(ref, str) and "#L" in ref:
                    m = RE_REF.match(ref.strip())
                    if not m:
                        errors.append(f"{chemin}: référence illisible — {ref}")
                    else:
                        cible = racine_code / m.group("file")
                        if not cible.exists():
                            errors.append(
                                f"{chemin}: fichier inexistant dans le périmètre — {m.group('file')}"
                            )
                        else:
                            total = len(cible.read_text(errors="replace").splitlines())
                            dernier = int(m.group("end") or m.group("start"))
                            if dernier > total:
                                errors.append(
                                    f"{chemin}: {m.group('file')} fait {total} lignes, la preuve "
                                    f"cite jusqu'à L{dernier}. Soit la référence est fausse, soit "
                                    "elle vise une autre arborescence que le périmètre"
                                )
                pile.extend(n.values())
            elif isinstance(n, list):
                pile.extend(n)


# Une note qui ressemble à du code EST du code. Fermer `excerpt` sans fermer
# `note` déplace la porte : les rédacteurs lisent les claims.
RE_NOTE_CODE = re.compile(r"[;{}]|\w+\.\w+\s*\(|->|=>|::|\bif\s*\(|\breturn\b|SELECT\s|INSERT\s|UPDATE\s")


def agents_connus():
    d = pathlib.Path(__file__).parent.parent / "agents"
    return {f.stem.replace("dmad-", "").lower() for f in d.glob("*.md")} if d.is_dir() else set()


def check_notes(artefacts, errors):
    for chemin, doc in artefacts:
        for ev in doc.get("evidence") or []:
            note = (ev or {}).get("note")
            if isinstance(note, str) and RE_NOTE_CODE.search(note):
                errors.append(
                    f"{chemin}: evidence.note contient du code — « {note[:60]}… ». "
                    "Une note dit en français ce que la preuve montre ; le code y "
                    "transite vers les rédacteurs, qui n'y ont pas droit"
                )


def ancres_de(chemin):
    """Les ancres qu'un titre Markdown produit, façon GitHub."""
    import unicodedata
    out = set()
    for m in re.finditer(r"^#{1,6}\s+(.+?)\s*$", chemin.read_text(encoding="utf-8"), re.M):
        s = unicodedata.normalize("NFKD", m.group(1))
        s = "".join(c for c in s if not unicodedata.combining(c)).lower()
        out.add(re.sub(r"[\s_]+", "-", re.sub(r"[^\w\s-]", "", s).strip()))
    return out


def check_validations(claims, run, errors):
    """Une validation humaine s'adosse à une décision tracée, ou elle n'existe pas."""
    agents = agents_connus()
    for chemin, claim in claims:
        intent = claim.get("intent")
        if not isinstance(intent, dict):
            continue
        vb = intent.get("validated_by")
        if not isinstance(vb, dict):
            continue
        who = str(vb.get("who", ""))
        mots = set(re.findall(r"[a-z-]+", who.lower().replace("dmad-", "")))
        if mots & agents or "agent" in who.lower():
            errors.append(
                f"{chemin}: intent.validated_by.who = « {who} » désigne un agent. "
                "Un agent ne valide pas une intention — c'est ce que P5 exclut, et "
                "c'est le seul levier de promotion qui existe"
            )
        gate = vb.get("gate", "")
        fichier, _, ancre = str(gate).partition("#")
        cible = run / fichier
        if not cible.exists():
            errors.append(
                f"{chemin}: intent.validated_by.gate pointe {fichier}, qui n'existe pas. "
                "Une validation sans trace de décision est une attestation fabriquée"
            )
        elif ancre and ancre.lower() not in ancres_de(cible):
            errors.append(
                f"{chemin}: {fichier} ne porte pas « {ancre} ». La décision citée "
                "n'est pas dans le compte rendu du gate"
            )


def check_cross_rules(claims, errors):
    """Règles inter-documents que le JSON Schema ne peut pas exprimer."""
    for path, claim in claims:
        # P5 : l'intention ne peut sortir de H que par une validation humaine tracée.
        intent = claim.get("intent") or {}
        if not isinstance(intent, dict):
            errors.append(f"{path}: intent doit être un objet, pas {type(intent).__name__}")
            continue
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
    ap.add_argument("--code", type=pathlib.Path, help="racine du code analysé, pour contrôler les plages de lignes")
    args = ap.parse_args()

    validators = {
        name: Draft202012Validator(json.loads((args.schemas / name).read_text()))
        for name in set(ROUTES.values()) | set(ROUTES_RACINE.values()) | set(SINGLE_FILES.values())
    }

    errors: list[str] = []
    checked = 0
    collected: dict[str, list[tuple[str, dict]]] = {r: [] for r in ROUTES}

    # Un dossier par processus, puis les routes de racine. Le sujet avant la nature.
    dossiers: list[tuple[pathlib.Path, str, str]] = []
    for proc in sorted((args.run / "processus").glob("*")) if (args.run / "processus").is_dir() else []:
        if proc.is_dir():
            for route, schema in ROUTES.items():
                dossiers.append((proc / route, route, schema))
    for route, schema in ROUTES_RACINE.items():
        dossiers.append((args.run / route, route, schema))

    for chemin_dossier, route, schema in dossiers:
        if not chemin_dossier.is_dir():
            continue
        for path in sorted(chemin_dossier.iterdir()):
            if path.is_dir() or path.name in TOLERES or path.name.startswith("."):
                continue
            if path.suffix not in EXTENSIONS_CONCEPT:
                # Un artefact ignoré doit être aussi bruyant qu'un artefact invalide.
                errors.append(
                    f"{path}: fichier non-concept dans un dossier routé. Un concept est "
                    "du Markdown à frontmatter ; ce fichier ne serait pas contrôlé, et "
                    "personne ne remarque un compteur bas"
                )
                continue
            checked += 1
            try:
                doc = (load_concept(path.read_text(encoding="utf-8"),
                                    CHAMP_CORPS.get(route, "statement"))
                       if path.suffix == ".md" else load(path))
            except (ValueError, yaml.YAMLError) as e:
                errors.append(f"{path}: illisible — {e}")
                continue
            errs = list(validators[schema].iter_errors(doc))
            for err in errs:
                loc = "/".join(str(p) for p in err.path) or "<racine>"
                errors.append(f"{path}: {loc}: {err.message}")
            # Les règles croisées ne tournent que sur ce qui a passé le schéma.
            # Sinon un `intent` écrit en chaîne fait tomber le validateur en
            # traceback — et un traceback se lit « souci d'outillage », pas
            # « mon artefact est invalide ».
            if not errs and route in collected:
                collected[route].append((str(path), doc))

    claims = collected.get("preuves/claims", [])

    for filename, schema in SINGLE_FILES.items():
        path = args.run / filename
        if path.exists():
            checked += 1
            for err in validators[schema].iter_errors(load(path)):
                loc = "/".join(str(p) for p in err.path) or "<racine>"
                errors.append(f"{path}: {loc}: {err.message}")

    tous = [x for lot in collected.values() for x in lot]
    check_refs(tous, args.code, errors)
    check_cross_rules(claims, errors)
    check_notes(tous, errors)
    check_validations(claims, args.run, errors)
    check_contracts(collected.get("preuves/contrats", []), errors)
    check_business_objects(collected.get("preuves/business-objects", []), errors)

    if errors:
        print(f"✗ {len(errors)} erreur(s) sur {checked} artefact(s)\n")
        for e in errors:
            print(f"  {e}")
        return 1

    print(f"✓ {checked} artefact(s) valides")
    return 0


if __name__ == "__main__":
    sys.exit(main())
