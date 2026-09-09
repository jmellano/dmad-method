# Partie C — L'outil `jcallgraph`

> Spec détaillée. Vue d'ensemble : [reste à faire](2026-09-09-dmad-reste-a-faire.md)
> **Dépend de** : rien. **Bloque** : rien — le cycle 1 doit fonctionner sans lui.

## L'objet

Une CLI Python adossée à `javap`. **Aucun build, aucune dépendance à installer** : le JDK est déjà présent, puisque le projet compile.

Elle fait deux choses qu'aucun outil du dispositif actuel ne fait :

**La traversée transitive.** Les outils de navigation sémantique rendent *un* niveau — les appelants directs, les appelés directs. Une liste d'appelants directs n'est pas une carte, et l'itération à la main coûte un appel LSP par nœud.

**Le franchissement vers l'intérieur des dépendances.** Le LSP n'indexe pas `~/.m2`. Aujourd'hui, la traversée s'arrête à la frontière du projet, et tout ce qui se passe derrière est une frontière journalisée. Or une partie du comportement documenté vit dans ces artefacts — à commencer par les contrats sortants.

## Pourquoi le bytecode plutôt que le texte

**Un site d'appel bytecode porte son descripteur complet.** Vérifié :

```
22: invokevirtual #29   // Method java/lang/StringBuilder.toString:()Ljava/lang/String;
16: invokeinterface #23 // InterfaceMethod java/util/List.forEach:(Ljava/util/function/Consumer;)V
```

Propriétaire, nom, signature exacte. **Les surcharges sont donc résolues**, ce qu'aucun grep ne fait et ce qu'un LSP ne garantit que si le projet compile. Zéro faux positif, et une arête qui porte réellement l'information dont le graphe a besoin.

Le prix à payer est la liste des angles morts, en fin de spec. Ils sont connus, bornés, et deux d'entre eux sont exactement ceux que DMAD traite déjà en `unresolved_dispatch`.

---

## C1 — L'index bytecode

### Sources de classes

| Source | Comment | Quand |
|---|---|---|
| `target/classes` du module étudié | lecture directe | toujours |
| jars du classpath | `mvn dependency:build-classpath` puis lecture des entrées | à la demande |
| `-sources.jar` | archive séparée, voir C5 | pour les annotations et la Javadoc |

Énumérer les classes d'un jar sans dépendre d'`unzip`, qui n'est pas garanti présent : `zipfile` de la bibliothèque standard, filtrer les entrées `.class`.

### Invocation

```
javap -p -c -cp <classpath> <classe> [<classe> …]
```

**`javap` accepte plusieurs classes par invocation, et c'est le levier de performance principal.** Un processus par classe rend l'outil inutilisable sur un projet à quelques milliers de classes ; un processus par lot de quelques centaines le rend praticable. Le lot est le paramètre à régler, pas la boucle.

### Parsing

Trois familles de lignes à reconnaître, toutes stables et toutes vérifiées :

```
en-tête       class Demo$Polite implements Demo$Greeter {
              public class Foo extends Bar implements A, B {
signature       public java.lang.String run(java.util.List<java.lang.String>);
site d'appel     22: invokevirtual #29  // Method owner.name:descripteur
```

Le commentaire de désassemblage — `// Method …`, `// InterfaceMethod …` — est la source à parser. Elle est plus lisible que le pool de constantes et suffit pour tout sauf les lambdas (C1bis).

### Cache

Un index persistant, clé = chemin du conteneur + horodatage, valeur = les arêtes et la hiérarchie extraites. Un jar de dépendance ne change jamais ; `target/classes` change à chaque build.

**La leçon du cache empoisonné vaut ici aussi** : si l'indexation d'un conteneur échoue, on **n'écrit pas** une entrée vide. Un résultat vide mis en cache est indiscernable d'un résultat vide légitime, et il survit indéfiniment. On écrit l'échec, ou on n'écrit rien.

## C1bis — Les lambdas

Une invocation de lambda apparaît comme un `invokedynamic` dont le commentaire ne nomme **pas** le corps :

```
11: invokedynamic #19,  0  // InvokeDynamic #0:accept:(LDemo;Ljava/lang/StringBuilder;)Ljava/util/function/Consumer;
```

Le corps est résoluble, mais seulement via `javap -v`, dans le pool de constantes :

```
#84 = MethodHandle  5:#85  // REF_invokeVirtual Demo.lambda$run$0:(Ljava/lang/StringBuilder;Ljava/lang/String;)V
```

**Sans ce traitement, toute chaîne d'appels passant par un `forEach`, un `stream().map()` ou un `Optional.ifPresent` est coupée.** Sur du Java récent, c'est une part majeure du code métier — et le silence est total : la traversée s'arrête sans rien signaler.

C'est donc un lot à part entière, pas un raffinement. Il coûte un second passage `javap -v` sur les seules classes portant un `invokedynamic`.

---

## C2 — La hiérarchie d'appels transitive

Descendante (`callees`) et ascendante (`callers`), bornées par `scope.budget.max_traversal_depth` et par un budget de nœuds.

L'ascendante demande un **index inversé** : le bytecode donne les appelés d'une méthode, jamais ses appelants. Il se construit en une passe sur l'ensemble indexé — ce qui impose de décider, avant, quel est cet ensemble. C'est le sens de la traversée à la demande de C3.

**Chaque arrêt est journalisé** au format `boundary_hit` que la task 20 définit déjà : `depth_limit`, `infra`, `third_party`, `budget`, `unresolved_dynamic`, avec son impact. Une traversée s'arrête toujours quelque part ; ce qui distingue une bonne carte, c'est qu'elle dessine ses propres bords.

**Filtrage par défaut** : `java.*`, `javax.*`, `jakarta.*`, `sun.*`, et les paquets déclarés en exclusion du `scope.yaml`. Sans lui, la moitié du graphe est du `StringBuilder`.

---

## C3 — La traversée dans les dépendances

Le point qui distingue l'outil de tout ce qui existe côté LSP.

**Résolution du classpath** : `mvn -q dependency:build-classpath -Dmdep.outputFile=…`, ou lecture du `pom` résolu. Le résultat donne aussi, pour chaque artefact, son **groupe, son nom et sa version** — ce dont C5 et l'invariant `artifact_version` ont besoin.

**Indexation à la demande, jamais du dépôt entier.** On n'indexe un jar que lorsque la traversée y entre. Un dépôt local contient des dizaines de milliers d'artefacts dont le projet n'utilise qu'une fraction, et l'indexation exhaustive transformerait un outil en batch nocturne.

**Politique de descente** — configurable, avec un défaut prudent :

| Cible | Défaut |
|---|---|
| artefacts du même système d'information (groupe déclaré dans `profile`) | on descend |
| bibliothèques tierces | on s'arrête et on journalise `third_party` |
| JDK | on s'arrête, filtré |

La distinction est métier, pas technique : descendre dans un module frère documente le système ; descendre dans Jackson documente Jackson.

---

## C4 — Hiérarchie de types et candidats de dispatch

L'en-tête de classe donne `extends` et `implements`. Une passe sur l'ensemble indexé construit la hiérarchie complète, donc les implémentations d'une interface.

**Un appel virtuel ou d'interface rend la liste de ses candidats, jamais un choix.** C'est la règle du Cartographer, et elle n'est pas négociable :

```yaml
unresolved_dispatch:
  at: "src/…/InvoiceService.java#L88"
  expression: "gateway.send(Invoice)"
  declared_type: "com.acme.AccountingGateway"
  candidates: ["HttpAccountingGateway", "LegacyFileGateway", "NoopGateway"]
  resolution: unknown
  open_question: OQ-0xx
```

L'outil peut **réduire** la liste — une interface à implémentation unique dans le périmètre indexé est résolue — mais il ne la tranche jamais par vraisemblance. Choisir silencieusement un candidat, c'est laisser bâtir trois pages sur une supposition.

---

## C5 — Extraction depuis les `-sources.jar`

Alimente la task 13, barreaux 1 et 2.

**Le bytecode ne suffit pas ici.** Les valeurs d'annotation de rétention `CLASS` ou `RUNTIME` y sont, mais la Javadoc du barreau 2 n'y est pas du tout — et c'est le repli quand l'artefact de sources manque.

Procédure, paramétrée par `profile.contract_convention` :

1. Localiser les `-sources.jar` sous `artifact_group_path` dans le dépôt local.
2. Y chercher les fichiers dont le nom se termine par `exposed_interface_suffix`.
3. Extraire les occurrences de `annotation` et de `code_pattern`, avec la méthode qui les porte.
4. Relever le **bloc d'annotations complet** : il donne d'un coup le code, le verbe, la route et le nom d'opération. Quatre attributs pour une lecture — c'est ce qui rend le barreau 1 rentable même quand un commentaire donne déjà le code.
5. Émettre le nœud avec son `artifact`, son `artifact_version` et son `resolution_rung`.

**Repli barreau 2** : la Javadoc de l'interface de dépendance, même méthode, `confidence: C`.

**Ce que l'outil ne fait pas** : confirmer que l'appel part réellement du chemin étudié. Une classe utilitaire peut porter un contrat annoté sans être invoquée depuis le périmètre. La confirmation vient de l'index inversé de C2 — et sans elle, on documente des appels qui n'ont pas lieu.

---

## C6 — Les sorties

**JSON** pour les agents, aligné sur les schémas d'A2 : nœuds, arêtes avec leur `evidence.tool`, `boundary_hit`, `unresolved_dispatch`, `ExternalContract`.

**Mermaid** pour les diagrammes, avec **les métriques du graphe rendu** — N, E, participants. C'est ce qui rend D15 mesurable, et c'est l'entrée naturelle du `diagram-engine` d'A5.

Chaque arête porte `tool: jcallgraph/<version>`, ce qui satisfait l'invariant du Cartographer : *aucune arête sans outil*.

### Interface

```
jcallgraph index   --classpath <cp> --output .jcg/
jcallgraph callees --from <FQCN#méthode(descripteur)> --depth 5
jcallgraph callers --to   <FQCN#méthode(descripteur)> --depth 3
jcallgraph leaves  --from <entrypoint> --types database,event,contract
jcallgraph contracts --profile <scope.yaml>
```

Sortie JSON par défaut, `--mermaid` pour le rendu.

---

## C7 — Le profil en configuration

Rien de spécifique à une organisation n'est câblé. Tout vient de `profile.contract_convention` du `scope.yaml`, déjà spécifié en partie A : `annotation`, `code_pattern`, `exposed_interface_suffix`, `artifact_group_path`, `resolution_chain`.

Le profil ISOCEL est alors un fichier d'exemple, pas une branche de code.

---

## C8 — L'intégration

Comme **implémentation de la capability `code-intelligence`**, avec son plafond de confiance déclaré, aux côtés de Serena/LSP, tree-sitter et grep.

La combinaison recommandée n'est pas un remplacement : le LSP reste meilleur pour aller du texte au symbole — un site d'appel, une ligne, un nom de champ. `jcallgraph` est meilleur pour aller du symbole au graphe, et il est le seul à franchir la frontière des dépendances. Les deux sont complémentaires, et le graphe doit dire lequel a produit chaque arête.

**Le cycle 1 doit continuer de fonctionner sans C**, en mode LSP plus grep, avec le plafond correspondant. C améliore le rendement et la fiabilité ; il ne conditionne pas la méthode. C'est aussi ce qui permet de le développer en parallèle du premier run réel.

---

## Les angles morts, à écrire dans la documentation de l'outil

Un outil qui ne dit pas ce qu'il ne voit pas produit des cartes qu'on croit complètes.

| Angle mort | Effet | Traitement |
|---|---|---|
| **Réflexion**, `Class.forName`, `ServiceLoader` | l'arête n'existe pas dans le bytecode | `unresolved_dispatch` |
| **Injection de dépendances** | le type déclaré est connu, l'implémentation injectée non | candidats + question ouverte |
| **Proxies et aspects** | le comportement réel n'est mentionné nulle part dans la méthode | **hors de portée** — c'est l'angle du Challenger, à signaler comme tel |
| **Dispatch par chaîne** dans une table de gestionnaires | l'appel est visible, la cible non | `unresolved_dispatch` |
| **Génération de code** au build | l'arête existe en bytecode mais pas dans les sources | information utile : le signaler plutôt que le masquer |
| **`-sources.jar` absent** | barreau 2 inatteignable | repli barreau 3, et le dire |

Les trois premiers sont exactement les pièges que le profil Java documente déjà. `jcallgraph` ne les résout pas — **il les rend visibles et comptables**, ce qui est la seule chose honnête à en faire.

---

## Fin de partie

`jcallgraph` indexe le module étudié et ses dépendances du même système, rend une hiérarchie transitive dont chaque arête porte son outil, résout les contrats au barreau 1 quand l'artefact est là, journalise tous ses arrêts — et sa documentation liste ce qu'il ne voit pas.
