# DMAD — Ce qu'il reste à faire

> Rédigé le 2026-09-09, après la première version du chantier A.
> Complète [la spec de conception v0.4](2026-09-09-dmad-v04-corpus-std-sfd-sfg-design.md), qui dit *quoi* ; celle-ci dit *ce qui manque encore*.

## Vue d'ensemble

| Partie | Objet | Dépend de | Poids | Spec détaillée |
|---|---|---|---|---|
| **A** | Achever la v0.4 — contraindre ce qu'elle a écrit | — | moyen | [partie A](2026-09-09-partie-A-achever-v04.md) |
| **B** | Couche de preuve OKF | A2 | moyen | [partie B](2026-09-09-partie-B-couche-preuve-okf.md) |
| **C** | Outil `jcallgraph` | — | lourd, parallélisable | [partie C](2026-09-09-partie-C-jcallgraph.md) |
| **D** | Dette ouverte de la v0.3, aggravée par la cascade | — | à trancher, pas à coder | [partie D](2026-09-09-partie-D-dette-ouverte.md) |
| **E** | Le premier run réel | A1, A2 | le seul jalon qui compte | [partie E](2026-09-09-partie-E-premier-run-reel.md) |

**Ce document est la vue d'ensemble.** Chaque partie a sa spec détaillée, autonome, avec ses lots, ses critères de fin et ses questions ouvertes. Les sections ci-dessous en sont le résumé.

**L'ordre recommandé est A1 → A2 → E (sur un point d'entrée) → B ∥ C → A3-A6.** La raison est dans la partie E : tant qu'aucun run réel n'a eu lieu, tout le reste est de l'investissement à l'aveugle, et A1 est ce qui rend un run réel *évaluable*.

---

# Partie A — Achever la v0.4

La v0.4 a **écrit** ses invariants. Elle ne les **contraint** pas. Or le manifeste pose qu'un principe non contraint par un schéma est un vœu pieux, et `validate.py` s'annonce comme « le point d'application mécanique des principes ». Aujourd'hui, six décisions sur huit reposent sur la bonne volonté d'un agent et l'attention d'un relecteur.

C'est le seul endroit du projet où l'écart entre le discours et le code est visible de l'extérieur.

## A1 — Contraindre les invariants v0.4

**Ce qu'il faut vérifier**, dans `tools/validate.py` :

| Invariant | Décision | Contrôle |
|---|---|---|
| Aucun bloc de code, de requête ou de configuration dans un document du corpus | D16 | recherche des clôtures de bloc de langage dans `std/`, `sfd/`, `sfg/` |
| Tout `ExternalContract` porte sa version d'artefact | D18 | champ obligatoire, refus à l'écriture |
| Toute section de SFD référence au moins un ancrage de la STD dont elle dérive | D17 | résolution des liens `derives_from` |
| Toute règle de SFG référence au moins une règle de la SFD | D17 | idem, plus l'index inverse |
| Tout diagramme porte sa question et respecte les seuils de `scope.yaml` | D15, R1 | métadonnées du plan de diagrammes |
| Sept blocs par cas d'usage de SFG, dont « ce qui n'est pas couvert », non vide | — | structure du document |
| L'index inverse de la SFG compte autant d'entrées que le corps a de règles | — | comptage |
| Une contradiction non résolue en SFD bloque la SFG | — | état du contrôle du Curator |

**Ce qui rend le lot non trivial** : quatre de ces contrôles portent sur des documents Markdown, pas sur du YAML. `validate.py` ne sait aujourd'hui valider que des artefacts structurés contre des schémas. Il faut soit lui ajouter un mode « corpus », soit écrire un second outil — et le second choix a l'avantage de ne pas alourdir un outil qui marche.

**Fixtures obligatoires.** Chaque nouveau garde-fou reçoit sa violation dans `examples/violations/`, et `selftest.sh` vérifie qu'elle est refusée. C'est la règle déjà appliquée aux six violations existantes : un garde-fou non testé n'est pas un garde-fou.

**Fin de lot** : `./tools/selftest.sh` refuse les huit nouvelles violations, et chaque message d'erreur **nomme la décision** qu'il applique (« D16 : bloc de code en STD ») — un message qui ne dit pas quelle règle il fait respecter se fait contourner ou supprimer au premier agacement.

## A2 — Schémas des types introduits par la v0.4

`claim.schema.json` ignore encore `ExternalContract`, `BusinessObject`, `DataFlow`, `Diagram` et `Document` : son `enum` de types les refuse, et son motif d'identifiant aussi.

- `schemas/external-contract.schema.json` — dont `artifact_version` requis et `resolution_rung` contraint entre 1 et 4, avec la confiance dérivée du barreau
- `schemas/business-object.schema.json` — `functional_name`, `recursive_depth`, `business_layer`, `own_leaves[]`, `sub_objects[]`, `patterns[]`
- `schemas/document.schema.json` — `kind`, `unit`, `unit_ref`, `derives_from`, `frozen_at`
- extension de `claim.schema.json` et des `ROUTES` de `validate.py`

**Une objection à traiter d'entrée** : la partie B va changer la sérialisation de tout cela. Écrire ces schémas maintenant, c'est accepter de les réécrire. Le calcul reste favorable — ils sont petits, et l'alternative est de ne rien contraindre pendant toute la durée de B, c'est-à-dire pendant le premier run réel.

**Fin de lot** : un `ExternalContract` sans version, un `BusinessObject` nommé d'après une méthode Java et une SFD sans `derives_from` sont refusés.

## A3 — Porter le run de référence au corpus à trois documents

`examples/atlas-billing/output/` rend encore `fonctionnel/` et `technique/`. C'est le seul endroit où les gabarits STD, SFD et SFG seront éprouvés **avant** un vrai projet, et c'est aussi la vitrine de la méthode.

Produire, pour la capacité Facturation : une STD sur le point d'entrée de dispatch, une SFD sur l'arbre de business objects correspondant, une SFG sur le domaine — avec leurs tables de correspondance croisées et au moins un `ExternalContract` résolu au barreau 1.

**Fin de lot** : le run de référence passe `validate.py` **et** les nouveaux contrôles de corpus d'A1.

## A4 — Les documents non relus contre la v0.4

| Document | Ce qui manque |
|---|---|
| `docs/05-knowledge-graph.md` | les types de nœuds v0.4 et leurs arêtes ; la table des origines et confiances natives |
| `docs/10-antipatterns.md` | trois candidats nouveaux, ci-dessous, et le tableau de correspondance |
| `QUICKSTART-java.md` | les trois cycles, le choix du corpus, la convention de contrat au gate 0 |
| `settings.example.json` | les règles `deny` visent deux rédacteurs qui n'existent plus ; il en faut trois, et la SFG doit être coupée du graphe autant que du code |
| `examples/violations/README.md` | les violations ajoutées en A1 |

**Les trois anti-patterns candidats** — chacun est une défaillance observée pendant la conception, pas une hypothèse :

- **A14 — Le contrat périmé par un bump de version.** Un code de contrat relevé dans un artefact reste plausible indéfiniment après que la dépendance a changé de version. C'est l'anti-pattern que `artifact_version` existe pour rendre détectable.
- **A15 — La cascade percée.** Un rédacteur qui descend d'un étage pour combler un trou — lire le code depuis la SFD, la STD depuis la SFG. Le document redevient une lecture indépendante, et il divergera. La parade est la `gap_request` qui remonte d'un cycle.
- **A16 — Le faux barreau.** Présenter un code lu dans un commentaire manuscrit comme s'il venait du contrat. Un code faux ressemble exactement à un code vrai ; seul le barreau écrit fait la différence.

## A5 — Le `diagram-engine`

Dette héritée de la v0.3, aggravée par la v0.4 qui multiplie les diagrammes.

La règle R3 dit : « généré depuis le graphe, jamais rédigé ». Aujourd'hui le contrat est défini et **le rendu n'existe pas** : les rédacteurs écrivent du Mermaid à la main. Tant que c'est le cas, R3 est un vœu pieux, un diagramme peut contredire le texte qui l'entoure, et le badge de confiance hérité du sous-graphe n'est pas calculé mais recopié.

**Fin de lot** : un rédacteur qui écrit une syntaxe de diagramme est refusé par le validateur ; les diagrammes du run de référence sont rendus depuis le graphe.

## A6 — Fraîcheur et couverture calculées

`freshness.py` n'existe pas, et la v0.4 lui ajoute une exigence : **la péremption se propage vers le haut** — une claim de STD périmée périme les sections de SFD qui en dérivent, et ainsi de suite. Sans cette propagation, une SFG peut rester marquée fraîche alors que son socle a bougé, ce qui est exactement le pire cas : le document le plus cru est le plus périmé.

La couverture est décrite mais calculée à la main. La v0.4 y ajoute la ligne « contrats résolus par barreau », qui mesure la **qualité des sources** et pas seulement le nombre de contrats trouvés.

---

# Partie B — La couche de preuve OKF

**Objet.** Le Knowledge Graph — `claims/`, `graph/`, `contracts/`, `business-objects/` — devient un bundle Open Knowledge Format conformant. Les trois documents restent des documents humains, projetés depuis le bundle : c'est la garde d'OKF lui-même, qui dit qu'un bundle est fait pour ce qu'un agent lit, pas pour de la prose humaine.

**Ce qui rend l'opération raisonnable** : le recouvrement est presque champ pour champ. `evidence` → `sources`, la confiance dérivée → les niveaux de confiance OKF, `freshness` → `status` et `stale_after`, la promotion par test forgé → `verified: { by: process:… }`, la validation humaine d'une intention → `verified: { by: human:… }`.

## B1 — Table de correspondance des champs
Le document qui décide de tout le reste. Il doit trancher les cas où le recouvrement n'est pas exact : `confidence_reason` (sans équivalent OKF, à conserver en champ libre), `intent` et sa séparation fait/intention, `conditional_on`, `challenged_by`.

## B2 — Types de concepts et arborescence du bundle
Un `type` par nature de nœud. L'arborescence doit rester navigable par progressive disclosure — un `index.md` par répertoire.

## B3 — Migration
Les artefacts existants et le run de référence. Un convertisseur ponctuel, pas un pont permanent : on ne maintient pas deux formats.

## B4 — Validation
`okf-validate --strict` intégré à `validate.py` et posé en gate. Le mode strict échoue sur les concepts orphelins et les liens morts — c'est exactement ce qu'on veut : **une preuve qu'aucun chemin n'atteint est une preuve absente.**

## B5 — `index.md` et `log.md`
Générés et maintenus à chaque écriture. Le journal est append-only, ce qui se marie bien avec la contrainte git déjà posée.

## B6 — Fraîcheur
`status` et `stale_after` remplacent le bloc `freshness`. À faire **après** A6, ou à faire *à la place* d'A6 si B est priorisé — les deux implémentent la même chose.

## Ce qui reste ouvert dans B
Le placement des trois documents. La décision actuelle les laisse hors du bundle. L'alternative — chaque section de STD, chaque business object, chaque cas d'usage devenant un concept lié — rendrait la cascade **mécaniquement vérifiable par le validateur de liens** : une section de SFD sans lien vers son ancrage STD deviendrait un orphelin détecté. C'est séduisant et ça se paie en confort de lecture humaine. À trancher au début de B, pas maintenant.

---

# Partie C — L'outil `jcallgraph`

**Objet.** Une CLI Python adossée à `javap`, sans build ni dépendance : le JDK est déjà présent puisque le projet compile.

**Ce qu'elle apporte que rien d'autre ne fait** : la traversée **transitive** (les outils de navigation ne rendent qu'un niveau) et le franchissement **vers l'intérieur des dépendances** (le LSP n'indexe pas `~/.m2`).

## C1 — Index bytecode
Lecture de `target/classes` et des jars de `~/.m2` via `javap -p -c`. Extraction des instructions d'invocation : owner, nom, descripteur. **Zéro faux positif de grep** — c'est l'argument principal du choix.

## C2 — Hiérarchie d'appels transitive
Descendante et ascendante, bornée par profondeur et par budget, avec journalisation des arrêts au format `boundary_hit` déjà défini par la task 20.

## C3 — Traversée dans les dépendances
Le point qui distingue l'outil. Résolution du classpath depuis `dependency:list` ou le `pom` résolu, puis indexation à la demande des jars traversés — pas de l'intégralité du dépôt local.

## C4 — Hiérarchie de types et candidats de dispatch
Lue au même endroit. Un appel virtuel rend **la liste de ses candidats**, jamais un choix. C'est la règle du Cartographer : on ne devine pas, on pose un nœud `unresolved_dispatch`.

## C5 — Extraction d'annotations depuis les `-sources.jar`
Alimente la task 13, barreaux 1 et 2. Le bytecode ne suffit pas : la Javadoc du barreau 2 n'y est pas, et les valeurs d'annotation ne sont lisibles proprement que dans les sources.

## C6 — Sorties
JSON pour les agents, Mermaid pour les diagrammes — ce dernier alimentant naturellement le `diagram-engine` d'A5.

## C7 — Profil ISOCEL en configuration
L'annotation, le motif de code, le suffixe d'interface exposée, la chaîne de résolution, le groupe d'artefacts. Rien de tout cela n'est câblé en dur : c'est ce que `profile.contract_convention` de `scope.yaml` déclare déjà.

## C8 — Intégration
Comme implémentation de la capability `code-intelligence`, avec son plafond de confiance, et comme outil des tasks 13 et 20.

**Le cycle 1 doit continuer de fonctionner sans C**, en mode dégradé LSP plus grep, avec le plafond correspondant. C améliore le rendement et la fiabilité ; il ne conditionne pas la méthode.

---

# Partie D — La dette ouverte, aggravée par la cascade

Ce sont des décisions à prendre, pas du code à écrire. Trois d'entre elles sont plus pressantes qu'en v0.3.

**D1 — La signature des validations humaines.** Question ouverte n° 3 de la v0.3, aggravée : la v0.4 a **trois revues de cycle**, donc trois signatures à tracer, et la revue de cycle 3 est le seul endroit où une intention peut monter de `H` à `C`. Il faut décider qui signe, comment c'est enregistré, et surtout **ce que devient une validation quand le code change ensuite**. Sans réponse, la seule promotion qu'un humain puisse prononcer n'est pas traçable.

**D2 — La calibration de l'échelle.** `V/C/I/H`, le seuil de trois signaux sur quatre, la fourchette de 15 à 30 % de findings, la conversion en pourcentage : ce sont des conventions raisonnées, pas des mesures. La partie E est ce qui les mesure.

**D3 — Le multi-dépôts.** Un legacy est rarement un seul dépôt. La traversée dans les dépendances de C en attaque un cas particulier — lire une dépendance figée — mais pas le cas général de plusieurs dépôts vivants.

**D4 — La confidentialité.** Le champ existe dans `scope.yaml`, le mécanisme d'application n'est pas spécifié. Bloquant pour tout usage en prestation, et inchangé depuis la v0.3.

**D5 — Le nom.** « DMAD » se lit *mad* en anglais. À trancher avant publication, pas après.

---

# Partie E — Le premier run réel

**Ce n'est pas un chantier de développement, et c'est le seul jalon qui compte.** Tant qu'il n'a pas eu lieu, DMAD est une spécification cohérente — ce qui ne prouve rien, et la v0.4 vient d'en ajouter trois cents lignes.

Le plus petit run utile est cadré : `examples/std-seule/`, un point d'entrée, `corpus: [std]`. Il ne demande qu'un développeur, pas d'expert métier, et il exerce déjà tout le cycle 1 — y compris la résolution des contrats, qui est la partie la plus neuve.

**Trois chiffres en sortent, et ce sont eux qui décident de la suite :**

1. **Le coût réel par étape**, en tokens et en temps. L'hypothèse du design — le modèle fort n'est payé qu'au découpage et à la réfutation — n'a jamais été vérifiée.
2. **Le taux de findings du Challenger.** À 3 %, il est complaisant et tout l'édifice de confiance s'effondre. À 70 %, l'Elucidator est inutilisable en l'état.
3. **La justesse par échantillonnage.** Cinq claims tirées au hasard, le code ouvert aux lignes citées. Plus d'une erreur sur cinq condamne le run.

**Ce que le run doit aussi produire** : une entrée de journal disant ce qui a été appris. C'est la pratique du corpus `skills-doc`, et c'est la partie la plus utile de ses skills — y compris les règles qui se sont révélées fausses et ont été remplacées.

**Prérequis minimal côté A** : A1, pour que les invariants soient vérifiés plutôt que constatés. A2 suit immédiatement, puisque A1 en dépend. Le reste peut attendre le retour du terrain — et sera meilleur pour l'avoir attendu.
