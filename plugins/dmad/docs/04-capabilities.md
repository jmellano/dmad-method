# DMAD — Capabilities

## Le principe

Les agents **ne connaissent pas les outils**. Ils consomment des **capabilities** : des contrats stables, avec plusieurs implémentations interchangeables.

```
   agents  ──consomment──►  capabilities  ──implémentées par──►  outils
  (Carver,                (code-intelligence,                  (Serena, LSP,
   Elucidator…)            repo-history…)                       tree-sitter, git…)
```

Sans ça, DMAD serait « la méthode qui marche si tu as Serena installé sur un projet Java ». Avec ça, DMAD est une méthode qui **se dégrade proprement** quand l'outillage manque.

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

| Implémentation | Plafond | Note |
|---|---|---|
| **Serena / LSP natif** | `V` | Nominal. Exhaustivité et résolution des types garanties. |
| tree-sitter + ctags | `C` | Structure fiable, résolution dynamique perdue. |
| `grep` / ripgrep | `I` | Dernier recours. **Aucune affirmation d'exhaustivité autorisée.** |

> **Arbitrage.** L'intuition de faire du LSP un prérequis est bonne : sans lui, DMAD retombe au niveau d'un « lis mon repo » sophistiqué. Mais en faire une **dépendance dure** exclut d'emblée les legacy les plus concernés — COBOL, PL/SQL, VB6, PHP4, 4GL propriétaires — c'est-à-dire le cœur de cible. D'où ce compromis : **le contrat est obligatoire, l'implémentation est libre, et la dégradation est visible dans la doc produite**.

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

### `doc-retrieval`
```
framework_docs(lib, version, query) -> Excerpt[]
```
Implémentation : Context7 ou équivalent. Indispensable sur du legacy : comprendre le code d'un Struts 1.2 ou d'un Spring 2.5 sans sa doc d'époque produit des contresens. **La version compte autant que le nom.**

### `reasoning`
```
sequential_think(problem, budget) -> ReasoningTrace
```
Réservé aux phases 3 et 5 (découpage, réfutation). Ailleurs c'est un luxe qui brûle des tokens sans gain mesurable.

### `diagram-engine`
```
render(kind, subgraph, question) -> DiagramSource
```
Prend un **sous-graphe** et une **question**, rend du Mermaid (défaut) ou du PlantUML. Les agents n'écrivent jamais de syntaxe de diagramme à la main : ils décrivent une intention, le moteur rend. Un diagramme incohérent avec le graphe devient ainsi impossible par construction.

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
| Writers | | | | | | | ✓ | ✓ |
| Curator | | | | | | | | ✓ |

Les cases vides sont des **interdictions**, pas des oublis : elles matérialisent le périmètre de lecture de chaque agent (cf. `03-agents.md`).
