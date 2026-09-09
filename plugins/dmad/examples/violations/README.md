# Violations — fixtures de non-régression

Quatorze artefacts volontairement fautifs. Chacun correspond à un **mode de défaillance réel** de la rétro-documentation par LLM, et chacun doit être refusé par `tools/validate.py`.

**Une fixture, une violation.** C'est la convention du dossier : une fixture qui en déclenche deux ne dit plus laquelle le garde-fou a attrapée.

| Fixture | Défaillance simulée | Principe violé | Ce qui se passerait sans le garde-fou |
|---|---|---|---|
| `BR-BAD-001` | Affirmation sans aucune preuve, justifiée par « le code semble indiquer » | **P2** | Une règle inventée entre dans la documentation métier avec l'apparence d'un fait |
| `BR-BAD-002` | Le modèle s'auto-décerne le niveau `V` sur la foi de sa propre lecture | **P3** | La confiance devient une opinion du modèle — exactement ce que l'échelle DMAD existe pour empêcher |
| `BR-BAD-003` | Une intention métier promue en `C` sans validation humaine | **P5** | Une hypothèse historique se transforme silencieusement en fait établi |
| `BR-BAD-004` | Règle pilotée par une configuration, énoncée sans condition | **conditional_on** | Documentation vraie en production et fausse en local — la variante la plus difficile à détecter en relecture |
| `BR-BAD-005` | Affirmation d'exhaustivité alors que la navigation s'est faite au `grep` | **plafond de capability** | Un « aucun autre appelant » non vérifiable fonde une décision de refactoring |
| `RISK-BAD-006` | Un constat structurel en `V` sans nommer l'outil qui l'a mesuré | **traçabilité mécanique** | Une impression du modèle (« beaucoup de modifications récentes ») prend le statut de mesure |

## Les huit fixtures de la v0.4

| Fixture | Défaillance simulée | Décision violée | Ce qui se passerait sans le garde-fou |
|---|---|---|---|
| `CTR-BAD-001` | Contrat lu au barreau 1, sans la version de l'artefact | **D18** | Le contrat reste plausible après le prochain bump de version, et devient faux en silence — anti-pattern A14 |
| `CTR-BAD-002` | Code lu dans un commentaire manuscrit, déclaré en `V` | **D18** | Un code faux ressemble exactement à un code vrai ; seul le barreau les distingue — anti-pattern A16 |
| `CTR-BAD-003` | Contrat non résolu, sans question ouverte | **D18** | Un placeholder visible se corrige ; un placeholder muet se propage |
| `BO-BAD-001` | Business object nommé d'après la méthode dont il est issu | **nommage** | La SFD parle le langage du code à un lecteur qui ne l'a pas |
| `BO-BAD-002` | Sous-objet inexistant dans l'arbre | **cohérence du graphe** | Un niveau de la vue récursive renvoie dans le vide |
| `DOC-BAD-001` | SFD sans `derives_from` | **D17** | L'information apparaît de nulle part : c'est la cascade percée, anti-pattern A15 |
| `DOC-BAD-002` | SFD dérivant d'une STD non figée | **D19** | Les corrections de la revue se propagent deux fois |
| `DOC-BAD-003` | SFG découpée par arbre de business objects | **D20** | Un document plié dans le découpage d'un autre gagne un niveau de titre et perd son lecteur |

`DOC-STD-FACT-001` n'est pas une violation : c'est le document non figé sur lequel `DOC-BAD-002` s'appuie. Une violation de cascade a besoin de deux documents pour exister.

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

Les principes du manifeste ne valent que s'ils sont **exécutables**. Ces fichiers sont la preuve que les schémas et les règles croisées de `validate.py` refusent réellement les dérives, plutôt que de les décrire dans un document que personne ne relit.

**Chaque message d'erreur nomme la décision qu'il applique.** Ce n'est pas de la cosmétique : un message qui ne dit pas quelle règle il fait respecter se fait contourner, puis supprimer, au premier agacement — et la règle disparaît avec lui.

```bash
python3 tools/validate.py examples/violations   # doit sortir en code 1
./tools/selftest.sh                             # vérifie l'ensemble
```
