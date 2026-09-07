# Schémas DMAD

Les schémas ne sont pas de la documentation : ce sont les **points d'application mécanique des principes du manifeste**. Un principe qui n'est pas contraint par un schéma est un vœu pieux.

| Schéma | Principe qu'il fait respecter |
|---|---|
| [`claim.schema.json`](claim.schema.json) | **P2** — `evidence` avec `minItems: 1` : une claim sans preuve est refusée à l'écriture, pas signalée après coup |
| | **P3** — `confidence_reason` obligatoire (min. 20 car.) : force l'agent à dire ce qui manque pour monter d'un niveau |
| | **P5** — `intent` est un objet séparé du `statement`, avec sa propre confiance plafonnée à `H` |
| | **P10** — `freshness` obligatoire : sans commit de référence, pas de détection de péremption |
| [`scope.schema.json`](scope.schema.json) | **P8** — `exclude` exige une `reason` par exclusion ; `feature.vocabulary` exige 3 termes minimum |
| [`capability.schema.json`](capability.schema.json) | **gate 3** — `hypothesis_strength` et les 4 `signals` obligent le Carver à exposer sur quoi il s'appuie |
| [`challenge.schema.json`](challenge.schema.json) | **anti-complaisance** — `angles_examined` + `angles_skipped` justifiés + `weakest_claims` |
| [`open-question.schema.json`](open-question.schema.json) | **P4** — `why_it_matters` et `audience` obligatoires : une question sans impact ni destinataire ne sera jamais traitée |

## Trois contraintes qui méritent une explication

### `confidence_reason` obligatoire
Demander le niveau ne suffit pas : un modèle coche `C` sans réfléchir. Exiger **pourquoi ce niveau et pas le suivant** l'oblige à formuler ce qui manque — et ce texte devient directement exploitable (« il manque un test de caractérisation sur ce chemin » est une tâche, pas un constat).

### `conditional_on`
Une règle dont le comportement dépend d'un feature flag ou d'une config n'est pas une règle : c'est deux règles et un interrupteur. Ce bloc rend la condition explicite. **C'est la source numéro un de documentation vraie en recette et fausse en production.**

### `evidence.kind: "absence"`
Une preuve négative est une preuve. « Aucun test associé à cette règle », « aucune trace de validation métier », « ce chemin n'apparaît dans aucun log » sont des informations qui pèsent sur la confiance. Sans ce type, un agent n'a aucun moyen d'enregistrer ce qu'il a cherché sans trouver — et l'absence de recherche devient indiscernable de l'absence de résultat.

## Validation

```bash
python3 tools/validate.py            # valide tous les artefacts d'un run
```

Les schémas sont en JSON Schema draft 2020-12 et validés en CI.
