# DMAD — Diagrammes

## L'arbitrage de départ

La demande est claire : **beaucoup** de diagrammes, UML et au-delà — classes, états, séquence, entrées/sorties de chaque étape, ports & adaptateurs, base de données, appels API, dépendances de services.

L'intention est la bonne : sur un legacy, un schéma vaut trente pages. Mais « beaucoup de diagrammes » se retourne systématiquement de deux façons :

- **Le hairball.** Un diagramme de classes généré sur un legacy de 400 classes est un nuage de flèches que personne n'ouvre deux fois. Ce n'est pas de la documentation, c'est une capture d'écran de la complexité.
- **Le diagramme sans question.** Généré parce qu'on peut, pas parce que quelqu'un se demandait quelque chose. Il occupe de la place, vieillit, et fait douter du reste.

DMAD garde donc l'ambition — **beaucoup de diagrammes** — mais l'encadre par trois règles qui font la différence entre une doc dense et une doc bruyante.

## Les trois règles

**R1 — Un diagramme = une question.** Le `Diagram Planner` doit écrire la question avant de générer. La question est affichée **au-dessus** du diagramme dans la doc. Pas de question formulable ⇒ pas de diagramme.

**R2 — Seuil de lisibilité.** Au-delà de **~20 nœuds** (~12 pour une séquence), on ne simplifie pas : on **découpe en plusieurs diagrammes**, chacun avec sa propre question. Un diagramme illisible est une non-livraison.

**R3 — Généré depuis le graphe, jamais rédigé.** Les agents décrivent un sous-graphe + une intention ; le `diagram-engine` rend. Un diagramme ne peut donc pas contredire la doc — les deux sortent de la même source. Et chaque diagramme hérite du **badge de confiance** de son sous-graphe.

## Catalogue

Le catalogue est volontairement large : c'est la densité qui est recherchée, chaque vue répondant à une question distincte.

| Question du lecteur | Diagramme | Source dans le graphe | Public |
|---|---|---|---|
| À quoi sert ce système, pour qui ? | **C4 Contexte** | Capability, Actor, ExternalService | Fonctionnel |
| De quoi dépend-il ? | **C4 Conteneurs** + graphe de dépendances | Module, ExternalService, DataStore | Technique |
| Comment est-ce structuré à l'intérieur ? | **C4 Composants** (par capacité) | Component, belongs_to | Technique |
| Comment se déroule *ce* cas d'usage ? | **Séquence** (une par UC) | UseCase → calls | Les deux |
| Que se passe-t-il de bout en bout côté métier ? | **Activité / BPMN-lite** avec couloirs | UseCase, Actor | Fonctionnel |
| Quelles données, quelles relations ? | **ERD** (par capacité) | Table, Column, FK | Les deux |
| Quel est le cycle de vie de cet objet ? | **Machine à états** | StateMachine, State | Les deux |
| Où sont les ports et les adaptateurs ? | **Composants hexagonaux** | Component + franchissements | Technique |
| Qu'est-ce qui appelle quoi depuis cette entrée ? | **Call graph borné** (profondeur ≤ 3) | Entrypoint → calls | Technique |
| Qu'est-ce qui entre et sort de cette étape ? | **Data flow / IPO** | reads, writes, publishes | Les deux |
| Quelles API externes, avec quels contrats ? | **Tableau + séquence d'intégration** | ApiCall, ExternalService | Technique |
| Où est le risque, où est la dette ? | **Treemap de hotspots** | Hotspot (churn × complexité) | Technique |
| Comment ces classes s'articulent ? | **Classes — par capacité uniquement** | Class, extends, implements | Technique |

**Le diagramme de classes est le seul explicitement bridé** : jamais global, toujours borné à une capacité validée, toujours sous le seuil R2. C'est la seule vue dont la version « tout le projet » est garantie inutile.

## Machines à états : la règle stricte

Une machine à états n'est générée **que si un état réel est détectable** :
- un champ `status`/`state`/`etat` (colonne, enum, constante) **et**
- des transitions repérables dans le code (affectations de ce champ, gardes).

Sinon, ce n'est pas un cycle de vie : c'est le modèle qui invente une machine plausible. Ce cas précis — un automate élégant, cohérent, et totalement imaginaire — est l'une des hallucinations les plus convaincantes et les plus dangereuses en rétro-documentation. **Pas de champ d'état ⇒ pas de diagramme d'états ⇒ une question ouverte à la place.**

## Formats

- **Mermaid** par défaut : versionnable dans git, diffable, rendu nativement par GitHub/GitLab, lisible en texte brut par un agent.
- **PlantUML** quand Mermaid ne suffit pas (séquences complexes, composants hexagonaux, notations UML fines).
- **Graphviz** pour les graphes générés à grande échelle (dépendances, call graphs).
- Le rendu image est un artefact de build, **jamais** la source versionnée.

## Badge de confiance sur les diagrammes

Un diagramme dérivé de claims `I` est un diagramme `I`. Il porte le badge, comme un chapitre :

```
> **Question :** que se passe-t-il quand un avoir est émis sur une facture déjà transmise ?
> **Confiance : I — inféré** · 2 chemins non explorés (hors périmètre) · voir OQ-018
```

Sans ce badge, un joli diagramme se lit comme une vérité établie. Un diagramme est **plus persuasif** qu'un paragraphe — c'est précisément pour ça qu'il doit porter son niveau de preuve.
