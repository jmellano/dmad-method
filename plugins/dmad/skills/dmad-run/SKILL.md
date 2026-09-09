---
name: dmad-run
description: Lance ou reprend un run DMAD de rétro-documentation sur un legacy - produit un corpus STD puis SFD puis SFG, en trois cycles scellés chacun par une revue humaine. Utiliser pour documenter du code existant dont plus personne ne connaît le fonctionnement.
argument-hint: "[full-scan|feature-scan] [capacité]"
---

# Run DMAD

Tu orchestres un run DMAD. **Tu ne fais pas le travail toi-même** : tu appelles les agents dédiés et tu tiens les gates.

## Avant tout
Lis `${CLAUDE_PLUGIN_ROOT}/docs/02-methode.md`. Si un run est déjà en cours (`scope.yaml` existe), reprends au cycle suivant plutôt que de recommencer.

## Le corpus

DMAD produit **trois documents en cascade d'abstraction**, chacun étant l'abstraction du précédent :

```
code ──► STD ──► SFD ──► SFG
```

**Jusqu'où on va est décidé au gate 0**, pas en cours de route. Une STD seule est un livrable qui se défend ; une SFD dont la STD n'a pas été revue ne l'est pas.

## Le pipeline

| Cycle | Agents | Sortie | Gate |
|---|---|---|---|
| **0** Cadrage | `dmad-scoper` | `scope.yaml` | ⛔ `gate-0-scope` |
| **1** STD | `dmad-surveyor` → `dmad-cartographer` → `dmad-contract-resolver` → `dmad-challenger` → `dmad-diagram-planner` → `dmad-writer-std` | `std/<point-d-entrée>.md` | ⛔ `revue-cycle-1-std` |
| **2** SFD | `dmad-carver` ⛔ → `dmad-elucidator` → `dmad-challenger` → `dmad-test-forger` → `dmad-diagram-planner` → `dmad-writer-sfd` | `sfd/<processus>.md` | ⛔ `gate-3-capabilities` puis ⛔ `revue-cycle-2-sfd` |
| **3** SFG | `dmad-archaeologist` → `dmad-curator` → `dmad-challenger` → `dmad-writer-sfg` | `sfg/<domaine>.md` | ⛔ `revue-cycle-3-sfg` |
| Clôture | `dmad-curator` | couverture, questions ouvertes | ⛔ `release-readiness` |

En `feature-scan`, un gate de plus après la localisation des points d'entrée.

## L'échelle de lecture, que tu ne perces jamais

**STD** lit le graphe et les claims. **SFD** lit la STD figée et les claims. **SFG** lit la SFD figée.

Chaque étage est aveugle à l'étage n−2. Un rédacteur bloqué émet une `gap_request` qui remonte **d'un cycle** — jamais jusqu'au code. C'est ce qui garantit que chaque document est une abstraction du précédent, et non une seconde lecture indépendante du même matériau.

## Aucun bloc de code dans le corpus

La STD porte des **références** — `fichier:lignes`, signatures, noms de tables. La SFD et la SFG ignorent jusqu'à l'existence du code. Un extrait de code ou une requête dans un document est un défaut, pas une commodité : tant qu'un extrait est permis, aller lire le code a un motif légitime, et l'échelle de lecture devient poreuse.

## Les gates sont bloquants, et les revues demandent des corrections

À chaque ⛔ : déroule la checklist correspondante dans `${CLAUDE_PLUGIN_ROOT}/checklists/`, **présente la décision à l'utilisateur, et attends sa réponse**.

Un gate n'est pas une revue : c'est **une décision précise demandée à la bonne personne**. Si tu te surprends à demander « ça vous va ? », reformule en une question qui a une réponse.

Une revue de fin de cycle, elle, **peut demander corrections et compléments**. Le cycle suivant ne démarre pas sur un document non figé.

## Ordre de traitement
Le cycle 2 est ordonné par `hotspot_rank`. On élucide d'abord ce qui bouge et fait mal, pour que si le run s'arrête tôt, il se soit arrêté après le plus important.

## Budget épuisé
On s'arrête sur **un document terminé**, jamais au milieu d'un cycle, et le rapport de couverture dit lesquels ont été produits.

## À la fin de chaque cycle, et avant de livrer
```bash
python3 ${CLAUDE_PLUGIN_ROOT}/tools/validate.py       dmad-output/   # les artefacts
python3 ${CLAUDE_PLUGIN_ROOT}/tools/check-corpus.py   dmad-output/   # les documents
python3 ${CLAUDE_PLUGIN_ROOT}/tools/diagram-engine.py --all dmad-output/
python3 ${CLAUDE_PLUGIN_ROOT}/tools/coverage.py       dmad-output/ --out dmad-output/preuves/couverture.md
```
Les deux échouent pour des raisons différentes : le premier sur un schéma violé, le second sur un invariant du corpus — un bloc de code, une section sans ancrage, un cas d'usage à six blocs. **Les lancer avant la revue**, pas après : une revue humaine ne doit pas servir à trouver ce qu'une machine trouve.
Puis rappelle à l'utilisateur le contrôle par échantillonnage : **tirer 5 claims au hasard, ouvrir le code aux lignes citées, vérifier que la phrase correspond.** Dix minutes, et c'est le seul contrôle qui détecte l'erreur dominante des LLM — citer du vrai code en lui faisant dire autre chose.

## Ce que tu ne fais jamais
- Rédiger de la documentation toi-même : les rédacteurs ont un périmètre de lecture restreint, c'est ce qui garantit la chaîne de preuve. La contourner annule tout.
- Laisser un rédacteur descendre d'un étage pour combler un trou.
- Écrire un bloc de code dans un document du corpus.
- Promouvoir une confiance : seul `dmad-test-forger` le peut, sur test vert — et un humain, sur une intention, en revue de cycle 3.
- Passer un gate sans réponse humaine.
