# Violations — fixtures de non-régression

Six claims volontairement fautives. Chacune correspond à un **mode de défaillance réel** de la rétro-documentation par LLM, et chacune doit être refusée par `tools/validate.py`.

| Fixture | Défaillance simulée | Principe violé | Ce qui se passerait sans le garde-fou |
|---|---|---|---|
| `BR-BAD-001` | Affirmation sans aucune preuve, justifiée par « le code semble indiquer » | **P2** | Une règle inventée entre dans la documentation métier avec l'apparence d'un fait |
| `BR-BAD-002` | Le modèle s'auto-décerne le niveau `V` sur la foi de sa propre lecture | **P3** | La confiance devient une opinion du modèle — exactement ce que l'échelle DMAD existe pour empêcher |
| `BR-BAD-003` | Une intention métier promue en `C` sans validation humaine | **P5** | Une hypothèse historique se transforme silencieusement en fait établi |
| `BR-BAD-004` | Règle pilotée par une configuration, énoncée sans condition | **conditional_on** | Documentation vraie en production et fausse en local — la variante la plus difficile à détecter en relecture |
| `BR-BAD-005` | Affirmation d'exhaustivité alors que la navigation s'est faite au `grep` | **plafond de capability** | Un « aucun autre appelant » non vérifiable fonde une décision de refactoring |
| `RISK-BAD-006` | Un constat structurel en `V` sans nommer l'outil qui l'a mesuré | **traçabilité mécanique** | Une impression du modèle (« beaucoup de modifications récentes ») prend le statut de mesure |

## Deux régimes de preuve pour le niveau `V`

`BR-BAD-002` et `RISK-BAD-006` testent les deux versants d'une même règle, et il
faut les lire ensemble :

- Une claim **interprétative** (règle de gestion, cas d'usage, invariant, machine
  à états, acteur) ne peut atteindre `V` que par une **preuve exécutée** (test
  vert) ou **déclarative** (schéma, migration, runtime). La lecture du code par
  le modèle ne prouve rien, quelle que soit sa qualité.
- Une claim **structurelle** (risque, terme) est un constat d'outil : un
  `git churn` ou un LSP la prouve. Elle atteint `V` sans test — mais **doit
  nommer l'outil** qui l'a produite.

Sans cette distinction, la règle stricte rejetterait les hotspots mesurés par
git ; sans le garde-fou du second versant, « le modèle a trouvé que » se
déguiserait en mesure.

## Pourquoi ces fixtures existent

Les principes du manifeste ne valent que s'ils sont **exécutables**. Ces six fichiers sont la preuve que `claim.schema.json` et les règles croisées de `validate.py` refusent réellement les dérives, plutôt que de les décrire dans un document que personne ne relit.

```bash
python3 tools/validate.py examples/violations   # doit sortir en code 1 avec 6 erreurs
./tools/selftest.sh                             # vérifie l'ensemble
```
