# Templates DMAD

Gabarits de sortie. Syntaxe de substitution volontairement neutre (`{{}}`) — le moteur de rendu est un détail d'implémentation.

| Template | Utilisé par | Sortie |
|---|---|---|
| [`doc-header.md`](doc-header.md) | tous les rédacteurs | bandeau obligatoire |
| [`std.md`](std.md) | writer-std | une STD, dix-sept sections |
| [`sfd.md`](sfd.md) | writer-sfd | une SFD, vue récursive par business object |
| [`sfg.md`](sfg.md) | writer-sfg | une SFG, sept blocs par cas d'usage |
| [`capability-summary.md`](capability-summary.md) | writer-sfd | chapitre d'une capacité |
| [`use-case.md`](use-case.md) | writer-sfg | un cas d'usage |
| [`module-sheet.md`](module-sheet.md) | writer-std | fiche de module |
| [`glossary.md`](glossary.md) | curator | glossaire métier ↔ code |
| [`open-questions.md`](open-questions.md) | curator | registre priorisé |
| [`coverage-report.md`](coverage-report.md) | curator | rapport de couverture |
| [`seams.md`](seams.md) | writer-std | points de découpe |

## Les sections qui ne s'omettent jamais

Trois sections sont obligatoires **même vides**, auquel cas elles affichent explicitement « aucune » :

- « À confirmer par le métier »
- « Ce qui n'a pas été analysé »
- « Limites de cette analyse » (STD)
- « Ce qui n'est pas couvert » (SFG, par cas d'usage) — celle-ci ne peut pas être vide : un cas d'usage sans frontière écrite ne peut être l'unité d'évolution de rien

Une section absente se lit « rien à signaler ». Une section vide et assumée se lit « on a regardé ». La différence est exactement celle entre une documentation honnête et une documentation qui inspire une confiance qu'elle n'a pas méritée.
