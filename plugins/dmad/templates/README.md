# Templates DMAD

Gabarits de sortie. Syntaxe de substitution volontairement neutre (`{{}}`) — le moteur de rendu est un détail d'implémentation.

| Template | Utilisé par | Sortie |
|---|---|---|
| [`doc-header.md`](doc-header.md) | tous les rédacteurs | bandeau obligatoire |
| [`capability-summary.md`](capability-summary.md) | writer-functional | chapitre d'une capacité |
| [`use-case.md`](use-case.md) | writer-functional | un cas d'usage |
| [`module-sheet.md`](module-sheet.md) | writer-technical | fiche de module |
| [`glossary.md`](glossary.md) | curator | glossaire métier ↔ code |
| [`open-questions.md`](open-questions.md) | curator | registre priorisé |
| [`coverage-report.md`](coverage-report.md) | curator | rapport de couverture |
| [`seams.md`](seams.md) | writer-technical | points de découpe |

## Les sections qui ne s'omettent jamais

Trois sections sont obligatoires **même vides**, auquel cas elles affichent explicitement « aucune » :

- « À confirmer par le métier »
- « Ce qui n'a pas été analysé »
- « Limites de cette analyse » (doc technique)

Une section absente se lit « rien à signaler ». Une section vide et assumée se lit « on a regardé ». La différence est exactement celle entre une documentation honnête et une documentation qui inspire une confiance qu'elle n'a pas méritée.
