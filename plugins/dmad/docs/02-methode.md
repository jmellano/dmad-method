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

---

## Les phases

Chaque phase déclare : ses **entrées**, ses **sorties**, sa **capability** dominante, et si elle se termine par un **gate humain** (⛔ = on ne passe pas sans validation).

### Phase 0 — Cadrage
**Interactif. Facilitateur : agent `Scoper`.**

On ne lance rien avant d'avoir répondu à :
- Quel **mode** ? (`full-scan` ou `feature-scan` — voir §Modes)
- Quel **périmètre** exact (dépôts, dossiers, exclusions : vendor, generated, migrations legacy…) ?
- Quel est le **budget** (tokens, temps, profondeur de traversée) ?
- Quelles **sources non-code** disponibles ? (git complet ou tronqué, Jira/Redmine, wiki, ADR, anciens cahiers des charges, humains encore joignables)
- Quel **vocabulaire métier d'amorce** ? (5–20 termes que le commanditaire utilise : « dossier », « adhérent », « lot », « avoir »…) — c'est la clé d'entrée du `feature-scan`.

**Sortie :** `scope.yaml` + glossaire d'amorce.
**⛔ Gate humain.** Un périmètre mal cadré fait exploser le coût sans rien produire.

---

### Phase 1 — Reconnaissance
**Mécanique. Zéro narration LLM.** Agent `Surveyor`. Modèle : le moins cher possible (Haiku) — il ne fait qu'orchestrer des outils.

Inventaire brut, factuel, non interprété :
- stack, build, gestionnaire de dépendances, versions
- **points d'entrée** : routes HTTP, handlers, commandes CLI, jobs/cron, consumers de queues, listeners d'événements, points d'entrée batch
- arborescence des modules, graphe de dépendances internes
- schéma de données : DDL, migrations, modèles ORM
- intégrations sortantes : clients HTTP, SDK, files, FTP
- tests existants + couverture si disponible
- **hotspots git** : churn × complexité, âge, bus factor par fichier

**Sortie :** `facts/*.json` — 100 % des affirmations en confiance `V`.
**Pourquoi c'est critique :** tout ce qui est établi ici n'aura jamais à être ré-inventé par un LLM. Chaque fait mécanique est un fait que le modèle n'a pas l'occasion d'halluciner.

---

### Phase 2 — Cartographie
Agent `Cartographer`. Capability dominante : `code-intelligence` (LSP).

Construction du **Knowledge Graph** :
- traversée depuis chaque point d'entrée : `callers`/`callees`, implémentations, hiérarchies de types
- flux de données : quelle fonction lit/écrit quelle table, quel champ
- franchissements de frontières : ports, adaptateurs, appels réseau, accès disque
- rattachement de chaque nœud à ses preuves

Le LLM intervient ici pour **nommer et regrouper**, jamais pour inventer une arête. **Une arête du graphe vient d'un outil, pas d'une intuition.**

**Sortie :** `graph/` (voir `05-knowledge-graph.md`).

---

### Phase 3 — Découpage en capacités
Agent `Carver`. Modèle fort (Opus) : c'est un travail de jugement.

- clustering du graphe (cohésion d'appels, co-modification git, partage de tables, vocabulaire)
- proposition de **capacités métier candidates** (« Facturation », « Gestion des droits », « Import fournisseur »)
- identification des *seams* : où le système se coupe proprement
- détection des zones de recouvrement et des dépendances circulaires

**⛔ Gate humain — le plus important de la méthode.** C'est ici qu'un métier corrige en 20 minutes ce que 4 heures d'agents auraient mal deviné. Le découpage proposé est faux quelque part : autant le savoir avant de documenter dessus.

**Sortie :** `capabilities.yaml` (validé).

---

### Phase 4 — Élucidation
Agents `Elucidator` (règles & cas d'usage) et `Archaeologist` (intention).

Par capacité :
- reconstitution des **cas d'usage** (déclencheur → acteur → flux nominal → alternatives → résultat)
- extraction des **règles de gestion** (conditions, seuils, calculs, exceptions)
- **invariants** et **machines à états** (uniquement quand un état réel existe — cf. `06-diagrammes.md`)
- en parallèle, `Archaeologist` fouille git/tickets/noms de tests pour proposer le **pourquoi**

C'est la phase où le LLM produit le plus → **c'est donc la phase la moins fiable**. Tout ce qui en sort est plafonné à `I`, et à `H` pour l'intention.

**Sortie :** claims en attente de challenge.

---

### Phase 5 — Challenge
Agent `Challenger` (adversarial) + `Test Forger`. Modèle fort.

**Le `Challenger` n'écrit pas de documentation. Son unique métier est de faire tomber les affirmations de la phase 4.** Pour chaque claim :
- la preuve citée dit-elle réellement ce qu'on lui fait dire ?
- existe-t-il un chemin de code qui contredit la règle (garde, court-circuit, feature flag, surcharge, config) ?
- l'affirmation est-elle vraie *partout* ou seulement sur le chemin lu ?

Le `Test Forger` prend les règles de gestion les plus critiques et écrit des **characterization tests** : si le test passe sur le code actuel, la règle est prouvée → la claim monte en `V`. **C'est le seul mécanisme qui fait monter la confiance au maximum.**

Sorties possibles par claim : **confirmée** (montée éventuelle) / **dégradée** / **contredite** (→ question ouverte) / **supprimée**.

**Sortie :** claims arbitrées + `tests/characterization/`.
**⛔ Gate humain** sur les contradictions non résolues.

---

### Phase 6 — Restitution
Agents `Diagram Planner`, `Writer:Functional`, `Writer:Technical`, `Curator`.

Génération des deux documentations et des diagrammes **depuis le graphe** — les rédacteurs n'ont pas accès au code, uniquement aux claims validées. C'est volontaire : **on ne peut pas halluciner ce qu'on ne lit pas.**

Le `Curator` passe en dernier : glossaire unifié, dédoublonnage, index, cohérence des renvois, calcul de la couverture.

**Sortie :** `dmad-output/` (voir `07-livrables.md`).

---

### Phase 7 — Maintien
Rejeu périodique : les `evidence` pointent vers `fichier:lignes` + commit. Si le code a bougé, la claim est marquée **périmée** et re-soumise au pipeline. Intégrable en CI.

Sans cette phase, DMAD produit une photo qui jaunit. Avec elle, il produit une documentation vivante.

---

## Les modes

### `full-scan`
Tout le périmètre. Réaliste jusqu'à ~quelques centaines de milliers de lignes selon le budget. Au-delà, la phase 1 (mécanique, peu coûteuse) reste faisable en entier, mais les phases 4–6 doivent être **priorisées par hotspots** : on élucide d'abord les 10 % de code qui concentrent le risque.

### `feature-scan`
Le mode par défaut sur les gros legacy. Le problème central : **trouver les points d'entrée de la feature** sans lire tout le projet.

Stratégie de localisation (par ordre de coût croissant) :
1. **Vocabulaire** — recherche du glossaire d'amorce dans les noms de fichiers, classes, tables, colonnes, routes, libellés d'IHM, messages d'erreur.
2. **Données** — quelles tables portent ce vocabulaire ? Qui les lit/écrit ? Souvent le signal le plus fiable dans un legacy mal nommé.
3. **Historique** — `git log --grep` sur les termes métier et les identifiants de tickets ; les commits d'une même feature se regroupent.
4. **Tests** — les noms de tests sont souvent la seule doc métier survivante.
5. **Surface externe** — routes, écrans, exports, jobs qui mentionnent le domaine.

→ Candidats classés → **⛔ confirmation humaine** → expansion transitive **bornée** (profondeur N, budget, arrêt aux frontières d'infrastructure).

**Règle d'honnêteté :** en `feature-scan`, la doc porte en tête l'avertissement que les interactions hors périmètre n'ont pas été analysées, avec la liste des frontières atteintes et non franchies.

---

## Routage des modèles

Cohérent avec une flotte locale à budget contraint :

| Phase | Agent | Modèle | Pourquoi |
|---|---|---|---|
| 1 | Surveyor | Haiku | orchestration d'outils, zéro jugement |
| 2 | Cartographer | Haiku → Sonnet | traversée mécanique, nommage léger |
| 3 | Carver | **Opus** | jugement structurant, coût d'erreur maximal |
| 4 | Elucidator / Archaeologist | Sonnet | exploration volumineuse |
| 5 | Challenger | **Opus** | adversarial : le maillon qui protège tout le reste |
| 5 | Test Forger | Sonnet | écriture de tests cadrée |
| 6 | Writers / Diagram Planner | Sonnet | rédaction contrainte par le graphe |
| 6 | Curator | Sonnet | cohérence |

Le principe : **le modèle fort est payé là où l'erreur coûte le plus** (le découpage et la réfutation), pas là où le volume est le plus gros.
