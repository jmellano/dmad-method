# Run de référence — Atlas ERP, capacité « Facturation »

Un run DMAD complet et fictif, déroulé de bout en bout. Il sert trois usages :

1. **Montrer à quoi ressemble la méthode en pratique**, plutôt que de la décrire
2. **Servir de fixture de non-régression** — `tools/validate.py` s'exécute dessus
3. **Fournir un modèle** pour un premier run réel

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

### Phase 6 — Restitution → [`output/`](output/)

- **[Documentation fonctionnelle](output/fonctionnel/facturation.md)** — aucun nom de classe. La règle `V` est affirmative (« Le montant est calculé… »), la règle `I` est au conditionnel (« D'après l'analyse du code, … ne serait pas transmise »), l'intention est explicitement une hypothèse. **Un lecteur pressé qui ignore les badges perçoit quand même l'incertitude**, parce qu'elle est dans la langue.
- **[Fiche de module](output/technique/module-billing.md)** — le bus factor à 1, le couplage non prévu avec `reporting`, le contournement par la CLI, et une section « limites » explicite.
- **[Rapport de couverture](output/preuves/couverture.md)** — 22 % du code, 90 % des hotspots, 100 % des points d'entrée de la capacité. Le run est bon, et il le démontre au lieu de le prétendre.

## Ce que ce run illustre

| Principe | Où le voir |
|---|---|
| **P2** — aucune affirmation sans preuve | chaque claim, 4 à 5 `evidence` |
| **P3** — confiance dérivée | `BR-FACT-021` promue en `V` par un test vert, pas par une opinion |
| **P4** — l'inconnu est un livrable | 5 questions P1, formulées comme des questions fermées avec options |
| **P5** — le code ne dit pas le pourquoi | `intent` séparé, en `H`, avec `competing_hypotheses` |
| **P9** — couverture mesurée | 22 % assumé et argumenté |
| Anti-hallucination | 2 dispatchs non résolus enregistrés au lieu d'être devinés |
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
python3 ../../tools/validate.py .     # 7 artefacts valides
../../tools/selftest.sh               # + les 5 violations bien refusées
```
