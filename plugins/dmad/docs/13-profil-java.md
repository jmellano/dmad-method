# DMAD — Profil Java

Java/JVM est le terrain le plus favorable à DMAD, pour trois raisons : le typage statique rend l'analyse fiable **sans exécution ni compilation**, une grande partie des règles est **déclarative** (donc de niveau `V` sans effort), et l'outillage de test permet de forger des preuves exécutables.

Ce document dit **où chercher quoi** dans un legacy Java. À lire avant le premier run.

## Avant de lancer : rendre le projet analysable

L'analyse syntaxique n'a **pas** besoin que le projet compile. C'est la principale vertu de `jcallgraph` sur un legacy Java, où la compilation est souvent le premier obstacle et parfois un obstacle définitif.

Les dépendances résolues restent utiles — pour la traversée dans les artefacts et la résolution des contrats sortants au barreau 1 — mais elles ne conditionnent plus le run.

```bash
mvn -q -DskipTests dependency:go-offline   # ou : mvn -q -DskipTests compile
./gradlew --offline compileJava
java -version                              # la version du JDK doit correspondre au projet
```

> **Ce que l'analyse prouve, question par question, est dans le skill embarqué [`code-intelligence-java`](../skills/code-intelligence-java/SKILL.md).** À lire avant la première traversée : le plafond de confiance s'y dérive de ce qu'on demande, pas de l'outil qui répond (D23).

| Situation | Conséquence | Que faire |
|---|---|---|
| Le projet ne compile pas | l'analyse fonctionne | rien de bloquant ; les contrats sortants retomberont au barreau 3 ou 4 |
| Dépendances non résolues | pas de traversée dans les artefacts | tenter `dependency:go-offline` ; sinon **le déclarer**, et accepter des contrats non résolus |
| Version du langage inconnue | l'analyse peut buter sur une construction récente | renseigner `profile.jdk_version` dans `scope.yaml` |

**Règle :** ce qui n'a pas pu être résolu s'écrit dans `scope.yaml` et s'affiche dans le bandeau. Un contrat non résolu porte un placeholder visible — **jamais un code plausible**.

## Les points d'entrée Java

| Famille | Où chercher |
|---|---|
| HTTP | `@RestController`, `@Controller`, `@RequestMapping`, `@GetMapping`… · JAX-RS `@Path` · `web.xml` + `HttpServlet` · Struts `struts-config.xml` / `@Action` |
| Planifié | `@Scheduled` · Quartz (`Job`, `Trigger`, tables `QRTZ_*`) · `TimerTask` |
| Messages | `@JmsListener`, `@KafkaListener`, `@RabbitListener` · `MessageDriven` (MDB) |
| Batch | Spring Batch (`Job`, `Step`, `ItemReader/Processor/Writer`) · `public static void main` |
| Événements | `@EventListener`, `ApplicationListener` · `@PostConstruct` avec effets |
| SOAP | `@WebService`, WSDL, `@Endpoint` |
| **Hors code** | **ordonnanceur externe** (Control-M, $U, Rundeck) appelant un `main()` · **triggers et procédures stockées** |

Les deux dernières lignes sont celles qu'on rate. Elles n'apparaissent **nulle part dans le dépôt** : réclamer la configuration de l'ordonnanceur et le DDL complet au gate 0.

## Les règles de gestion déclaratives — le meilleur rendement

C'est la spécificité Java qui change tout : **beaucoup de règles sont annotées, donc mécaniquement extractibles en niveau `V`**, sans interprétation et sans risque d'hallucination.

| Source | Ce que ça donne | Niveau |
|---|---|---|
| **Bean Validation** (`@NotNull`, `@Size`, `@Min`, `@Pattern`, `@Past`, contraintes maison) | obligations, formats, plages | **V** |
| **JPA** (`@Column(nullable, length, precision, scale)`, `@Enumerated`, `@Version`) | modèle de données, précision des montants | **V** |
| **Relations JPA** (`@OneToMany`, `cascade`, `orphanRemoval`, `fetch`) | règles de cycle de vie et de suppression en cascade | **V** |
| **Contraintes en base** (DDL, `CHECK`, `UNIQUE`, FK) | invariants non contournables | **V** |
| **Migrations** Flyway / Liquibase | l'évolution du métier dans le temps | **V** |
| **Sécurité** (`@PreAuthorize`, `@Secured`, `@RolesAllowed`) | qui a le droit de faire quoi | **V** |
| `@Transactional` (propagation, `rollbackFor`, `readOnly`) | frontières transactionnelles | **V** |

**Commence toujours par là.** Sur un projet Spring/JPA typique, cette passe seule produit plusieurs dizaines de règles prouvées en quelques minutes, avant même que le moindre modèle n'interprète une ligne de code.

## Les pièges spécifiques Java

### Le dispatch par IoC — le plus important
Spring résout les implémentations à l'exécution. `find_implementations` donne les candidats ; **il ne dit pas lequel est injecté**.

À vérifier systématiquement : `@Primary` · `@Qualifier` · `@Profile` · `@ConditionalOnProperty` / `@ConditionalOnMissingBean` · configuration XML héritée · `@Component` scanné vs `@Bean` déclaré.

Sans réponse tranchée → nœud `unresolved_dispatch` avec les candidats et une question ouverte. **Ne jamais choisir le plus probable.**

### L'AOP invisible
`@Aspect`, `@Around`, `@Before`, intercepteurs, proxies CGLIB/JDK. Le comportement réel d'une méthode peut être **entièrement modifié par du code qui ne la mentionne pas**, et qu'aucune traversée d'appels ne trouvera.

C'est l'angle 4 du Challenger, et sur du Spring legacy il est loin d'être théorique : recenser tous les `@Aspect` du périmètre **avant** la phase 4, et vérifier leurs pointcuts contre les classes documentées.

### Les profils Spring
`application-prod.yml`, `application-recette.yml`, `@Profile("prod")`, `@ConditionalOnProperty`. C'est la source Java numéro un de l'anti-pattern A3 (documentation vraie en recette, fausse en production).

Renseigner `conditional_on.observed` **par profil**, en comparant systématiquement la valeur par défaut du dépôt à celle de production.

### Les montants
`float`/`double` pour de l'argent est un bug de gestion, pas un détail. Vérifier : `BigDecimal` vs primitifs · `setScale()` et `RoundingMode` · `@Column(precision, scale)` vs la précision du calcul · la précision d'affichage.

**Un écart entre la précision calculée et la précision stockée est une règle de gestion à documenter**, pas une coquille.

### Lombok
`@Data`, `@Builder`, `@EqualsAndHashCode` génèrent des accesseurs **qui n'existent pas dans les sources**. Une analyse syntaxique ne les voit donc pas : un appel à `getMontant()` sur une classe annotée peut n'avoir aucune déclaration correspondante.

Ce n'est pas une panne, c'est une arête que l'outil ne peut pas poser. Elle se traite comme un dispatch non résolu : signalée, jamais devinée.

### L'héritage profond et les classes abstraites
Les hiérarchies à 4-5 niveaux sont fréquentes dans les legacy Java. Une règle définie dans une classe mère peut être redéfinie n'importe où en dessous : `type_hierarchy` avant toute affirmation d'exhaustivité.

### La réflexion et les usines
`Class.forName()`, `ServiceLoader`, dispatch par chaîne dans une `Map<String, Handler>`. Même traitement que l'IoC : candidats + question ouverte.

## La résolution des contrats sortants

Un appel HTTP sortant vers un autre module d'un même système d'information porte en général un **code de contrat**. C'est la clé d'entrée de son exploitation : propriétaire, supervision, contrat. La task 13 en fait un nœud `ExternalContract`, feuille du graphe.

**Le code se lit à quatre endroits de fiabilité très inégale**, et le barreau atteint détermine la confiance :

| Barreau | Où | Confiance |
|---|---|---|
| 1 | l'annotation de contrat sur l'interface exposée du module appelé, **dans l'artefact de la dépendance** | `V` |
| 2 | la Javadoc de l'interface de dépendance, générée depuis la même source | `C` |
| 3 | un commentaire manuscrit dans le code appelant | `I` |
| 4 | le placeholder | — |

**Le chemin d'accès est le point délicat.** Le code appelant n'importe pas l'interface annotée : il importe une interface de service applicatif qui ne porte aucune annotation. La chaîne générée typique compte trois ou quatre maillons entre l'import et l'annotation. Le motif de nommage se déclare dans `scope.yaml` au gate 0 — sans lui, la résolution retombe au barreau 3.

**Ce qu'aucune navigation de symboles ne fait ici.** L'annotation vit dans un `-sources.jar` du dépôt Maven local, **hors du périmètre analysé**. C'est de la lecture d'archive, pas de la navigation.

`unzip` n'est pas garanti présent sur un poste agent. Passer par Python :

```python
import zipfile, pathlib, re
root = pathlib.Path.home() / ".m2/repository" / GROUP_PATH
pat  = re.compile(ANNOTATION_REGEX)          # déclaré dans scope.yaml
for jar in root.rglob("*-sources.jar"):
    z = zipfile.ZipFile(jar)
    for name in z.namelist():
        if name.endswith(EXPOSED_INTERFACE_SUFFIX):
            for code in pat.findall(z.read(name).decode("utf-8", "replace")):
                print(code, jar.name, name.split("/")[-1])
```

**Deux mises en garde.**

L'échelle vaut pour les appels **sortants**. Les points d'entrée du module étudié n'ont pas d'artefact dans le dépôt local — un module ne dépend pas de sa propre API. Pour documenter les contrats entrants, lire les sources du module lui-même. Chercher un artefact qui n'existe pas coûte longtemps.

**Le module appelé est figé à la version de la dépendance.** L'artefact lu porte un numéro qui n'est pas celui du module étudié : un code relevé décrit le contrat **tel que le module étudié le consomme**, pas tel que le module appelé le publie aujourd'hui. C'est pourquoi `artifact_version` est obligatoire sur le nœud.

## Les tests de caractérisation en Java

Terrain favorable : JUnit 5 + AssertJ + Mockito, et Testcontainers quand une base est nécessaire.

```java
@Test
void une_facture_a_montant_nul_n_est_pas_transmise_au_SI_comptable() {
    Invoice invoice = anInvoice().withTotalTTC(ZERO).build();
    dispatcher.dispatch(invoice);
    assertThat(accountingGateway.sentInvoices()).isEmpty();
    assertThat(invoice.getStatus()).isEqualTo(SKIPPED);
}
```

**Ordre de facilité** — méthode statique pure ✅ · service avec dépendances injectables ✅ · service avec `new` en dur ⚠️ *(seam manquant, à signaler)* · code accédant à un singleton statique ❌ · code lisant l'horloge système ❌ *(seam manquant)*

Les deux derniers cas ne sont pas des échecs : ce sont des **seams manquants identifiés**, à documenter dans `70-seams.md`. C'est exactement ce que la task 51 appelle un « résultat précieux ».

## Les seams Java typiques

Par ordre de coût croissant : interface à implémentation unique (le point d'injection existe déjà) · `@Bean` de configuration (remplaçable par un profil de test) · client HTTP encapsulé (`RestTemplate`/`Feign` mockable) · appel statique (nécessite une extraction) · `new` en dur (nécessite une injection).

## Le schéma de données

Trois sources, à croiser :
1. **DDL réel** — la vérité. Réclamer un export au gate 0.
2. **Migrations** Flyway/Liquibase — l'histoire du métier.
3. **Entités JPA** — le modèle *tel que le code le croit*.

> **Les écarts entre les trois sont de l'information de première qualité.** Une colonne en base absente de l'entité, un `nullable=false` côté JPA sans `NOT NULL` en base : chacun raconte quelque chose, et mérite une question ouverte.

## Checklist avant le run de demain

- [ ] Le projet compile (ou le mode dégradé est acté et annoncé)
- [ ] Le JDK correspond
- [ ] `jcallgraph` répond sur un symbole de test
- [ ] Historique git complet (`git log --oneline | wc -l` cohérent avec l'âge du projet)
- [ ] DDL ou accès base disponible
- [ ] Configuration de l'ordonnanceur externe réclamée
- [ ] Configuration de production accessible (profils, flags) — **sinon l'anti-pattern A3 est garanti**
- [ ] Rapport de couverture si un build le produit
- [ ] Vocabulaire métier d'amorce collecté auprès d'un humain, pas déduit du code
- [ ] **Convention de contrat d'API déclarée** — quelle annotation, quel suffixe d'interface exposée, quel groupe d'artefacts. Sans elle, la résolution des contrats retombe au barreau 3
- [ ] **Corpus visé décidé** — STD seule, jusqu'à la SFD, ou complet
- [ ] **Seuils de lisibilité** actés (défaut : N ≤ 12, E ≤ 15, McCabe ≤ 10)
