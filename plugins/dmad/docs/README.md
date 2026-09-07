# La méthode DMAD

Les documents se lisent dans l'ordre, mais chacun est autonome.

## Le socle
| | |
|---|---|
| [01 — Manifeste](01-manifeste.md) | pourquoi DMAD existe, en quoi ce n'est pas BMAD à l'envers, les 10 principes, l'échelle de confiance `V/C/I/H` |
| [02 — Méthode](02-methode.md) | le double entonnoir, les 8 phases, les gates, les modes `full-scan` / `feature-scan`, le routage des modèles |

## La mécanique
| | |
|---|---|
| [03 — Agents](03-agents.md) | les 12 agents, définis par périmètre de lecture avant persona |
| [04 — Capabilities](04-capabilities.md) | contrats d'outillage, implémentations interchangeables, dégradation qui plafonne la confiance |
| [05 — Knowledge Graph](05-knowledge-graph.md) | 3 strates, format d'une claim, séparation fait / intention |
| [06 — Diagrammes](06-diagrammes.md) | catalogue de 13 vues, règles anti-hairball, le cas des machines à états |
| [07 — Livrables](07-livrables.md) | arborescence de sortie, les 3 artefacts qui font la différence |

## La mise en œuvre
| | |
|---|---|
| [09 — Mettre en œuvre](09-usage.md) | installation du plugin, correspondance avec Claude Code, coût, parallélisation, confidentialité |
| [13 — Profil Java](13-profil-java.md) | où chercher quoi dans un legacy JVM, les pièges Spring/JPA/AOP, la checklist d'avant-run |

## Le recul
| | |
|---|---|
| [08 — Décisions](08-decisions.md) | 10 arbitrages, ce qui a été écarté et pourquoi |
| [10 — Anti-patterns](10-antipatterns.md) | les 13 défaillances de la rétro-documentation par LLM, et leur parade |
| [11 — Glossaire](11-glossaire.md) | le vocabulaire de la méthode, dont l'homonyme assumé « capability » |
| [12 — État et suite](12-roadmap.md) | ce qui existe, ce qui manque, ce que DMAD ne deviendra pas |

## Par où commencer

**Pour comprendre l'idée** → [01 — Manifeste](01-manifeste.md), section 2 (la différence fondamentale avec BMAD).

**Pour juger si la méthode tient** → [10 — Anti-patterns](10-antipatterns.md). Chaque contrainte de DMAD y trouve la défaillance qu'elle empêche ; c'est le document qui justifie les choix qui paraissent excessifs isolément.

**Pour voir à quoi ça ressemble** → [le run de référence](../examples/atlas-billing/).

**Pour l'utiliser** → [09 — Mettre en œuvre](09-usage.md), puis le [profil Java](13-profil-java.md) si c'est un projet JVM.
