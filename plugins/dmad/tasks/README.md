# Tâches DMAD

Procédures opérationnelles mobilisées par les agents. Chaque tâche indique son agent, sa phase, ses sorties, et surtout **ses modes d'échec** — c'est la partie la plus utile en pratique.

| Tâche | Agent | Phase |
|---|---|---|
| [00 — Cadrer le run](00-scope-run.md) | scoper | 0 |
| [10 — Recenser la codebase](10-survey-codebase.md) | surveyor | 1 |
| [11 — Découvrir les points d'entrée](11-discover-entrypoints.md) | surveyor | 1 |
| [12 — Localiser une fonctionnalité](12-locate-feature.md) | surveyor | 1b |
| [20 — Construire le graphe](20-build-graph.md) | cartographer | 2 |
| [30 — Découper en capacités](30-carve-capabilities.md) | carver | 3 |
| [40 — Reconstituer les cas d'usage](40-elucidate-usecases.md) | elucidator | 4 |
| [41 — Extraire les règles de gestion](41-extract-business-rules.md) | elucidator | 4 |
| [42 — Reconstituer l'intention](42-reconstruct-intent.md) | archaeologist | 4 |
| [50 — Réfuter une claim](50-challenge-claim.md) | challenger | 5 |
| [51 — Forger un test de caractérisation](51-forge-characterization-test.md) | test-forger | 5 |
| [60 — Planifier les diagrammes](60-plan-diagrams.md) | diagram-planner | 6 |
| [61 — Rendre la doc fonctionnelle](61-render-functional-doc.md) | writer-functional | 6 |
| [62 — Rendre la doc technique](62-render-technical-doc.md) | writer-technical | 6 |
| [70 — Calculer la couverture](70-compute-coverage.md) | curator | 6 |
| [71 — Vérifier la fraîcheur](71-check-freshness.md) | curator | 7 |

## Les quatre tâches à lire en premier

Si vous ne lisez que quatre tâches, celles-ci portent l'essentiel de ce qui fait la différence entre DMAD et une génération de documentation :

- **[12 — Localiser une fonctionnalité](12-locate-feature.md)** — les cinq sondes. Le seul mode d'échec de la méthode qui ne se voit pas dans le résultat : une documentation parfaite du mauvais périmètre.
- **[41 — Extraire les règles](41-extract-business-rules.md)** — commencer par les contraintes de base (des règles `V` gratuites), et les quatre pièges : calculs, configuration, code mort, surcharge.
- **[50 — Réfuter une claim](50-challenge-claim.md)** — les 9 angles, et pourquoi « trouve ce qui rend ceci faux » ne donne pas le même résultat que « vérifie ceci ».
- **[42 — Reconstituer l'intention](42-reconstruct-intent.md)** — le motif « incident », souvent la découverte la plus utile d'un run.
