# DMAD — La méthode

## Le double entonnoir

L'erreur intuitive serait de dérouler BMAD à l'envers : code → stories → archi → PRD. Ça ne marche pas, parce qu'on ne peut pas remonter au métier sans d'abord savoir **où regarder**, et qu'on ne sait pas où regarder sans une première idée du métier.

DMAD procède donc en **double entonnoir itératif** :

```
        MÉCANIQUE (bottom-up)              INTERPRÉTATIF (top-down)
        ─────────────────────              ────────────────────────
  code ─► faits ─► graphe ─► clusters ─► capacités ─► cas d'usage ─► règles
                                  ▲                                    │
                                  └──────── ré-vérification ───────────┘
```

Ce qui monte est **mécanique et prouvé**. Ce qui redescend est **interprétatif et doit être re-confronté au code**. La boucle tourne jusqu'à ce que les contradictions soient épuisées ou consignées.

## Le corpus à trois documents

Depuis la v0.4, la remontée se matérialise en **trois documents en cascade d'abstraction**, et non plus en deux rendus parallèles du même graphe.

```
code ──────► STD ──────► SFD ──────► SFG
             technique    fonctionnel   métier
             détaillée    détaillée     générale

             un point     un arbre de   un cas
             d'entrée     business obj. d'usage
```

| | STD | SFD | SFG |
|---|---|---|---|
| Lecteur | développeur, architecte, ops | analyste, MOE, MOA | utilisateur métier, PO |
| Question | « comment, et où je touche ? » | « que fait le processus, avec quelles données ? » | « qu'est-ce que je peux attendre du système ? » |
| Unité | le point d'entrée | l'arbre de business objects | le cas d'usage |
| Lit | le graphe et les claims | la STD et les claims | la SFD |
| Vocabulaire | technique, noms réels du code | métier, noms fonctionnels | métier exclusivement |
| Références | `fichier:lignes`, signatures | vers les niveaux et les business objects | vers les cas d'usage |
| Interdits | **blocs de code, blocs SQL** | idem + noms de classes | idem + toute trace de technique |

**Chaque étage est aveugle à l'étage n−2** (D17). La SFD ne lit pas le code ; la SFG ne lit ni le code ni le graphe. C'est la contrainte D3 de la v0.3 — « les rédacteurs n'ont pas accès au code » — généralisée en échelle de lecture. Elle garantit que chaque niveau est réellement une **abstraction** du précédent, et non une seconde lecture indépendante du même matériau : deux lectures indépendantes divergent, une abstraction non.

**Aucun des trois ne contient de bloc de code** (D16). La STD porte des références — `fichier:lignes`, signatures de méthodes, noms de tables et de colonnes. La SFD et la SFG ignorent jusqu'à l'existence du code.

---

## Les cycles

Chaque document est produit par un **cycle complet** — enquête, challenge, rédaction — scellé par une **revue humaine** qui peut demander corrections et compléments. Le cycle suivant ne démarre pas sur un document non figé (D19).

### Cycle 0 — Cadrage
**Interactif. Facilitateur : agent `Scoper`.**

On ne lance rien avant d'avoir répondu à :
- Quel **mode** ? (`full-scan` ou `feature-scan` — voir §Modes)
- **Jusqu'où va-t-on ?** STD seule, jusqu'à la SFD, ou le corpus complet. C'est une question de budget autant que de besoin : une STD seule est un livrable qui se défend.
- Quel **périmètre** exact (dépôts, dossiers, exclusions : vendor, generated, migrations legacy…) ?
- Quel est le **budget** (tokens, temps, profondeur de traversée) ?
- Quels **seuils de lisibilité** ? Défaut : N ≤ 12 nœuds, E ≤ 15 arêtes, McCabe ≤ 10 (D15).
- Quel **profil** ? Langage, gestionnaire de dépendances, et conventions locales de contrat d'API — sans quoi la résolution des appels sortants n'a pas de cible.
- Quelles **sources non-code** disponibles ? (git complet ou tronqué, Jira/Redmine, wiki, ADR, anciens cahiers des charges, humains encore joignables)
- Quel **vocabulaire métier d'amorce** ? (5–20 termes que le commanditaire utilise : « dossier », « adhérent », « lot », « avoir »…) — c'est la clé d'entrée du `feature-scan`.

**Sortie :** `scope.yaml` + glossaire d'amorce.
**⛔ Gate humain.** Un périmètre mal cadré fait exploser le coût sans rien produire.

---

## Cycle 1 — La STD

**Registre mécanique.** Tout ce qui s'y établit est un fait outillé, et tout ce qui s'y établit n'aura jamais à être ré-inventé par un modèle aux étages supérieurs.

### 1.1 Reconnaissance
Agent `Surveyor`. Modèle : le moins cher possible — il ne fait qu'orchestrer des outils.

Inventaire brut, factuel, non interprété :
- stack, build, gestionnaire de dépendances, versions
- **résolution des dépendances** — sur un projet compilé, c'est le prérequis de tout le reste : un projet qui ne résout pas ses dépendances donne un run plafonné à `I`, et ça se déclare
- **protocole de démarrage de l'indexeur sémantique** — voir `13-profil-java.md`, dont la leçon générale est qu'un indexeur qui répond vide au premier appel n'est pas en panne, il chauffe
- **points d'entrée** : routes HTTP, handlers, commandes CLI, jobs/cron, consumers de queues, listeners d'événements, points d'entrée batch
- arborescence des modules, graphe de dépendances internes
- schéma de données : DDL, migrations, modèles ORM
- intégrations sortantes : clients HTTP, SDK, files, FTP
- tests existants + couverture si disponible
- **hotspots git** : churn × complexité, âge, bus factor par fichier

**Sortie :** `facts/*.json` — 100 % des affirmations en confiance `V`.

### 1.2 Cartographie
Agent `Cartographer`. Capability dominante : `code-intelligence`.

Construction du **Knowledge Graph** :
- traversée **transitive** depuis chaque point d'entrée : `callers`/`callees`, implémentations, hiérarchies de types
- **typage des feuilles** : accès base de données, événement publié ou consommé, contrat sortant, fichier, notification. Une feuille non typée est une traversée inachevée
- flux de données : quelle fonction lit/écrit quelle table, quel champ
- franchissements de frontières : ports, adaptateurs, appels réseau, accès disque
- rattachement de chaque nœud à ses preuves

Le LLM intervient ici pour **nommer et regrouper**, jamais pour inventer une arête. **Une arête du graphe vient d'un outil, pas d'une intuition.**

**Sortie :** `graph/`, `boundaries.yaml`.

### 1.3 Résolution des contrats sortants
Agent `Contract Resolver`. **Nouveau en v0.4.**

Un appel sortant vers un service tiers porte un code de contrat qui est la clé d'entrée de son exploitation : c'est par lui qu'on retrouve le propriétaire, la supervision et le contrat lui-même. Le trouver n'est pas une commodité — c'est la moitié de la valeur de la section « appels externes » de la STD.

Le code se lit à quatre endroits de fiabilité très inégale, et **la confiance est dérivée du barreau atteint** :

| Barreau | Source | Confiance | Ce qu'il vaut |
|---|---|---|---|
| 1 | l'annotation de contrat, dans l'artefact de la dépendance | `V` | fait foi — donne aussi le verbe, la route et le nom d'opération |
| 2 | la Javadoc de l'interface de dépendance | `C` | générée depuis la même source, mais c'est un commentaire |
| 3 | un commentaire dans le code appelant | `I` | écrit à la main : survit à un refactoring et ment alors sans le dire |
| 4 | le placeholder | — | n'affirme rien, et c'est sa vertu |

**Chercher jusqu'au barreau le plus haut atteignable, et écrire lequel a servi.** Un placeholder visible vaut mieux qu'un code plausible : le premier se corrige, le second se propage.

Chaque contrat résolu devient un nœud `ExternalContract`, feuille du graphe au même titre qu'un accès base de données, portant **obligatoirement la version de l'artefact** où le contrat a été lu (D18) — le contrat décrit ce que le module consomme, pas ce que le module appelé publie aujourd'hui.

**Sortie :** `contracts/`.

### 1.4 Challenge technique
Agent `Challenger`, angles du registre mécanique :
- un aspect ou un intercepteur modifie-t-il le comportement d'une méthode sans la mentionner ?
- l'implémentation injectée est-elle celle que la traversée a supposée, ou seulement l'une des candidates ?
- la configuration diffère-t-elle entre les environnements ?
- le chemin d'erreur a-t-il été traversé, ou seulement le chemin nominal ?
- l'affirmation d'exhaustivité est-elle soutenue par l'outillage réellement disponible ?

### 1.5 Rédaction
Agents `Diagram Planner` puis `Writer:STD`.

Dix-sept sections imposées, dans un ordre fixe, **jamais omises** : une section dont le sujet n'existe pas dans le point d'entrée se remplit avec le constat d'absence et son périmètre. Un résultat négatif explicite fait gagner du temps au lecteur ; une section absente le pousse à chercher lui-même. Le détail est dans `07-livrables.md`.

**⛔ Revue humaine — `revue-cycle-1-std`.** Corrections et compléments, puis la STD est figée. C'est elle qui devient l'entrée du cycle 2.

---

## Cycle 2 — La SFD

**Registre interprétatif borné.** On quitte le fait outillé pour le sens, et la confiance plafonne en conséquence.

### 2.1 Découpage en capacités et en business objects
Agent `Carver`. Modèle fort : c'est un travail de jugement.

- clustering du graphe (cohésion d'appels, co-modification git, partage de tables, vocabulaire)
- proposition de **capacités métier candidates** (« Facturation », « Gestion des droits », « Import fournisseur »)
- reconnaissance des **patrons de conception** qui structurent le processus — prérequis à l'identification des business objects, parce qu'un Template Method ou une Strategy déterminent où sont les vrais nœuds d'orchestration
- identification des **business objects** : les nœuds qui conjuguent plusieurs feuilles externes ou plusieurs sous-objets, filtrés par pertinence métier, **nommés par leur sens fonctionnel et non par leur méthode d'origine**
- identification des *seams* : où le système se coupe proprement
- détection des zones de recouvrement et des dépendances circulaires

**⛔ Gate humain — `gate-3-capabilities`, le plus important de la méthode.** C'est ici qu'un métier corrige en 20 minutes ce que quatre heures d'agents auraient mal deviné. Le découpage proposé est faux quelque part : autant le savoir avant de documenter dessus. Depuis la v0.4 il se tient **après** la revue de la STD (D21), donc devant un expert qui vient de lire la carte technique.

**Sortie :** `capabilities.yaml` (validé), `business-objects/`.

### 2.2 Élucidation
Agents `Elucidator` et, en parallèle, préparation de l'`Archaeologist` pour le cycle 3.

Par capacité :
- reconstitution des **cas d'usage** (déclencheur → acteur → flux nominal → alternatives → résultat)
- extraction des **règles de gestion** (conditions, seuils, calculs, exceptions)
- **classification ISO 25010** de chaque opération et de chaque donnée :
  - opération de **traitement** (elle transforme) ou de **contrôle** (elle branche et orchestre)
  - donnée à but de **traitement** — **initiale** si présente en entrée, **ad-hoc** si chargée en cours d'exécution — ou donnée à but de **contrôle**
  - sortie **normale** ou **anormale**
- **invariants** et **machines à états** (uniquement quand un état réel existe — cf. `06-diagrammes.md`)
- assignation des **niveaux d'abstraction** : à chaque business object, sa profondeur récursive et sa couche métier

La distinction traitement/contrôle n'est pas cosmétique : elle change ce qu'on documente d'une opération. Et la distinction initiale/ad-hoc est le signal le plus rentable pour un lecteur qui cherche une opportunité d'optimisation — une donnée ad-hoc chargée dans une boucle est un appel par itération.

C'est la phase où le LLM produit le plus → **c'est donc la phase la moins fiable**. Tout ce qui en sort est plafonné à `I`.

### 2.3 Challenge interprétatif et preuve
Agents `Challenger` puis `Test Forger`.

Pour chaque claim : la preuve citée dit-elle réellement ce qu'on lui fait dire ? Existe-t-il un chemin de code qui contredit la règle ? L'affirmation est-elle vraie *partout* ou seulement sur le chemin lu ?

Le `Test Forger` prend les règles les plus critiques et écrit des **characterization tests**. Si le test passe sur le code actuel, la règle est prouvée → la claim monte en `V`. **C'est le seul mécanisme qui fait monter la confiance au maximum.**

### 2.4 Rédaction
Agents `Diagram Planner` puis `Writer:SFD`.

**On analyse bas → haut, on rédige haut → bas.** L'analyse part des feuilles et remonte vers la racine : c'est comme ça qu'on découvre un processus qu'on ne connaît pas. La rédaction présente le niveau le plus haut d'abord et descend : c'est comme ça qu'un lecteur le comprend. Confondre les deux produit un document où le lecteur se noie dans le détail avant d'avoir le contexte.

**⛔ Revue humaine — `revue-cycle-2-sfd`.** Corrections et compléments, puis la SFD est figée.

---

## Cycle 3 — La SFG

**Registre métier.** La SFG ne se dérive pas du code : elle se dérive de la SFD, et n'a rien à lire tant que celle-ci n'est pas fiable.

### 3.1 Intention
Agent `Archaeologist`. Il fouille git, tickets, ADR, wiki, noms de tests et fichiers supprimés pour proposer le **pourquoi**.

Plafond `H`, **sans exception**. Seule une validation humaine tracée peut le faire monter. C'est le seul agent qui approche l'intention, et c'est le seul apport propre de la SFG : la seule information du corpus qu'aucune relecture de code ne produira jamais, puisqu'elle vient du métier.

### 3.2 Contrôle de cohérence — bloquant
Agent `Curator`.

**Une contradiction laissée dans la SFD devient une promesse fausse faite à l'utilisateur**, et le lecteur de la SFG n'a aucun moyen de la détecter — il n'a ni le code, ni le graphe, ni la STD. C'est le risque propre du troisième document, et il est asymétrique : une erreur de STD se corrige devant un développeur qui la repère, une erreur de SFG se découvre en production, chez un utilisateur qui avait cru.

Toute contradiction non résolue dans la SFD **bloque** la production de la SFG. Elle ne la dégrade pas : elle la bloque.

### 3.3 Rédaction
Agents `Elucidator` (arbitrage des règles partagées entre cas d'usage, traduction du vocabulaire) puis `Writer:SFG`.

Sept blocs par cas d'usage, un index inverse règle → cas d'usage, et rien qui trahisse l'existence d'un système informatique derrière.

**⛔ Revue humaine — `revue-cycle-3-sfg`.**

---

## Maintien

Rejeu périodique : les `evidence` pointent vers `fichier:lignes` + commit. Si le code a bougé, la claim est marquée **périmée** et re-soumise. La péremption se propage vers le haut : une claim de STD périmée périme les sections de SFD qui en dérivent, et ainsi de suite. Intégrable en CI.

Sans cette phase, DMAD produit une photo qui jaunit. Avec elle, il produit une documentation vivante.

---

## Les modes

### `full-scan`
Tout le périmètre. Réaliste jusqu'à ~quelques centaines de milliers de lignes selon le budget. Au-delà, le cycle 1 (mécanique, peu coûteux) reste faisable en entier, mais les cycles 2 et 3 doivent être **priorisés par hotspots** : on élucide d'abord les 10 % de code qui concentrent le risque.

### `feature-scan`
Le mode par défaut sur les gros legacy. Le problème central : **trouver les points d'entrée de la feature** sans lire tout le projet.

Stratégie de localisation (par ordre de coût croissant) :
1. **Vocabulaire** — recherche du glossaire d'amorce dans les noms de fichiers, classes, tables, colonnes, routes, libellés d'IHM, messages d'erreur.
2. **Données** — quelles tables portent ce vocabulaire ? Qui les lit/écrit ? Souvent le signal le plus fiable dans un legacy mal nommé.
3. **Historique** — `git log --grep` sur les termes métier et les identifiants de tickets ; les commits d'une même feature se regroupent.
4. **Tests** — les noms de tests sont souvent la seule doc métier survivante.
5. **Surface externe** — routes, écrans, exports, jobs qui mentionnent le domaine.

→ Candidats classés → **⛔ confirmation humaine** → expansion transitive **bornée** (profondeur N, budget, arrêt aux frontières d'infrastructure).

**Règle d'honnêteté :** en `feature-scan`, chaque document du corpus porte en tête l'avertissement que les interactions hors périmètre n'ont pas été analysées, avec la liste des frontières atteintes et non franchies.

---

## Critère d'arrêt

Le budget épuisé s'arrête sur un **document terminé**, jamais au milieu d'un cycle. C'est la généralisation de la règle qui valait déjà pour les capacités : une capacité documentée en entier vaut mieux que six ébauches, et une STD revue vaut mieux qu'une SFD à moitié écrite sur une STD qui ne l'a pas été.

---

## Routage des modèles

| Cycle | Agent | Modèle | Pourquoi |
|---|---|---|---|
| 1 | Surveyor | Haiku | orchestration d'outils, zéro jugement |
| 1 | Cartographer | Haiku → Sonnet | traversée mécanique, nommage léger |
| 1 | Contract Resolver | Haiku | lecture d'archives et d'annotations, zéro jugement |
| 1 | Challenger | **Opus** | adversarial |
| 1 | Writer:STD | Sonnet | rédaction contrainte par le graphe |
| 2 | Carver | **Opus** | jugement structurant, coût d'erreur maximal |
| 2 | Elucidator | Sonnet | exploration volumineuse |
| 2 | Challenger | **Opus** | le maillon qui protège tout le reste |
| 2 | Test Forger | Sonnet | écriture de tests cadrée |
| 2 | Writer:SFD | Sonnet | rédaction contrainte par la STD |
| 3 | Archaeologist | Sonnet | fouille volumineuse, plafond `H` de toute façon |
| 3 | Curator | Sonnet | cohérence |
| 3 | Writer:SFG | Sonnet | rédaction contrainte par la SFD |
| 1, 2 | Diagram Planner | Sonnet | plan contraint par les seuils |

Le principe : **le modèle fort est payé là où l'erreur coûte le plus** (le découpage et la réfutation), pas là où le volume est le plus gros.
