# La méthode DMAD

Les documents se lisent dans l'ordre, mais chacun est autonome.

## Le socle
| | |
|---|---|
| [01 — Manifeste](01-manifeste.md) | pourquoi DMAD existe, en quoi ce n'est pas BMAD à l'envers, les 10 principes, l'échelle de confiance `V/C/I/H` |
| [02 — Méthode](02-methode.md) | le double entonnoir, le corpus STD → SFD → SFG, les trois cycles et leurs revues, les modes `full-scan` / `feature-scan`, le routage des modèles |

## La mécanique
| | |
|---|---|
| [03 — Agents](03-agents.md) | les agents, définis par périmètre de lecture avant persona, et l'échelle de lecture des trois rédacteurs |
| [04 — Capabilities](04-capabilities.md) | contrats d'outillage, implémentations interchangeables, dégradation qui plafonne la confiance |
| [05 — Knowledge Graph](05-knowledge-graph.md) | 3 strates, format d'une claim, séparation fait / intention |
| [06 — Diagrammes](06-diagrammes.md) | les quatre diagrammes cardinaux, catalogue large, seuils paramétrables, le cas des machines à états |
| [07 — Livrables](07-livrables.md) | le corpus à trois documents, les dix-sept sections de la STD, les 3 artefacts qui font la différence |

## La mise en œuvre
| | |
|---|---|
| [09 — Mettre en œuvre](09-usage.md) | installation du plugin, correspondance avec Claude Code, coût, parallélisation, confidentialité |
| [13 — Profil Java](13-profil-java.md) | où chercher quoi dans un legacy JVM, les pièges Spring/JPA/AOP, la checklist d'avant-run |

## Le recul
| | |
|---|---|
| [08 — Décisions](08-decisions.md) | les arbitrages, ce qui a été écarté et pourquoi — dont D15 à D22, qui fondent la v0.4 |
| [10 — Anti-patterns](10-antipatterns.md) | les 13 défaillances de la rétro-documentation par LLM, et leur parade |
| [11 — Glossaire](11-glossaire.md) | le vocabulaire de la méthode, dont l'homonyme assumé « capability » |
| [12 — État et suite](12-roadmap.md) | ce qui existe, ce qui manque, ce que DMAD ne deviendra pas |

## Par où commencer

**Pour comprendre l'idée** → [01 — Manifeste](01-manifeste.md), section 2 (la différence fondamentale avec BMAD).

**Pour juger si la méthode tient** → [10 — Anti-patterns](10-antipatterns.md). Chaque contrainte de DMAD y trouve la défaillance qu'elle empêche ; c'est le document qui justifie les choix qui paraissent excessifs isolément.

**Pour voir à quoi ça ressemble** → [le run de référence](../examples/atlas-billing/).

**Pour l'utiliser** → [09 — Mettre en œuvre](09-usage.md), puis le [profil Java](13-profil-java.md) si c'est un projet JVM.

## Les outils

| | |
|---|---|
| `tools/validate.py` | les artefacts contre leurs schémas, plus les règles croisées |
| `tools/check-corpus.py` | les documents contre D16, D17, D20, R1, R3 et les sept blocs |
| `tools/diagram-engine.py` | rend un diagramme depuis son plan, le compte, et refuse au-delà du seuil |
| `tools/freshness.py` | ce qui a péri, et la propagation vers le haut de la cascade |
| `tools/coverage.py` | les chiffres du rapport de couverture ; l'interprétation reste écrite |
| `tools/selftest.sh` | prouve que les garde-fous refusent bien ce qu'ils doivent refuser |

> Un principe qui n'est pas contraint par un outil est un vœu pieux, et chaque message d'erreur nomme la décision qu'il applique — un message qui ne dit pas quelle règle il fait respecter se fait contourner, puis supprimer, au premier agacement.

## Les skills embarqués

Deux prérequis, consommés par plusieurs agents, disponibles dans `../skills/` :

- [`code-intelligence-java`](../skills/code-intelligence-java/SKILL.md) — le protocole de démarrage de l'indexeur sémantique et la chaîne de ses quatre causes d'échec. À lire **avant** la première invocation.
- [`patterns-gof-cqrs`](../skills/patterns-gof-cqrs/SKILL.md) — reconnaître les patrons pour découper juste, et savoir où ils ont le droit d'apparaître dans le corpus.
