# DMAD — Mettre en œuvre

DMAD se distribue comme **plugin Claude Code**. Le corpus complet — méthode, tâches, schémas, templates, checklists, outils — voyage avec le plugin : il n'y a rien à copier dans le dépôt legacy analysé.

## Installation

### Classique

```
/plugin marketplace add jmellano/dmad-method
/plugin install dmad@dmad-method
```

`/plugin list` doit afficher `dmad@dmad-method` en **enabled**. Puis, dans le dépôt legacy : `/dmad-run`.

Le marketplace sert la **branche par défaut** du dépôt : une version en cours de développement sur une autre branche ne s'installe pas ainsi.

### En développement — itérer

```bash
claude --plugin-dir /chemin/vers/dmad-method/plugins/dmad
```

Puis `/reload-plugins` après chaque modification. C'est le seul mode qui évite de réinstaller à chaque changement, et donc le seul praticable quand on travaille *sur* la méthode plutôt qu'*avec* elle.

### En développement — comme en vrai

Pour vérifier que l'installation elle-même fonctionne, avant publication :

```
/plugin marketplace add /chemin/vers/dmad-method     # le DÉPÔT, pas le plugin
/plugin install dmad@dmad-method
```

Le chemin est celui du dépôt parce que le marketplace est déclaré dans son `.claude-plugin/marketplace.json`, qui pointe ensuite vers `./plugins/dmad`. C'est l'erreur la plus fréquente.

### Vérifier le packaging
```bash
claude plugin validate /chemin/vers/dmad-method/plugins/dmad   # le plugin
claude plugin validate /chemin/vers/dmad-method                # le marketplace
```

Les deux doivent afficher `Validation passed`. Un manifeste invalide s'installe silencieusement de travers : mieux vaut le découvrir soi-même.

### Savoir ce qu'on charge

```bash
claude plugin details dmad
```

Inventaire des composants et **coût en tokens projeté**. DMAD est un gros plugin, et une bonne partie de son corpus n'est lue qu'à la demande via `${CLAUDE_PLUGIN_ROOT}` — les procédures détaillées ne sont pas dupliquées dans les prompts. Cette commande dit ce qui pèse réellement au chargement, par opposition à ce que pèse le dépôt.

### Ce qu'il n'y a pas à installer

**Aucun serveur MCP** (D24) : rien à lancer, rien à diagnostiquer quand ça ne répond pas. Les outils du plugin sont en Python 3 et demandent `pyyaml` et `jsonschema`.

## Ce que le plugin apporte

| | |
|---|---|
| 15 agents | `dmad-scoper`, `dmad-surveyor`, … chacun avec son périmètre de lecture et son modèle |
| 3 skills | `/dmad-run` orchestre ; `code-intelligence-java` et `patterns-gof-cqrs` sont des prérequis lus à la demande |
| Serveurs MCP | **aucun** — le plugin n'a aucune dépendance à installer |
| Le corpus | `docs/`, `tasks/`, `templates/`, `checklists/`, `schemas/`, `workflows/`, `examples/` |
| Les outils | `tools/validate.py`, `tools/selftest.sh` |

Les agents référencent le corpus via `${CLAUDE_PLUGIN_ROOT}` : les procédures détaillées ne sont pas dupliquées dans les prompts, elles sont **lues à la demande**. Un agent charge la tâche dont il a besoin, pas les seize.

## Correspondance DMAD ↔ Claude Code

| Concept DMAD | Mécanisme |
|---|---|
| `dmad.reads` | `tools:` / `disallowedTools:` dans le frontmatter |
| `agent.model` | `model: haiku \| sonnet \| opus` |
| Contexte séparé du Challenger | un subagent = un contexte isolé, par construction |
| Gate humain | la skill présente la décision et s'arrête |
| Capabilities | outils de l'hôte, exécutables locaux, ou le modèle |
| Corpus de la méthode | `${CLAUDE_PLUGIN_ROOT}/…` |

**Le point important :** l'isolation de contexte des subagents est ce qui rend le Challenger réellement adversarial. Il ne voit pas le raisonnement de l'Elucidator — non par consigne, mais parce que le mécanisme ne le lui transmet pas. C'est une garantie structurelle, pas une promesse de prompt.

## Le cas des rédacteurs

DMAD exige que les trois rédacteurs **n'aient pas accès au code**, et que chacun soit en outre aveugle à l'étage n−2 de la cascade : `dmad-writer-sfd` ne lit que la STD figée et les claims, `dmad-writer-sfg` ne lit que la SFD figée.

Trois niveaux d'application, du plus fort au plus faible :

1. **Retrait des outils d'exploration** — `disallowedTools: Grep, Glob, Bash` dans le frontmatter. Livré tel quel par le plugin.
2. **Règles de permission `deny`** sur les chemins sources, dans le `.claude/settings.json` du projet analysé. **À adapter au projet** : voir `settings.example.json`, dont les chemins sont des exemples.
3. **Consigne dans le system prompt** — nécessaire mais insuffisante seule.

Les deux premiers niveaux sont des contraintes réelles. Ne compter que sur le troisième revient à espérer que le modèle se retienne.

## Capabilities et implémentations

| Capability | Implémentation |
|---|---|
| `code-intelligence` | `jcallgraph` — analyseur tree-sitter, plafond dérivé de la question (D23) |
| `doc-retrieval` | les outils de recherche de l'hôte, quand il en a — **optionnelle** |
| `reasoning` | le modèle lui-même |
| `repo-history` | `git` via Bash |
| `schema-intelligence` | migrations + client SQL via Bash |
| `runtime-evidence` | rapports de couverture, logs — lecture de fichiers |
| `diagram-engine` | `tools/diagram-engine.py` — Mermaid, aucune dépendance |
| `evidence-store` | fichiers YAML versionnés |

**Aucun serveur MCP**, et c'est délibéré (D24). Les huit capabilities se satisfont d'outils déjà présents, d'un exécutable local ou du modèle lui-même.

Ce que ça change en pratique : rien à installer, rien à lancer, rien à diagnostiquer quand ça ne répond pas — et aucun serveur qui consomme du contexte à chaque appel. Le prix est que `doc-retrieval` devient optionnelle : sur un framework ancien, ce qu'on ne peut pas vérifier se dit plutôt que de se deviner.

## Coût et routage

Le modèle fort est payé **là où l'erreur coûte le plus**, pas là où le volume est le plus gros.

| Cycle | Étape | Modèle | Part attendue du coût |
|---|---|---|---|
| 1 | Reconnaissance | haiku | faible |
| 1 | Cartographie | haiku | moyenne — beaucoup d'appels LSP |
| 1 | Contrats sortants | haiku | faible — lecture d'archive |
| 1 | Challenge + rédaction STD | opus, sonnet | moyen |
| 2 | Découpage | **opus** | faible en volume, fort en valeur |
| 2 | Élucidation | sonnet | **le plus gros poste** |
| 2 | Challenge | **opus** | moyen — le maillon qui protège tout |
| 2 | Rédaction SFD | sonnet | moyen |
| 3 | Intention + rédaction SFG | sonnet | faible |

**Un run `corpus: [std]` ne paie que les quatre premières lignes** — c'est le moyen le moins cher de mesurer les proportions réelles avant de s'engager sur le corpus complet.

**Ces proportions n'ont pas été mesurées sur un run réel** — c'est le premier chiffre à établir (cf. [roadmap](12-roadmap.md)).

## Parallélisation

Deux endroits, et deux seulement :
- **Cycle 1** — plusieurs points d'entrée en parallèle : chaque STD est un document indépendant.
- **Cycle 2** — plusieurs capacités en parallèle, une fois le gate 3 passé.

**Le reste est séquentiel par nécessité**, et la v0.4 le rend plus strict encore : les trois rédacteurs ne peuvent pas travailler en parallèle, puisque chacun lit le document figé du cycle précédent. Paralléliser le Challenger avec l'Elucidator reviendrait à réfuter des claims encore en cours d'écriture.

## Confidentialité

Sur du code client, `scope.confidentiality` doit être **appliqué**, pas seulement déclaré :
- `local_only: true` ⇒ aucun appel réseau. Depuis la v0.4, **le plugin n'embarque aucun serveur MCP** : la surface est réduite aux outils de l'hôte, qu'il faut couper par règles `deny`
- règles `deny` sur les outils réseau
- `redaction_rules` appliquées **avant écriture**, jamais après : une donnée caviardée après coup reste dans l'historique git — que DMAD versionne et conserve

> **La surface de risque a diminué en v0.4.** Les extraits de code étaient le principal vecteur de fuite ; D16 les a supprimés des documents, et `evidence.excerpt` a disparu du schéma des claims — c'était le dernier canal par lequel du code atteignait un rédacteur censé en être coupé. Restent les références précises, qui sont le cœur de la méthode et ne peuvent pas disparaître.

**Le mécanisme d'application n'est pas encore spécifié** — limite connue, bloquante pour un usage en prestation. Voir [roadmap](12-roadmap.md).

## Vérifier avant de livrer

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/tools/validate.py     dmad-output/   # artefacts contre schémas
python3 ${CLAUDE_PLUGIN_ROOT}/tools/check-corpus.py dmad-output/   # documents contre invariants
```

Deux outils parce que deux natures de vérification. `validate.py` route un artefact YAML vers son schéma et applique les règles croisées ; `check-corpus.py` lit les documents Markdown et vérifie D16, D17, D20, R1 et les sept blocs. Mélanger les deux produirait des messages d'erreur que personne ne sait interpréter.

Puis le contrôle qui compte réellement : **tirer 5 claims au hasard, ouvrir le code aux lignes citées, vérifier que la phrase correspond.** Dix minutes. Un taux d'erreur supérieur à 1 sur 5 condamne le run.

C'est le seul contrôle qui détecte l'anti-pattern A2 (la preuve trahie), parce qu'une relecture intégrale d'un texte crédible et bien sourcé ne détecte rien.
