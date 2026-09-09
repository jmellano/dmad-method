# Tâches DMAD

Procédures opérationnelles mobilisées par les agents. Chaque tâche indique son agent, sa phase, ses sorties, et surtout **ses modes d'échec** — c'est la partie la plus utile en pratique.

| Tâche | Agent | Cycle |
|---|---|---|
| [00 — Cadrer le run](00-scope-run.md) | scoper | 0 |
| [10 — Recenser la codebase](10-survey-codebase.md) | surveyor | 1 |
| [11 — Découvrir les points d'entrée](11-discover-entrypoints.md) | surveyor | 1 |
| [12 — Localiser une fonctionnalité](12-locate-feature.md) | surveyor | 1 |
| [13 — Résoudre les contrats sortants](13-resolve-outbound-contracts.md) | contract-resolver | 1 |
| [20 — Construire le graphe](20-build-graph.md) | cartographer | 1 |
| [30 — Découper en capacités](30-carve-capabilities.md) | carver | 2 |
| [31 — Identifier les business objects](31-identify-business-objects.md) | carver | 2 |
| [40 — Reconstituer les cas d'usage](40-elucidate-usecases.md) | elucidator | 2 |
| [41 — Extraire les règles de gestion](41-extract-business-rules.md) | elucidator | 2 |
| [42 — Reconstituer l'intention](42-reconstruct-intent.md) | archaeologist | 3 |
| [43 — Classer opérations et données](43-classify-iso25010.md) | elucidator | 2 |
| [50 — Réfuter une claim](50-challenge-claim.md) | challenger | 1, 2, 3 |
| [51 — Forger un test de caractérisation](51-forge-characterization-test.md) | test-forger | 2 |
| [60 — Planifier les diagrammes](60-plan-diagrams.md) | diagram-planner | 1, 2 |
| [63 — Rendre la STD](63-render-std.md) | writer-std | 1 |
| [64 — Rendre la SFD](64-render-sfd.md) | writer-sfd | 2 |
| [65 — Rendre la SFG](65-render-sfg.md) | writer-sfg | 3 |
| [70 — Calculer la couverture](70-compute-coverage.md) | curator | 3 |
| [71 — Vérifier la fraîcheur](71-check-freshness.md) | curator | maintien |

## Les quatre tâches à lire en premier

Si vous ne lisez que quatre tâches, celles-ci portent l'essentiel de ce qui fait la différence entre DMAD et une génération de documentation :

- **[12 — Localiser une fonctionnalité](12-locate-feature.md)** — les cinq sondes. Le seul mode d'échec de la méthode qui ne se voit pas dans le résultat : une documentation parfaite du mauvais périmètre.
- **[41 — Extraire les règles](41-extract-business-rules.md)** — commencer par les contraintes de base (des règles `V` gratuites), et les quatre pièges : calculs, configuration, code mort, surcharge.
- **[50 — Réfuter une claim](50-challenge-claim.md)** — les 9 angles, et pourquoi « trouve ce qui rend ceci faux » ne donne pas le même résultat que « vérifie ceci ».
- **[42 — Reconstituer l'intention](42-reconstruct-intent.md)** — le motif « incident », souvent la découverte la plus utile d'un run.

Deux ajouts de la v0.4 méritent la même attention :

- **[13 — Résoudre les contrats sortants](13-resolve-outbound-contracts.md)** — l'échelle à quatre barreaux. Un code de contrat faux ressemble exactement à un code vrai ; écrire le barreau est ce qui rend la différence visible.
- **[43 — Classer opérations et données](43-classify-iso25010.md)** — le filtre qui décide de ce qui entre dans une SFD, et la distinction initiale/ad-hoc, signal le plus rentable du cycle 2.
