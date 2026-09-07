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
- **Produit :** `scope.yaml`, glossaire d'amorce, budget.
- **Plafond :** n/a
- **Rôle :** poser les questions de cadrage, refuser de lancer un run mal borné. Seul agent réellement conversationnel.

### `Surveyor` — le recenseur
- **Lit :** l'arborescence, les fichiers de build, les configs, le DDL, le git log.
- **Produit :** des **faits** uniquement (`facts/*.json`). Interdiction de produire de la prose.
- **Plafond :** `V` (tout ce qu'il produit est mécanique).
- **Garde-fou :** si un outil échoue, il **déclare l'échec** — il ne comble pas par déduction.

### `Cartographer` — le cartographe
- **Lit :** le code via `code-intelligence` (LSP), les faits de la phase 1.
- **Produit :** nœuds et arêtes du Knowledge Graph.
- **Plafond :** `V` pour les arêtes issues d'outils, `I` pour les regroupements qu'il propose.
- **Garde-fou :** **aucune arête sans outil**. Une relation « devinée » à la lecture est une claim, pas une arête.

### `Carver` — le découpeur
- **Lit :** le graphe, les métriques de co-modification git, le vocabulaire.
- **Produit :** capacités candidates, *seams*, zones de recouvrement.
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

### `Writer:Functional` — le rédacteur métier
- **Lit :** **uniquement les claims validées et le glossaire. Pas le code.**
- **Produit :** la documentation fonctionnelle, badges de confiance inclus, section « à confirmer par le métier » par chapitre.
- **Ton :** vocabulaire métier, zéro nom de classe, zéro jargon technique.

### `Writer:Technical` — le rédacteur technique
- **Lit :** **uniquement les claims validées et le graphe. Pas le code.**
- **Produit :** la documentation technique, arc42/C4, renvois `fichier:lignes`.
- **Ton :** dev qui arrive sur le projet lundi matin.

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

Une demande `blocking` relance l'Elucidator **sur ce point précis**, puis le Challenger sur la claim produite. C'est un aller-retour ciblé, pas une reprise de phase.

Une demande `degrades` ne relance rien : elle devient une question ouverte et une mention dans « ce qui n'a pas été analysé ». **Le document sort avec son trou visible**, ce qui est l'issue voulue.

> Sans cette boucle, la contrainte de lecture se retourne contre la méthode : un rédacteur privé de code et privé de recours produit soit de l'invention, soit de l'illisible.

> **Pourquoi les rédacteurs ne lisent pas le code.** C'est la contrainte la plus contre-intuitive et la plus importante de DMAD. Un rédacteur qui a le code sous les yeux comblera les trous du graphe par sa propre lecture — et cette lecture n'aura traversé ni le `Challenger` ni le `Test Forger`. En le coupant du code, **toute affirmation publiée a nécessairement franchi la chaîne de preuve.** Les trous restent visibles au lieu d'être bouchés silencieusement.

### `Curator` — le gardien de la cohérence
- **Lit :** l'ensemble des sorties.
- **Produit :** glossaire unifié, index, détection de contradictions inter-capacités, **rapport de couverture**, liste consolidée des questions ouvertes.

---

## Ce que devient le pipeline

```
Scoper ─⛔─► Surveyor ─► Cartographer ─► Carver ─⛔─► Elucidator ─┐
                                                   Archaeologist ─┤
                                                                  ▼
                                                             Challenger
                                                             Test Forger
                                                                  │
                                                                 ⛔
                                                                  ▼
                                    Diagram Planner ─► Writers ─► Curator
```

⛔ = gate humain obligatoire.

## Compatibilité BMAD

Les agents sont décrits au format BMAD (fichier Markdown avec en-tête YAML : persona, commands, dependencies) et l'arborescence reprend ses conventions (`agents/`, `tasks/`, `templates/`, `checklists/`, `workflows/`). Objectif : quiconque connaît BMAD est opérationnel immédiatement, et DMAD peut être distribué comme *expansion pack* aussi bien qu'exécuté en autonome.

**Les deux ajouts au format BMAD**, sans lesquels la méthode ne tient pas :
- `reads:` — le périmètre de lecture autorisé de l'agent
- `confidence_ceiling:` — le plafond de confiance de ses productions
