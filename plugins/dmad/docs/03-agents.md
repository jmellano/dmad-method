# DMAD — Le casting d'agents

## Principe de conception

Chaque agent DMAD est défini par **quatre contraintes**, dans cet ordre d'importance :

1. **Ce qu'il a le droit de lire** (le code ? seulement le graphe ? seulement les claims ?)
2. **Ce qu'il a le droit de produire** (des faits ? des hypothèses ? des réfutations ?)
3. **Le plafond de confiance** de ce qu'il produit
4. Sa persona / son style

L'ordre n'est pas anodin. Dans BMAD, la persona porte l'essentiel. Dans DMAD, **c'est le périmètre de lecture qui garantit la fiabilité** : un agent qui n'a pas accès au code ne peut pas inventer de fait sur le code.

---

## Les agents

### `Scoper` — le facilitateur
- **Lit :** rien du code. Dialogue avec l'humain.
- **Produit :** `run.yaml`, glossaire d'amorce, budget.
- **Plafond :** n/a
- **Rôle :** poser les questions de cadrage, refuser de lancer un run mal borné. Seul agent réellement conversationnel.

### `Surveyor` — le recenseur
- **Lit :** l'arborescence, les fichiers de build, les configs, le DDL, le git log.
- **Produit :** des **faits** uniquement (`facts/*.json`). Interdiction de produire de la prose.
- **Plafond :** `V` (tout ce qu'il produit est mécanique).
- **Garde-fou :** si un outil échoue, il **déclare l'échec** — il ne comble pas par déduction.

### `Cartographer` — le cartographe
- **Lit :** le code via `code-intelligence` (`jcallgraph`), les faits du cycle 1.
- **Produit :** nœuds et arêtes du Knowledge Graph.
- **Plafond :** `V` pour les arêtes issues d'outils, `I` pour les regroupements qu'il propose.
- **Garde-fou :** **aucune arête sans outil**. Une relation « devinée » à la lecture est une claim, pas une arête.

### `Contract Resolver` — le greffier des contrats *(v0.4)*
- **Lit :** les feuilles « contrat sortant » du graphe, et les **artefacts des dépendances** — hors du projet indexé, donc hors de portée de tout outil de navigation sémantique.
- **Produit :** des nœuds `ExternalContract` — code, verbe, route, opération, artefact **et sa version**.
- **Plafond :** dérivé du **barreau de résolution** atteint : `V` pour l'annotation de contrat, `C` pour la Javadoc générée, `I` pour le commentaire manuscrit, rien pour le placeholder.
- **Garde-fou :** un contrat sans `artifact_version` est refusé à l'écriture. L'artefact lu est figé à la version que le module consomme ; sans le champ, la preuve devient fausse au prochain bump **sans que rien ne le signale**.

### `Carver` — le découpeur
- **Lit :** le graphe, les métriques de co-modification git, le vocabulaire.
- **Produit :** capacités candidates, **business objects** avec leurs deux étiquettes de niveau, patrons de conception reconnus, *seams*, zones de recouvrement.
- **Plafond :** `I` (montée à `C` après validation humaine du gate).
- **Modèle :** fort. C'est le jugement le plus structurant de la méthode.

### `Elucidator` — l'analyste métier
- **Lit :** le graphe + le code d'une capacité donnée (périmètre borné).
- **Produit :** cas d'usage, règles de gestion, invariants, machines à états.
- **Plafond :** `I`.
- **Garde-fou :** chaque règle citée avec ses lignes exactes. Une règle sans localisation précise est refusée.

### `Archaeologist` — l'historien
- **Lit :** git log/blame, messages de commit, tickets, ADR, wiki, noms de tests, anciens fichiers supprimés.
- **Produit :** des **hypothèses d'intention** (« cette règle date de X, introduite avec le ticket Y qui mentionne une contrainte réglementaire »).
- **Plafond :** `H`, sans exception. Seule une validation humaine tracée peut la faire monter.
- **Pourquoi il est indispensable :** c'est le seul agent qui peut approcher le *pourquoi* (principe P5).

### `Challenger` — l'avocat du diable
- **Lit :** les claims **et** le code, pour les confronter.
- **Produit :** des **réfutations, des dégradations, des questions ouvertes**. Il lui est **interdit de produire de la documentation**.
- **Pouvoir :** peut dégrader un niveau de confiance ou invalider une claim. **Ne peut jamais faire monter un niveau.**
- **Modèle :** fort. C'est le garde-fou principal contre la doc plausible et fausse.
- **Angles d'attaque imposés :** garde/court-circuit oublié, feature flag, surcharge/polymorphisme, chemin d'erreur, configuration environnementale, transaction/rollback, cas limite sur données nulles.

### `Test Forger` — le prouveur
- **Lit :** les règles de gestion critiques + le code d'accès.
- **Produit :** des *characterization tests* qui capturent le comportement actuel.
- **Pouvoir :** **le seul agent qui peut faire monter une claim en `V`** — et uniquement si le test passe réellement.
- **Garde-fou :** un test qui échoue ne dégrade pas la claim automatiquement : il ouvre une question (le test peut être faux).

### `Diagram Planner` — le scénographe
- **Lit :** le graphe uniquement.
- **Produit :** un **plan de diagrammes** : pour chaque diagramme, la question à laquelle il répond, son type, son périmètre, ses nœuds.
- **Garde-fou :** refuse tout diagramme sans question associée ou dépassant le seuil de lisibilité (cf. `06-diagrammes.md`).

### Les trois rédacteurs — une échelle de lecture

C'est la contrainte la plus contre-intuitive de DMAD, et la v0.4 la resserre : elle ne porte plus sur deux rédacteurs coupés du code, mais sur **trois rédacteurs en cascade, chacun aveugle à l'étage n−2**.

| Rédacteur | Lit | Produit | Unité |
|---|---|---|---|
| `Writer:STD` | le graphe et les claims validées | la spécification technique détaillée | le point d'entrée |
| `Writer:SFD` | **la STD figée** et les claims validées | la spécification fonctionnelle détaillée, en vue récursive par business object | l'arbre de business objects |
| `Writer:SFG` | **la SFD figée** | la spécification fonctionnelle générale, par cas d'usage | le cas d'usage |

**Aucun des trois n'écrit de bloc de code, de requête ou de configuration** (D16). La STD porte des références — `fichier:lignes`, signatures, noms de tables. La SFD et la SFG ignorent jusqu'à l'existence du code.

Ce second interdit n'est pas qu'une affaire de conformité : c'est lui qui rend le premier tenable. Tant qu'un extrait est permis, aller lire le code a un motif légitime, et la coupure devient poreuse.

**Ce que l'échelle garantit en plus de la coupure.** Que chaque niveau est réellement une *abstraction* du précédent, et non une seconde lecture indépendante du même matériau. Deux lectures indépendantes divergent ; une abstraction, non. Et une information absente de la STD ne peut pas apparaître dans la SFD : le trou se propage visiblement au lieu d'être comblé silencieusement à l'étage supérieur — où il serait le plus difficile à détecter, puisque le lecteur métier n'a aucun moyen de vérifier.

**Gradation de la langue selon la confiance**, imposée aux trois :

| Niveau | Formulation |
|---|---|
| `V` · `C` | « Le système transmet… » + badge |
| `I` | « **D'après l'analyse**, le système transmettrait… » |
| `H` | « **Hypothèse à confirmer :** … » |

Un badge seul est invisible en lecture rapide ; un conditionnel ne l'est pas.

### La boucle de retour

La contrainte « les rédacteurs ne lisent pas le code » ne tient que si un rédacteur bloqué a une issue. Sans elle, il finit par contourner : il devine, ou il produit un document criblé de trous inutilisable.

Quand un rédacteur rencontre un manque, il émet une **demande ciblée** — il ne comble pas, il ne devine pas, il demande :

```yaml
gap_request:
  from: writer-functional
  capability: facturation
  need: >
    Le cas d'usage UC-FACT-003 ne dit pas ce qu'il advient de la commande
    d'origine après émission de la facture. Impossible d'écrire la
    postcondition sans inventer.
  blocks: "fonctionnel/30-capacites/facturation/10-cas-usage/UC-FACT-003.md"
  severity: blocking        # blocking | degrades | cosmetic
```

Une demande `blocking` relance l'agent compétent **sur ce point précis**, puis le Challenger sur la claim produite. C'est un aller-retour ciblé, pas une reprise de cycle.

**La demande remonte d'un cycle, jamais jusqu'au code.** Un `Writer:SFD` bloqué relance la cartographie ou l'élucidation du cycle 1 ; il ne va pas lire les sources. Un `Writer:SFG` bloqué relance le cycle 2. C'est ce qui rend l'échelle de lecture tenable sans la percer.

Une demande `degrades` ne relance rien : elle devient une question ouverte et une mention dans « ce qui n'a pas été analysé ». **Le document sort avec son trou visible**, ce qui est l'issue voulue.

> Sans cette boucle, la contrainte de lecture se retourne contre la méthode : un rédacteur privé de code et privé de recours produit soit de l'invention, soit de l'illisible.

> **Pourquoi les rédacteurs ne lisent pas le code.** C'est la contrainte la plus contre-intuitive et la plus importante de DMAD. Un rédacteur qui a le code sous les yeux comblera les trous du graphe par sa propre lecture — et cette lecture n'aura traversé ni le `Challenger` ni le `Test Forger`. En le coupant du code, **toute affirmation publiée a nécessairement franchi la chaîne de preuve.** Les trous restent visibles au lieu d'être bouchés silencieusement.

### `Curator` — le gardien de la cohérence
- **Lit :** l'ensemble des sorties.
- **Produit :** glossaire unifié, index, détection de contradictions inter-capacités, **rapport de couverture**, liste consolidée des questions ouvertes.

---

## Ce que devient le pipeline

```
Cycle 0   Scoper ─⛔─►
Cycle 1   Surveyor ─► Cartographer ─► Contract Resolver ─► Challenger ─► Writer:STD ─⛔─►
Cycle 2   Carver ─⛔─► Elucidator ─► Challenger ─► Test Forger ─► Writer:SFD ─⛔─►
Cycle 3   Archaeologist ─► Curator ─► Challenger ─► Writer:SFG ─⛔
```

⛔ = gate ou revue humaine. Le `Diagram Planner` intervient avant chaque rédaction ; le `Curator` clôt l'ensemble.

Chaque revue de fin de cycle peut demander **corrections et compléments** : elle ne se réduit pas à un feu vert. Le cycle suivant ne démarre pas sur un document non figé.

## Compatibilité BMAD

Les agents sont décrits au format BMAD (fichier Markdown avec en-tête YAML : persona, commands, dependencies) et l'arborescence reprend ses conventions (`agents/`, `tasks/`, `templates/`, `checklists/`, `workflows/`). Objectif : quiconque connaît BMAD est opérationnel immédiatement, et DMAD peut être distribué comme *expansion pack* aussi bien qu'exécuté en autonome.

**Les deux ajouts au format BMAD**, sans lesquels la méthode ne tient pas :
- `reads:` — le périmètre de lecture autorisé de l'agent
- `confidence_ceiling:` — le plafond de confiance de ses productions
