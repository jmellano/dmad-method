# Run de référence — Atlas ERP, capacité « Facturation »

Un run DMAD complet et fictif, déroulé de bout en bout. Il sert trois usages :

1. **Montrer à quoi ressemble la méthode en pratique**, plutôt que de la décrire
2. **Servir de fixture de non-régression** — `validate.py` et `check-corpus.py` s'exécutent dessus
3. **Fournir un modèle** pour un premier run réel

Depuis la v0.4, il produit le **corpus à trois documents** : une STD par point d'entrée, une SFD par arbre de business objects, une SFG par cas d'usage. Chacun est l'abstraction du précédent et **aveugle à l'étage n−2**.

## Le contexte

Atlas ERP : 214 kLOC de Java 8 / Spring 4.3, démarré en 2011. Le développeur qui a écrit la facturation est parti en 2023. Un nouveau barème doit entrer en vigueur au 1er janvier, et **personne ne sait comment les montants sont calculés**.

> « Dans trois semaines, je dois pouvoir faire évoluer les règles de facturation sans risquer de régression comptable. »

C'est un `objective.kind: evolve`, et vu la taille du dépôt, un `feature-scan`.

## Le déroulé

### Phase 0 — Cadrage → [`scope.yaml`](scope.yaml)

Le vocabulaire d'amorce fourni par le responsable comptable — *facture, avoir, échéance, relance, barème, campagne de facturation* — est ce qui rend le feature-scan possible.

Trois exclusions justifiées, une confidentialité tranchée (`local_only: true`, aucun extrait de code ne sort de la machine), et surtout **un plafond annoncé d'emblée** : la couverture de tests est disponible mais pas les traces d'exécution, donc `runtime-evidence` est en mode dégradé. La documentation décrira des chemins *possibles*, pas *empruntés*. Le commanditaire l'apprend au gate 0, pas à la livraison.

### Phases 1–2 — Reconnaissance et cartographie

51 points d'entrée recensés sur tout le dépôt, 8 retenus pour la facturation après le gate de localisation. 17 frontières de traversée journalisées, dont **2 dispatchs dynamiques non résolus** — enregistrés comme tels plutôt que devinés.

### Phase 3 — Découpage → [`capabilities/facturation.yaml`](capabilities/facturation.yaml)

Le Carver propose 6 capacités, dont une ambiguïté qu'il expose au lieu de la trancher : *Recouvrement* est-elle autonome ou une étape de *Facturation* ? Les données sont partagées, mais l'historique git les sépare depuis 2021.

**Le gate 3 est instructif** : l'expert métier confirme le découpage proposé, mais **pour une raison que le code ne pouvait pas donner** — le recouvrement a ses propres indicateurs et son propre pilotage. Cette raison est conservée dans `gate_3.corrections`, et elle vaudra pour le prochain arbitrage.

### Phase 4 — Élucidation → [`claims/`](claims/)

Deux claims illustrent les deux régimes de la méthode :

**[`BR-FACT-021`](claims/BR-FACT-021.yaml)** — l'arrondi des montants. Quatre preuves convergentes dont un type `DECIMAL(12,4)` en base et un test qui passe. C'est le cœur de l'objectif du run.

**[`BR-FACT-014`](claims/BR-FACT-014.yaml)** — les factures à montant nul. Énoncée d'abord sans condition, en `C`.

### Phase 5 — Challenge → [`challenges/`](challenges/)

**[`CHK-2026-09-07-031`](challenges/CHK-2026-09-07-031.yaml)** est l'artefact le plus démonstratif du run. Le Challenger examine 8 angles sur 9 (le 9e, la concurrence, est écarté avec justification écrite) et trouve **deux défauts que personne n'aurait vus en relecture** :

- **Angle 3 — configuration.** La règle est pilotée par un flag actif en production mais **inactif par défaut dans le dépôt**. Formulée sans condition, elle est vraie pour qui observe la production et fausse pour un développeur qui lance le projet en local. C'est le type d'erreur qui, découvert plus tard, fait perdre confiance dans toute la documentation.

- **Angle 7 — exhaustivité.** L'énoncé disait « n'est jamais transmise ». Or sur 3 appelants, un seul passe par la garde : `ReinvoiceCommand` appelle le service d'envoi directement. **L'exhaustivité était fausse.**

Résultat : `demoted` de `C` à `I`, reformulation exigée, et une question ouverte créée.

En parallèle, le Test Forger écrit `AmountCalculatorCharacterizationTest`. Le test passe → **`BR-FACT-021` est promue en `V`**. C'est le seul mécanisme qui atteint le niveau maximal, et il produit au passage un filet de sécurité réutilisable pour le changement de barème.

### Cycle 1 — la STD → [`output/std/nightly-billing.md`](output/std/nightly-billing.md)

Dix-sept sections, **aucune omise** : la section « Événements » porte son constat d'absence plutôt que de disparaître, et la section « Requêtes clés » signale que les requêtes de `reporting` portent sur les mêmes tables **sans appartenir à ce batch** — le piège d'attribution le plus probable ici.

**Aucun bloc de code, aucune requête.** Des références : `AmountCalculator.java:88`, `invoice_lines.amount DECIMAL(12,4)`. C'est la conformité ISO 25010, et c'est ce qui rend tenable la coupure des rédacteurs : tant qu'un extrait est permis, aller lire le code a un motif légitime.

La section 9 montre **les deux bouts de l'échelle des contrats** : un contrat résolu au barreau 1, avec son artefact et sa version, et un contrat non résolu qui porte un placeholder visible plutôt qu'un identifiant plausible.

La revue de cycle 1 a produit une **correction factuelle** : le document annonçait une reprise indéfinie de la transmission ; elle s'arrête à cinq campagnes. Le développeur l'a vue, la traversée l'avait manquée.

### Cycle 2 — la SFD → [`output/sfd/facturation.md`](output/sfd/facturation.md)

Vue récursive à trois niveaux, chacun avec ses six blocs. **Analysée bas → haut, rédigée haut → bas.**

Ce que la classification ISO 25010 fait apparaître et qu'une rédaction libre aurait manqué : le statut de litige est lu **par commande** — environ 1 400 lectures par campagne — et le barème **par ligne**, jusqu'à quarante par facture. Deux données `ad-hoc` en boucle, signalées comme telles. C'est le premier candidat à l'optimisation, et il ne se voit nulle part ailleurs.

Le document ne contient **aucun nom de classe et aucun nom de patron** : le Template Method reconnu par le Carver a servi au découpage, il n'apparaît pas.

### Cycle 3 — la SFG → [`output/sfg/facturation.md`](output/sfg/facturation.md)

Deux cas d'usage, sept blocs chacun, dont « ce qui n'est pas couvert » — le bloc qu'on oublie, et le plus structurant.

**Le constat de méthode le plus instructif du run est là** : le découpage initial suivait les deux points d'entrée techniques, et il a fallu écrire les deux sections en entier pour voir que la vraie ligne de partage n'est pas le déclencheur mais **le jeu de règles appliqué**.

Et une **correction factuelle** consignée dans l'historique, avec ce qui était écrit et pourquoi c'était faux : la version 1.0 présentait la reprise comme une garantie de non-perte. La SFD disait « reprise à la campagne suivante » sans dire jusqu'à quand ; la dérivation avait comblé le silence par une promesse. **C'est exactement le risque propre au troisième document** — le lecteur de la SFG n'a aucun moyen de le détecter.

### Le rapport de couverture → [`output/preuves/couverture.md`](output/preuves/couverture.md)

22 % du code, 90 % des hotspots, 100 % des points d'entrée de la capacité — et la ligne nouvelle en v0.4 : **un contrat résolu sur deux, avec la répartition par barreau**. Elle mesure la qualité des sources, pas seulement le nombre de contrats trouvés.

## Ce que ce run illustre

| Principe | Où le voir |
|---|---|
| **P2** — aucune affirmation sans preuve | chaque claim, 4 à 5 `evidence` |
| **P3** — confiance dérivée | `BR-FACT-021` promue en `V` par un test vert, pas par une opinion |
| **P4** — l'inconnu est un livrable | 5 questions P1, formulées comme des questions fermées avec options |
| **P5** — le code ne dit pas le pourquoi | `intent` séparé, en `H`, avec `competing_hypotheses` |
| **P9** — couverture mesurée | 22 % assumé et argumenté |
| Anti-hallucination | 2 dispatchs non résolus enregistrés au lieu d'être devinés |
| **D16** — aucun code dans le corpus | la STD porte des références, la section 8 remplace le SQL par tables et intention |
| **D17** — cascade | chaque niveau de la SFD ancré dans la STD, chaque règle de la SFG tracée vers la SFD |
| **D18** — contrat versionné | `CTR-FACT-001` porte `accounting-api:4.7.2` ; `CTR-FACT-002` porte un placeholder assumé |
| **D19** — revue par cycle | trois revues, trois corrections, dont deux factuelles |
| Configuration | `conditional_on` sur `BR-FACT-014` — la doc n'est pas la même en prod et en local |

## Le résultat, en une phrase

> Le commanditaire voulait pouvoir changer le barème sans casser la compta.
> Il repart avec **le calcul des montants prouvé par des tests**, un filet de
> sécurité réutilisable, **deux défauts qu'il ignorait** (le flag divergent
> entre environnements, le contournement par la CLI), et **cinq questions
> précises** dont les réponses feront monter 14 affirmations d'hypothèse à
> fait établi.

Aucune de ces quatre choses ne serait sortie d'un « résume-moi ce repo ».

## Vérifier

```bash
python3 ../../tools/validate.py     .          # 17 artefacts valides
python3 ../../tools/check-corpus.py output/    # 3 documents conformes
../../tools/selftest.sh                        # + les 25 violations bien refusées
```
