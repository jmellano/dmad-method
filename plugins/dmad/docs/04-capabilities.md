# DMAD — Capabilities

## Le principe

Les agents **ne connaissent pas les outils**. Ils consomment des **capabilities** : des contrats stables, avec plusieurs implémentations interchangeables.

```
   agents  ──consomment──►  capabilities  ──implémentées par──►  outils
  (Carver,                (code-intelligence,                  (jcallgraph, git,
   Elucidator…)            repo-history…)                        grep…)
```

Sans ça, DMAD serait « la méthode qui marche avec tel outil sur tel langage ». Avec ça, DMAD est une méthode qui **se dégrade proprement** quand l'outillage manque — et qui dit où elle se dégrade.

## La règle qui fait tenir l'édifice

> **Une capability dégradée plafonne la confiance des affirmations qui en dépendent.**

C'est le pont entre l'architecture technique et le manifeste. Si la navigation de code se fait au `grep` faute de LSP, on ne peut pas prétendre connaître tous les appelants d'une fonction — donc toute affirmation d'exhaustivité qui en découle est plafonnée à `I`, mécaniquement, sans intervention humaine.

Chaque implémentation déclare donc son `confidence_ceiling`. Le runtime le propage aux claims.

---

## Les contrats

### `code-intelligence` — **prérequis dur**
Navigation sémantique du code.

```
list_symbols(path)                -> Symbol[]
find_definition(symbol)           -> Location
find_references(symbol)           -> Location[]
find_callers(symbol)              -> Symbol[]
find_callees(symbol)              -> Symbol[]
type_hierarchy(symbol)            -> { parents, children }
find_implementations(interface)   -> Symbol[]
```

**Implémentation de référence : `jcallgraph`** (voir la partie C). Analyseur tree-sitter, sans serveur à lancer ni indexeur à faire chauffer.

#### Le plafond se dérive de la question, pas de l'outil

C'est le changement de la v0.4, et il découle du principe P3 : *la confiance est dérivée de la nature de la preuve.* Un plafond unique par implémentation était lui-même une approximation — le même outil peut prouver exhaustivement une hiérarchie de types et ne proposer que des candidats sur un dispatch dynamique.

| Ce qu'on demande | Plafond | Pourquoi |
|---|---|---|
| structure d'un fichier, symboles déclarés | `V` | lecture syntaxique exhaustive |
| hiérarchie de types, implémentations d'une interface | `V` | déclaré dans les sources, entièrement résoluble |
| appel statique, appel sur type déclaré | `V` | la cible est écrite |
| appelants d'une méthode | `V` si le périmètre est entièrement indexé, `C` sinon | l'exhaustivité dépend de ce qui a été lu, pas de l'outil |
| appel virtuel ou d'interface | `C` — **liste de candidats, jamais un choix** | le type dynamique n'est pas connu statiquement |
| injection de dépendances, fabrique par chaîne | `C` avec `unresolved_dispatch` | le câblage est ailleurs, souvent hors du code |
| réflexion, chargement par nom | `I`, et une question ouverte | rien dans les sources ne le dit |
| comportement modifié par aspect ou proxy | **hors de portée** | à signaler, jamais à supposer |

**La règle qui tient l'édifice ne change pas** : une réponse dégradée plafonne les affirmations qui en dépendent. Ce qui change, c'est qu'elle s'applique **par arête du graphe** plutôt que globalement au run — donc plus finement, et sans pénaliser tout un run parce qu'un dispatch n'a pas pu être résolu.

#### Repli

| Repli | Plafond global | Note |
|---|---|---|
| recherche textuelle | `I` | dernier recours. **Aucune affirmation d'exhaustivité autorisée.** |

> **Arbitrage, révisé en v0.4 (D23).** Faire d'un serveur de langage un prérequis dur excluait d'emblée les legacy les plus concernés — COBOL, PL/SQL, VB6, 4GL propriétaires. Le compromis d'origine gardait le contrat obligatoire et l'implémentation libre. La v0.4 va plus loin : **elle abandonne le serveur de langage** au profit d'un analyseur tree-sitter, qui n'a ni classpath à résoudre, ni magasin de certificats, ni cache à empoisonner, ni processus orphelins — quatre modes de panne dont trois n'apparaissaient qu'après avoir résolu le précédent.

### `repo-history`
```
log(path?, grep?, since?)  -> Commit[]
blame(path, lines)         -> Attribution[]
churn(path?)               -> ChangeFrequency[]
hotspots()                 -> Hotspot[]        # churn × complexité
coupling()                 -> CoChangePair[]   # co-modification
```
Sert à la fois au `Carver` (le couplage temporel révèle des frontières que le code masque) et à l'`Archaeologist` (l'intention).

### `schema-intelligence`
```
tables() / columns(table) / foreign_keys()
migrations()               -> Migration[]      # historique = évolution du métier
orm_models()               -> Model[]
```
Dans un legacy mal nommé, **le schéma de données est souvent le document métier le plus fiable du projet**. Il est modélisé, versionné par les migrations, et il ment moins que le code.

### `runtime-evidence` *(optionnel, à privilégier quand disponible)*
```
coverage()      -> CoverageReport
traces(filter?) -> Trace[]
logs(filter?)   -> LogSample[]
```
**Seule capability qui prouve le comportement réel plutôt que le comportement possible.** Une trace de production tranche instantanément des débats que trois agents ne résoudraient pas. Quand elle est branchée, elle autorise le niveau `V` sur des chemins que le statique laisse en `I`.

### `doc-retrieval` — *optionnelle*
```
framework_docs(lib, version, query) -> Excerpt[]
```
Comprendre du Struts 1.2 ou du Spring 2.5 sans sa doc d'époque produit des contresens, et **la version compte autant que le nom**.

Implémentation : les outils de recherche de l'hôte, quand il en a. **Aucun serveur n'est requis** — et quand la capability est indisponible, ce n'est pas un run dégradé, c'est un risque nommé : toute affirmation qui repose sur le comportement d'un framework ancien, plutôt que sur le code lu, est plafonnée à `I` et porte sa question ouverte.

### `reasoning`
```
sequential_think(problem, budget) -> ReasoningTrace
```
**Servi par le modèle lui-même.** Réservé au découpage et à la réfutation ; ailleurs c'est un luxe qui brûle des tokens sans gain mesurable.

### `diagram-engine`
```
render(plan) -> (figure, metrics)      # tools/diagram-engine.py
```
Prend un **plan** — un sous-graphe, un type et une question — et rend la figure complète : la question, le badge de confiance, un **marqueur de rendu**, et le bloc Mermaid.

Les agents n'écrivent jamais de syntaxe de diagramme. Trois conséquences, et la troisième est celle qu'on oublie :

1. Un diagramme **ne peut pas contredire** le graphe : les deux sortent de la même source.
2. Le badge de confiance est **calculé** depuis le sous-graphe, pas recopié.
3. **Les nœuds sont comptés.** Sans rendu, D15 serait un seuil que rien ne mesure — personne ne compte les arêtes d'un diagramme écrit à la main, ni l'auteur ni le relecteur.

Le moteur **refuse** de rendre au-delà du seuil : la règle R2 est de découper, pas de simplifier. Et `check-corpus.py` re-rend chaque plan pour comparer : un diagramme retouché après coup est détecté.

### `evidence-store`
```
put_claim(claim) / get_claim(id) / link_evidence(claim, evidence)
verify_freshness()  -> StaleClaim[]
```
La colonne vertébrale. Persiste les claims, leurs preuves, leur niveau, leur historique d'arbitrage — et détecte le périmé (phase 7).

---

## Matrice agents × capabilities

| | code-intel | repo-history | schema | runtime | doc-retr | reasoning | diagram | evidence |
|---|---|---|---|---|---|---|---|---|
| Scoper | | ✓ | | | | | | |
| Surveyor | ✓ | ✓ | ✓ | ✓ | | | | ✓ |
| Cartographer | ✓ | | ✓ | ✓ | | | | ✓ |
| Carver | ✓ | ✓ | ✓ | | | ✓ | | ✓ |
| Elucidator | ✓ | | ✓ | ✓ | ✓ | | | ✓ |
| Archaeologist | | ✓ | ✓ | | | | | ✓ |
| Challenger | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | | ✓ |
| Test Forger | ✓ | | ✓ | ✓ | ✓ | | | ✓ |
| Diagram Planner | | | | | | | ✓ | ✓ |
| Contract Resolver | ✓ | | | | | | | ✓ |
| Writers (STD, SFD, SFG) | | | | | | | ✓ | ✓ |
| Curator | | | | | | | | ✓ |

Les cases vides sont des **interdictions**, pas des oublis : elles matérialisent le périmètre de lecture de chaque agent (cf. `03-agents.md`).
