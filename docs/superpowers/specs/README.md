# Specs

Documents de conception, du plus général au plus détaillé.

## v0.4 — le corpus à trois documents

| | |
|---|---|
| [Conception v0.4](2026-09-09-dmad-v04-corpus-std-sfd-sfg-design.md) | ce que la v0.4 change et pourquoi — les décisions D15 à D22, le pipeline en trois cycles, le modèle de connaissance, les invariants |
| [Reste à faire — vue d'ensemble](2026-09-09-dmad-reste-a-faire.md) | les cinq parties, leurs dépendances, l'ordre recommandé |

## Les cinq parties, en détail

| | | |
|---|---|---|
| **A** | [Achever la v0.4](2026-09-09-partie-A-achever-v04.md) | contraindre les invariants que la v0.4 a écrits sans les vérifier, les schémas, le run de référence, le `diagram-engine`, la fraîcheur |
| **B** | [Couche de preuve OKF](2026-09-09-partie-B-couche-preuve-okf.md) | le graphe devient un bundle conformant ; la table de correspondance des champs, et la question du placement des documents |
| **C** | [`jcallgraph`](2026-09-09-partie-C-jcallgraph.md) | traversée transitive et franchissement vers les dépendances, sur bytecode ; y compris les angles morts, écrits |
| **D** | [Dette ouverte](2026-09-09-partie-D-dette-ouverte.md) | cinq décisions à trancher, avec leurs options et une recommandation |
| **E** | [Premier run réel](2026-09-09-partie-E-premier-run-reel.md) | le protocole de mesure, les cinq chiffres, et le journal qui en sort |

## L'ordre recommandé

```
A1 → A2 → E (sur un point d'entrée) → B ∥ C → le reste de A
```

La raison est dans la partie E : tant qu'aucun run réel n'a eu lieu, le reste est de l'investissement à l'aveugle — et A1 est ce qui rend un run réel *évaluable* plutôt que simplement raconté.
