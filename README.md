# DMAD

**Documentation Method for Agentic Discovery** — une méthode agentique pour reconstruire, depuis un code legacy, un **corpus de trois documents en cascade d'abstraction** dont chaque affirmation est prouvée, datée et vérifiable.

> Le pendant inverse de [BMAD](https://github.com/bmad-code-org/BMAD-METHOD).
> BMAD descend d'une intention vers du code. DMAD remonte d'un code vers une intention.
> Ce n'est pas la même méthode dans l'autre sens : **BMAD génère, DMAD enquête.**

## Installation

### Depuis le marketplace

```
/plugin marketplace add jmellano/dmad-method
/plugin install dmad@dmad-method
```

Vérifier : `/plugin list` doit afficher `dmad@dmad-method` en **enabled**.

Puis, dans le dépôt legacy à documenter :

```
/dmad-run
```

> Le marketplace sert la **branche par défaut** du dépôt. Une version en cours de développement sur une autre branche ne s'installe pas par ce chemin — utiliser le mode développement ci-dessous.

### En mode développement

Deux façons, selon qu'on veut itérer sur le plugin ou seulement l'essayer avant publication.

**Charger le plugin directement** — la plus courte, et celle qui permet de recharger sans réinstaller :

```bash
claude --plugin-dir /chemin/vers/dmad-method/plugins/dmad
```

Puis, après chaque modification du plugin :

```
/reload-plugins
```

**Passer par un marketplace local** — plus proche de l'installation réelle, donc ce qu'il faut employer pour valider le packaging avant publication :

```
/plugin marketplace add /chemin/vers/dmad-method
/plugin install dmad@dmad-method
```

C'est le chemin du **dépôt**, pas celui du plugin : le marketplace est déclaré dans `.claude-plugin/marketplace.json` à la racine, et il pointe vers `./plugins/dmad`.

### Vérifier le packaging avant de publier

```bash
claude plugin validate /chemin/vers/dmad-method/plugins/dmad   # le plugin
claude plugin validate /chemin/vers/dmad-method                # le marketplace
```

Les deux doivent afficher `Validation passed`. Un manifeste invalide s'installe silencieusement de travers : la commande ne coûte rien, et elle évite de découvrir le problème chez quelqu'un d'autre.

### Savoir ce qu'on charge

```bash
claude plugin details dmad
```

Inventaire des composants et **coût en tokens projeté**. DMAD est un gros plugin — quinze agents, vingt tâches, six outils — et une bonne partie n'est lue qu'à la demande via `${CLAUDE_PLUGIN_ROOT}`. Cette commande dit ce qui pèse réellement au chargement.

### Aucune dépendance à installer

Le plugin n'embarque **aucun serveur MCP** (D24) : rien à lancer, rien à diagnostiquer quand ça ne répond pas. Tout le corpus — méthode, tâches, schémas, gabarits, checklists, outils — voyage avec lui, et rien n'est à copier dans le projet analysé.

Les outils sont en Python 3 et demandent `pyyaml` et `jsonschema`.

## Le problème

Un legacy est un système dont le comportement est connu de la machine et inconnu des humains. Les auteurs sont partis, la doc ment, plus personne n'ose toucher. Chaque évolution coûte trois fois son prix parce qu'on paie d'abord la ré-investigation.

## Le piège que DMAD existe pour éviter

Demander à un LLM de documenter un legacy produit en quelques minutes une documentation fluide, structurée, crédible — et fausse par endroits, **sans qu'on sache lesquels**.

Sur du legacy, une documentation fausse est **pire que pas de documentation** : l'équipe suivante la croit, décide sur cette base, et découvre l'erreur en production.

Toute la méthode est construite autour de ce risque unique. Les [13 façons dont il se manifeste](plugins/dmad/docs/10-antipatterns.md) sont cataloguées, et chaque contrainte de DMAD répond à l'une d'elles.

## Le corpus

```
code ──────► STD ──────► SFD ──────► SFG
             technique    fonctionnel   métier
             détaillée    détaillée     générale

             un point     un arbre de   un cas
             d'entrée     business obj. d'usage
```

Chaque document est **l'abstraction du précédent**, et **aveugle à l'étage n−2** : la SFD ne lit pas le code, la SFG ne lit ni le code ni la STD. Ce n'est pas trois rendus du même graphe — c'est une suite, et c'est ce qui garantit qu'un niveau abstrait ne soit pas une seconde lecture indépendante qui divergera.

**Aucun des trois ne contient de bloc de code.** La STD porte des références — `fichier:lignes`, signatures, noms de tables ; les deux autres ignorent jusqu'à l'existence du code.

## Les quatre idées

1. **Aucune affirmation sans preuve.** Chaque phrase porte ses `evidence` : `fichier:lignes`, commit, test, migration. Contraint par schéma — une claim sans preuve est refusée à l'écriture, pas signalée en relecture.
2. **La confiance est dérivée, pas devinée.** Échelle `V` vérifié / `C` corroboré / `I` inféré / `H` hypothèse, calculée depuis la **nature de la preuve** — jamais un pourcentage sorti du modèle.
3. **L'inconnu est un livrable.** Le registre des questions ouvertes est l'ordre du jour de l'atelier métier, et souvent le livrable le plus rentable du run.
4. **Un agent adversarial garde la porte.** Le Challenger ne rédige rien : son seul métier est de faire tomber les affirmations des autres. Seul un test de caractérisation qui passe fait monter une claim au niveau maximal.

## Le pipeline — trois cycles

```
Cycle 0   Scoper ─⛔─►
Cycle 1   Surveyor ─► Cartographer ─► Contract Resolver ─► Challenger ─► Writer:STD ─⛔─►
Cycle 2   Carver ─⛔─► Elucidator ─► Challenger ─► Test Forger ─► Writer:SFD ─⛔─►
Cycle 3   Archaeologist ─► Curator ─► Challenger ─► Writer:SFG ─⛔
```

⛔ = gate ou revue humaine. Chaque cycle est scellé par une revue qui peut demander **corrections et compléments** ; le cycle suivant ne démarre pas sur un document non figé.

**Le budget épuisé s'arrête sur un document terminé**, jamais au milieu d'un cycle : une STD seule est un livrable qui se défend, une SFD bâtie sur une STD non revue ne l'est pas.

## Voir la méthode en action

**→ [Run de référence : Atlas ERP, capacité Facturation](plugins/dmad/examples/atlas-billing/)**

Un run complet déroulé de bout en bout, où le Challenger trouve deux défauts qu'aucune relecture n'aurait vus : un feature flag actif en production mais inactif par défaut dans le dépôt (documentation vraie en recette, fausse ailleurs), et un « n'est jamais transmise » faux sur le troisième appelant.

## Documentation

Tout est dans [`plugins/dmad/docs/`](plugins/dmad/docs/) — commencer par le [manifeste](plugins/dmad/docs/01-manifeste.md), ou par les [anti-patterns](plugins/dmad/docs/10-antipatterns.md) pour juger si la méthode tient.

Projet Java ? → [profil Java](plugins/dmad/docs/13-profil-java.md).

## Prérequis

- **`jcallgraph`** pour la navigation sémantique — un analyseur tree-sitter, sans serveur à lancer ni projet à faire compiler. **Le plafond de confiance se dérive de la question posée, pas de l'outil** : une hiérarchie de types est `V`, un appel virtuel rend des candidats en `C`, une réflexion ouvre une question. Ce qui n'est pas prouvé est dit tel quel dans la documentation produite.
- Accès à l'**historique git complet** : l'intention se reconstruit largement là.
- Optionnel mais décisif : **couverture, traces ou logs de production** — la seule preuve du comportement *réel* plutôt que *possible*.

## État

**v0.4 — corpus à trois documents spécifié.** Ce qui manque est le seul jalon qui compte : **un run sur un vrai legacy**. Tant qu'il n'a pas eu lieu, DMAD est une spécification cohérente — ce qui ne prouve rien. Voir [l'état et la suite](plugins/dmad/docs/12-roadmap.md).

## Filiation

[BMAD](https://github.com/bmad-code-org/BMAD-METHOD) (orchestration) · Michael Feathers, *Working Effectively with Legacy Code* (seams, characterization tests) · Adam Tornhill (hotspots, behavioral code analysis) · EventStorming « as-is » · C4 / arc42 / ADR.

## Licence

MIT
