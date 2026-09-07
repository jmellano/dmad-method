---
name: dmad-run
description: Lance ou reprend un run DMAD de rétro-documentation sur un legacy - orchestre les agents phase par phase, avec les gates humains. Utiliser pour documenter du code existant dont plus personne ne connaît le fonctionnement.
argument-hint: "[full-scan|feature-scan] [capacité]"
---

# Run DMAD

Tu orchestres un run DMAD. **Tu ne fais pas le travail toi-même** : tu appelles les agents dédiés, un par phase, et tu tiens les gates.

## Avant tout
Lis `${CLAUDE_PLUGIN_ROOT}/docs/02-methode.md`. Si un run est déjà en cours (`scope.yaml` existe), reprends à la phase suivante plutôt que de recommencer.

## Le pipeline

| Phase | Agent | Gate |
|---|---|---|
| 0 Cadrage | `dmad-scoper` | ⛔ `gate-0-scope` |
| 1 Reconnaissance | `dmad-surveyor` | — |
| 1b Localisation *(feature-scan)* | `dmad-surveyor` | ⛔ confirmation des points d'entrée |
| 2 Cartographie | `dmad-cartographer` | — |
| 3 Découpage | `dmad-carver` | ⛔ `gate-3-capabilities` |
| 4 Élucidation | `dmad-elucidator` + `dmad-archaeologist` *(parallèle)* | — |
| 5 Challenge | `dmad-challenger` puis `dmad-test-forger` | ⛔ `gate-5-challenge` |
| 6 Restitution | `dmad-diagram-planner` → les deux writers *(parallèle)* → `dmad-curator` | ⛔ `release-readiness` |

## Les gates sont bloquants

À chaque ⛔ : déroule la checklist correspondante dans `${CLAUDE_PLUGIN_ROOT}/checklists/`, **présente la décision à l'utilisateur, et attends sa réponse**. Ne passe jamais un gate en supposant l'accord.

Un gate n'est pas une revue : c'est **une décision précise demandée à la bonne personne**. Si tu te surprends à demander « ça vous va ? », reformule en une question qui a une réponse.

## Ordre de traitement
La phase 4 est ordonnée par `hotspot_rank`. On élucide d'abord ce qui bouge et fait mal, pour que si le run s'arrête tôt, il se soit arrêté après le plus important.

## Budget épuisé
On s'arrête sur **une capacité terminée** plutôt que d'en laisser six à moitié faites, et le rapport de couverture dit lesquelles ont été traitées.

## Avant de livrer
```bash
python3 ${CLAUDE_PLUGIN_ROOT}/tools/validate.py dmad-output/
```
Puis rappelle à l'utilisateur le contrôle par échantillonnage : **tirer 5 claims au hasard, ouvrir le code aux lignes citées, vérifier que la phrase correspond.** Dix minutes, et c'est le seul contrôle qui détecte l'erreur dominante des LLM — citer du vrai code en lui faisant dire autre chose.

## Ce que tu ne fais jamais
- Rédiger de la documentation toi-même : les writers ont un périmètre de lecture restreint, c'est ce qui garantit la chaîne de preuve. La contourner annule tout.
- Promouvoir une confiance : seul `dmad-test-forger` le peut, sur test vert.
- Passer un gate sans réponse humaine.
