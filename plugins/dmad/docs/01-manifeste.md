# DMAD — Manifeste

> **DMAD** — *Documentation Method for Agentic Discovery*
> Le pendant inverse de [BMAD](https://github.com/bmad-code-org/BMAD-METHOD) : là où BMAD descend d'une intention vers du code, DMAD remonte d'un code existant vers une intention documentée — fonctionnelle **et** technique.

## 1. Pourquoi DMAD existe

Un projet legacy est un système dont **le comportement est connu de la machine et inconnu des humains**. Le code tourne, il facture, il expédie, il calcule des droits — et plus personne ne sait pourquoi il le fait comme ça. Les gens qui savaient sont partis. La doc, si elle existe, ment.

Le résultat est toujours le même : on n'ose plus toucher. Chaque évolution coûte trois fois son prix parce qu'on paie d'abord la ré-investigation.

**DMAD existe pour transformer un code opaque en une connaissance exploitable, traçable et vérifiable — par les métiers comme par les développeurs.**

## 2. La différence fondamentale avec BMAD

Ce n'est pas une symétrie. C'est une inversion de nature.

| | BMAD | DMAD |
|---|---|---|
| Sens | Intention → code | Code → intention |
| Nature | **Génératif** | **Investigatif** |
| Vérité terrain | N'existe pas encore, on la crée | Existe déjà, elle nous contredit |
| Risque principal | Incohérence entre artefacts | **Documentation plausible et fausse** |
| Critère de qualité | Le code compile et passe les tests | **Chaque affirmation est prouvée** |
| Rôle de l'humain | Valideur de direction | **Détenteur de l'intention manquante** |

**Conséquence directe :** on ne peut pas forker BMAD en changeant le sens des flèches. Un générateur de documentation sans mécanisme de preuve produit de la fiction crédible — et une doc legacy fausse est **pire que pas de doc**, parce que la suivante équipe va la croire.

Tout le design de DMAD découle de là.

## 3. Les principes fondateurs

### P1 — Le code est la seule source de vérité *factuelle*
Ce que le système **fait** se lit dans le code, le schéma de données et le runtime. Rien d'autre ne fait foi. La doc existante, les tickets, les souvenirs des équipes sont des **sources d'intention** : précieuses, faillibles, à croiser — jamais des preuves.

### P2 — Aucune affirmation sans preuve
Toute phrase produite par DMAD porte une ou plusieurs `evidence` : `fichier:lignes`, commit, test, migration, trace runtime. Une affirmation sans preuve n'est pas publiée : elle devient une **question ouverte**.

### P3 — Le niveau de confiance est *dérivé*, pas deviné
Un LLM à qui l'on demande « tu es sûr à combien de % ? » invente un nombre. La confiance DMAD est **calculée mécaniquement à partir de la nature de la preuve** (voir §4). Elle n'est jamais une opinion du modèle.

### P4 — L'inconnu est un livrable de première classe
« Je ne sais pas pourquoi cette règle existe » est une **sortie légitime et attendue**. Le registre des questions ouvertes (`open-questions.md`) est un artefact aussi important que la doc elle-même : c'est l'ordre du jour des ateliers avec le métier.

### P5 — Le code dit *quoi*, jamais *pourquoi*
L'intention métier ne se déduit pas du code. Elle se reconstruit à partir de l'historique git, des messages de commit, des noms de tests, du vocabulaire des tables, des tickets — et se **valide auprès d'humains**. Toute affirmation d'intention est marquée comme hypothèse jusqu'à validation humaine.

### P6 — Trois lecteurs, trois documents, une cascade d'abstraction
Les trois documents du corpus — STD, SFD, SFG — ne sont pas trois rédactions parallèles, qui divergeraient. **Chacun est l'abstraction du précédent**, et n'a le droit de lire que lui : la SFD ne lit pas le code, la SFG ne lit ni le code ni la STD.

Deux lectures indépendantes du même matériau divergent ; une abstraction, non. Et une information absente d'un étage ne peut pas apparaître à l'étage supérieur : le trou se propage visiblement au lieu d'être comblé silencieusement là où il serait le plus difficile à détecter — chez le lecteur métier, qui n'a aucun moyen de vérifier.

Le *Knowledge Graph* reste le seul état partagé : une correction dans le graphe se propage à toute la cascade.

### P7 — Un diagramme répond à une question
Un diagramme qui ne répond à aucune question précise ne sort pas. Un diagramme de classes global d'un legacy est un plat de spaghetti illisible : ce n'est pas de la documentation, c'est du bruit avec des flèches.

### P8 — Le périmètre est déclaré et borné
DMAD ne « lit pas le projet ». Il analyse un périmètre explicite (tout le projet, ou une capacité). Ce qui est hors périmètre est dit hors périmètre, pas passé sous silence.

### P9 — La couverture est mesurée et affichée
DMAD publie quelle **fraction du code a réellement été atteinte** par l'analyse. Une doc qui couvre 30 % du code et le dit est honnête. Une doc qui couvre 30 % et se présente comme complète est un piège.

### P10 — La doc est rejouable et surveillée
Chaque affirmation pointe vers du code. Le code bouge. DMAD rejoue et **marque comme périmé** ce qui ne tient plus. Sans ça, DMAD produit de la dette documentaire à retardement.

## 4. L'échelle de confiance

> **Note d'arbitrage.** La demande initiale était un pourcentage par chapitre (80 %, 95 %, 100 %). L'intuition est juste — il *faut* afficher la fiabilité — mais un pourcentage sorti d'un LLM est une **fausse précision** : il n'est pas calibré, il ne veut rien dire, et il transforme une incertitude en chiffre rassurant. DMAD retient donc une échelle **discrète et dérivable mécaniquement**. Un rendu en pourcentage reste possible (§4.2) pour l'UX, mais il est calculé, jamais estimé.

### 4.1 Les quatre niveaux

| Niveau | Nom | Ce qui le justifie | Ce que ça veut dire pour le lecteur |
|---|---|---|---|
| **V** | Vérifié | Fait extrait mécaniquement (AST/LSP/DDL) **ou** prouvé par un test exécuté, **ou** observé en runtime | Tu peux t'appuyer dessus |
| **C** | Corroboré | ≥ 2 preuves indépendantes et convergentes (ex. code + test + nommage de table) | Très probablement vrai |
| **I** | Inféré | Lecture du code par le modèle, **une seule** source de preuve | Plausible — à relire avant de décider |
| **H** | Hypothèse | Intention métier reconstruite, non prouvable par le code | À faire valider par un humain |

**Règles de dérivation (non négociables) :**
- La confiance d'un chapitre est le **minimum de celle de ses énoncés de fait** (`statement`), jamais la moyenne. Une moyenne dilue le mensonge.
- **Les intentions sont exclues de ce calcul.** Elles sont toutes en `H` par construction (P5) : les inclure badgerait mécaniquement tout chapitre en `H` et rendrait l'échelle inutile. Chaque intention porte son propre marquage `H`, affiché à côté de la règle qu'elle explique.
- Une capability dégradée **plafonne** la confiance (ex. navigation par `grep` au lieu du LSP ⇒ plafond `I`). Voir `04-capabilities.md`.
- Toute affirmation d'intention métier (`P5`) démarre en `H` et ne peut monter qu'après validation humaine explicite, tracée.
- Le *Challenger* (§ agent adversarial) peut **dégrader** un niveau, jamais le monter.

### 4.2 Rendu

Chaque titre de chapitre porte un badge, et la source YAML porte le niveau brut :

```
## Règles de facturation  [C · corroboré · 12 affirmations · 2 questions ouvertes]
```

Le badge porte donc sur **ce que le système fait**. Le *pourquoi* est marqué séparément, au fil du texte :

> « Une facture à montant nul n'est pas transmise **[C]**.
> *Raisonnement supposé : éviter les rejets en masse du SI comptable.* **[H — à confirmer]** »

Un lecteur voit ainsi d'un coup d'œil qu'il peut s'appuyer sur le comportement, et qu'il ne doit pas s'appuyer sur son explication.

Si un pourcentage est souhaité en surface : `V=100 / C=85 / I=60 / H=30`, appliqué au **minimum** du chapitre. C'est une convention de lecture, pas une mesure. Elle doit être documentée comme telle en tête de chaque document.

## 5. Ce que DMAD n'est pas

- **Pas un résumeur de repo.** « Résume-moi ce projet » se fait en une commande, sans méthode, et produit une paraphrase invérifiable. DMAD n'a d'intérêt que par sa chaîne de preuve.
- **Pas un remplaçant du métier.** DMAD reconstruit des hypothèses d'intention et **prépare les bonnes questions**. Il ne décide pas ce que le métier voulait.
- **Pas un projet de refonte.** DMAD documente pour rendre l'évolution possible. Ce qu'on fait ensuite (strangler fig, refonte, gel) est une autre décision.
- **Pas un générateur de wiki.** L'objectif n'est pas 200 pages. C'est un graphe de connaissance exploitable dont la doc lisible est un rendu.

## 6. Filiation assumée

DMAD ne réinvente pas la rétro-ingénierie. Il **orchestre par des agents des pratiques déjà éprouvées** :

- **Michael Feathers**, *Working Effectively with Legacy Code* — les *seams* et les *characterization tests* : la seule façon de prouver qu'on a compris.
- **Adam Tornhill**, *behavioral code analysis* — les *hotspots* (churn × complexité) : on ne documente pas tout, on documente ce qui bouge et fait mal.
- **EventStorming « as-is »** — reconstruire le flux métier existant avant de le juger.
- **C4 · arc42 · ADR** — des formats de sortie normés plutôt qu'un gabarit maison.
- **BMAD** — le modèle d'orchestration : agents spécialisés, artefacts qui se contraignent, gates humains.

C'est cette filiation qui rend DMAD défendable. Une méthode ex nihilo ne le serait pas.
