# DMAD — Diagrammes

## L'arbitrage de départ

La demande est claire : **beaucoup** de diagrammes, UML et au-delà — classes, états, séquence, entrées/sorties de chaque étape, ports & adaptateurs, base de données, appels API, dépendances de services.

L'intention est la bonne : sur un legacy, un schéma vaut trente pages. Mais « beaucoup de diagrammes » se retourne systématiquement de deux façons :

- **Le hairball.** Un diagramme de classes généré sur un legacy de 400 classes est un nuage de flèches que personne n'ouvre deux fois. Ce n'est pas de la documentation, c'est une capture d'écran de la complexité.
- **Le diagramme sans question.** Généré parce qu'on peut, pas parce que quelqu'un se demandait quelque chose. Il occupe de la place, vieillit, et fait douter du reste.

DMAD garde donc l'ambition — **beaucoup de diagrammes** — mais l'encadre par quatre règles qui font la différence entre une doc dense et une doc bruyante.

## Les quatre règles

**R1 — Un diagramme = une question.** Le `Diagram Planner` doit écrire la question avant de générer. La question est affichée **au-dessus** du diagramme dans la doc. Pas de question formulable ⇒ pas de diagramme.

**R2 — Seuil de lisibilité, paramétrable.** Au-delà du seuil, on ne simplifie pas : on **découpe en plusieurs diagrammes**, chacun avec sa propre question. Un diagramme illisible est une non-livraison.

Les seuils sont déclarés dans `scope.yaml` (D15). Valeurs par défaut, sur trois indicateurs cumulés :

| Indicateur | Défaut | Ce qu'il mesure |
|---|---|---|
| Nœuds `N` | ≤ 12 (≤ 12 participants en séquence) | au-delà, l'œil ne suit plus |
| Arêtes `E` | ≤ 15 | la densité de liens, qui sature avant le nombre de nœuds |
| Complexité de McCabe | ≤ 10 | les chemins linéairement indépendants du graphe de contrôle |

**Le nombre de niveaux d'abstraction n'est pas un choix : c'est la sortie de cette contrainte.** On ajoute un niveau chaque fois que les indicateurs dépassent le seuil — autant de niveaux qu'il en faut, ni plus (empilement inutile) ni moins (diagramme illisible).

C'est l'arbitrage entre les deux leviers de décomposition. La **longueur** est la séquence d'opérations d'un niveau donné ; la **profondeur** est l'empilement des niveaux. Un diagramme trop long se répare en décomposant certaines étapes en sous-niveau — on convertit de la longueur en profondeur. Un empilement de sous-niveaux triviaux se répare en fusionnant — l'inverse. Les deux leviers ne se substituent pas : ils s'ajustent en tension.

**R3 — Généré depuis le graphe, jamais rédigé.** Les agents décrivent un sous-graphe + une intention dans un **plan** ; `tools/diagram-engine.py` rend. Un diagramme ne peut donc pas contredire la doc — les deux sortent de la même source. Et chaque diagramme hérite du **badge de confiance** de son sous-graphe.

La figure rendue porte un **marqueur** qui cite son plan et ses métriques :

```
<!-- diagram: DIA-STD-001 · N=8 E=7 McCabe=1 -->
```

`check-corpus.py` s'en sert pour deux contrôles : un diagramme sans marqueur a été écrit à la main, et un diagramme dont le contenu diverge de son plan a été retouché après rendu. **C'est ce qui rend R3 opposable** — sans quoi elle reste une consigne que rien ne vérifie.

**R4 — Nommé par ce qu'il montre, jamais par son type.** « Diagramme de séquence 3 » ne dit rien ; « Échanges du calcul de refacturation avec les services amont » dit à quoi sert la figure avant qu'on la regarde. Le type de rendu est un détail d'implémentation qui n'a rien à faire dans un titre.

## Les quatre diagrammes cardinaux

Avant le catalogue large, quatre types portent l'essentiel de la charge et répondent chacun à une question précise. **Utiliser le bon outil pour la bonne question**, pas le même à toutes les sauces.

| Diagramme | Répond à | Quand |
|---|---|---|
| **flowchart** | quels traitements et quels contrôles, dans quel ordonnancement, avec quels objets métier en entrée et en sortie de chaque étape | l'enchaînement des opérations d'un niveau — c'est l'outil du levier *longueur* |
| **sequenceDiagram** | quels objets métier, depuis quelles sources et vers quels puits, dans quel ordre temporel | les échanges entre le processus et le monde extérieur — un participant par acteur externe |
| **stateDiagram** | quels états d'un objet métier, et par quel traitement on transite | un objet à cycle de vie réel — **jamais systématique** |
| **erDiagram** | quelles relations entre objets métier, établies à quel moment, servant à quel contrôle | plusieurs objets en persistance dont les relations portent de l'information |

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
