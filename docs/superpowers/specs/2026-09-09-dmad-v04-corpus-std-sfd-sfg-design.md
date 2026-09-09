# DMAD v0.4 — Le corpus STD → SFD → SFG

> Spec de conception du **chantier A**. Rédigée le 2026-09-09.
> Chantiers B (couche de preuve OKF) et C (outil `jcallgraph`) : hors périmètre de cette spec, cadrés en § 8.

## 1. Le problème

DMAD v0.3 est une méthode d'enquête aboutie — chaîne de preuve, échelle `V/C/I/H` dérivée, agent adversarial, gates humains — mais sa **restitution est sous-spécifiée**. Elle produit une arborescence `dmad-output/fonctionnel|technique` dont le contenu tient en une liste de fichiers et un bandeau.

À l'inverse, le corpus `skills-doc` porte une doctrine de rédaction éprouvée sur des livrables réels — cadre ISO 25010, leviers *length*/*depth*, critère de complexité de graphe, quatre diagrammes cardinaux, vue récursive par business object, dix-sept sections de STD, échelle de résolution des contrats sortants — mais **presque aucune machinerie d'enquête** : pas de chaîne de preuve, pas de challenge adversarial, pas de mesure de couverture.

Les deux se complètent exactement là où l'autre est faible. v0.4 les fusionne.

## 2. Ce que v0.4 change

**Un corpus à trois documents, en cascade d'abstraction.**

```
code ──► STD ──► SFD ──► SFG
        technique  fonctionnel  métier
        détaillé   détaillé     général
```

Chaque document s'appuie sur le précédent, dont il est une abstraction. Chaque étage est **aveugle à l'étage n−2** : la SFD ne lit pas le code, la SFG ne lit ni le code ni le graphe.

C'est le renforcement de la décision D3 de v0.3 (« les rédacteurs n'ont pas accès au code »), généralisée en **échelle de lecture**.

## 3. Les arbitrages (ADR D15 à D22)

Reportés dans `plugins/dmad/docs/08-decisions.md`, résumés ici.

| | Décision |
|---|---|
| **D15** | Les seuils de lisibilité des diagrammes sont **paramétrables**, valeurs par défaut `skills-doc` : N ≤ 12 nœuds, E ≤ 15 arêtes, McCabe ≤ 10 |
| **D16** | **Aucun bloc de code ni de SQL** dans aucun des trois documents. La STD porte des références ; SFD et SFG sont agnostiques du code |
| **D17** | **Échelle de lecture en cascade** : STD lit graphe + claims ; SFD lit STD + claims ; SFG lit SFD |
| **D18** | Un **contrat sortant** (`@Cusi` et assimilés) est une **feuille du graphe**, au même titre qu'un accès BDD ou un événement — et porte la **version de l'artefact** où il a été lu |
| **D19** | **Trois cycles emboîtés**, chacun scellé par une revue humaine avec corrections et compléments |
| **D20** | **Trois unités documentaires distinctes** : STD par point d'entrée, SFD par arbre de business objects, SFG par cas d'usage |
| **D21** | Le **gate 3** (découpage en capacités) migre en tête du cycle 2 |
| **D22** | Le **modèle** de connaissance est spécifié ici ; sa **sérialisation** relève du chantier B |

## 4. Le pipeline

```
Cycle 0 — CADRAGE
  Scoper : périmètre, budget, glossaire d'amorce, seuils de lisibilité,
           profil (Java/Maven, ISOCEL on/off), documents visés
  ⛔ gate-0-scope

Cycle 1 — STD                 unité : le point d'entrée        registre : mécanique
  Surveyor           inventaire, points d'entrée, hotspots, résolution Maven,
                     protocole de démarrage LSP, contrôle du JDK
  Cartographer       graphe d'appels transitif, feuilles typées, hiérarchie de
                     types, dispatch non résolu
  Contract Resolver  échelle à quatre barreaux, contrats sortants + version d'artefact
  Challenger         angles techniques
  Diagram Planner    plan de diagrammes, seuils appliqués
  Writer:STD         dix-sept sections, références seules
  ⛔ revue-cycle-1-std — corrections / compléments — STD figée

Cycle 2 — SFD                 unité : l'arbre de business objects
  Carver             capacités, business objects, patterns, seams
  ⛔ gate-3-capabilities
  Elucidator         cas d'usage, règles, ISO 25010, niveaux d'abstraction
  Challenger         angles interprétatifs
  Test Forger        seul chemin vers V
  Diagram Planner    plan de diagrammes par niveau
  Writer:SFD         analyse bas → haut, rédaction haut → bas
  ⛔ revue-cycle-2-sfd — corrections / compléments — SFD figée

Cycle 3 — SFG                 unité : le cas d'usage
  Archaeologist      intention, plafond H sans exception
  Elucidator         arbitrage des règles partagées, traduction du vocabulaire
  Curator            contrôle de cohérence — bloquant
  Challenger         angles de promesse
  Writer:SFG         sept blocs par cas d'usage, index inverse
  ⛔ revue-cycle-3-sfg — corrections / compléments — SFG figée
```

**Justification des trois unités.** Le frontmatter du skill STD porte `entry_point_type` et `entry_point_name` : une STD documente une porte d'entrée du système. La SFD est une vue récursive sur un arbre de business objects — un processus, pas une porte. La SFG se découpe par cas d'usage, unité d'évolution. Rendre les trois selon un découpage unique forcerait deux d'entre eux dans un plan qui ne leur appartient pas.

**Justification du déplacement du gate 3.** Une STD par point d'entrée se produit sans savoir quelles capacités métier existent. Le découpage en capacités est une question métier, dont dépend l'organisation de la SFD et de la SFG — pas celle de la STD. Sa place est la porte d'entrée du fonctionnel.

**Critère d'arrêt.** Le budget épuisé s'arrête sur un **document terminé**, généralisation de la règle v0.3 (« une capacité terminée plutôt que six ébauches »). Une STD seule est un livrable défendable ; une SFD dont la STD n'a pas été revue ne l'est pas.

## 5. Le casting

| Agent | Cycle | Évolution |
|---|---|---|
| `Scoper` | 0 | + seuils, profil, documents visés, prérequis outillage |
| `Surveyor` | 1 | + résolution Maven, protocole LSP en deux temps, contrôle du JDK |
| `Cartographer` | 1 | + traversée transitive, feuilles typées, hiérarchie de types |
| **`Contract Resolver`** | 1 | **nouveau** — échelle à quatre barreaux |
| `Carver` | 2 | + patterns GoF/CQRS, identification des business objects |
| `Elucidator` | 2, 3 | + ISO 25010, niveaux d'abstraction, arbitrage `length`/`depth` |
| `Archaeologist` | 3 | inchangé, déplacé en cycle 3 |
| `Challenger` | 1, 2, 3 | + angles par registre |
| `Test Forger` | 2 | inchangé |
| `Diagram Planner` | 1, 2 | + quatre diagrammes cardinaux, seuils paramétrables, règle de nommage |
| **`Writer:STD`** | 1 | remplace `Writer:Technical` |
| **`Writer:SFD`** | 2 | remplace `Writer:Functional` |
| **`Writer:SFG`** | 3 | **nouveau** |
| `Curator` | 3 | + cohérence inter-documents, index inverse, glossaire imposé |

Deux skills prérequis embarqués, consommés par plusieurs agents : `patterns-gof-cqrs` (grille de reconnaissance) et `code-intelligence-java` (protocole de démarrage LSP et ses modes de défaillance).

## 6. Le modèle de connaissance

Nouveaux types de nœuds par rapport à v0.3. La sérialisation relève du chantier B.

| Type | Strate | Champs propres | Confiance native |
|---|---|---|---|
| `ExternalContract` | données | `code`, `http_verb`, `route`, `operation`, `artifact`, `artifact_version`, `resolution_rung` | `V` au barreau 1, `C` au 2, `I` au 3 |
| `BusinessObject` | métier | `functional_name`, `recursive_depth`, `business_layer`, `own_leaves[]`, `sub_objects[]`, `patterns[]` | `I` |
| `DataFlow` | données | `purpose` (traitement \| contrôle), `availability` (initiale \| ad-hoc), `direction`, `normality` (normale \| anormale) | `V` si typé par outil |
| `Diagram` | transverse | `question`, `kind`, `scope`, `metrics` (N, E, McCabe), `badge` | héritée du sous-graphe |
| `Document` | transverse | `kind` (STD \| SFD \| SFG), `unit`, `unit_ref`, `derives_from`, `frozen_at` | minimum de ses claims |

`ExternalContract` sans `artifact_version` est refusé à l'écriture : un contrat décrit ce que le module **consomme**, figé à la version de la dépendance, pas ce que le module appelé publie aujourd'hui. Sans le champ, la preuve devient fausse au prochain bump sans que rien ne le signale.

## 7. Les invariants vérifiables

Applicables mécaniquement, en gate de fin de cycle.

1. Aucune clôture de bloc de code de langage (```` ```java ````, ```` ```sql ````, ```` ```xml ````) dans un document du corpus — **D16**.
2. Toute section de SFD référence au moins un ancrage de la STD dont elle dérive — **D17**.
3. Toute règle de SFG référence au moins une règle de la SFD dont elle dérive — **D17**.
4. Tout diagramme porte sa question et respecte les seuils déclarés dans `scope.yaml` — **D15**.
5. Toute feuille externe porte son type ; tout `ExternalContract` porte sa version d'artefact — **D18**.
6. Toute contradiction non résolue dans la SFD **bloque** la production de la SFG — une contradiction laissée en SFD deviendrait une promesse fausse faite à l'utilisateur, indétectable par son lecteur.
7. Tout diagramme d'états suppose un champ d'état réel et des transitions repérables — règle v0.3 conservée.

## 8. Hors périmètre

**Chantier B — couche de preuve OKF.** Les `claims/` et le `graph/` deviennent un bundle OKF conformant : un concept par claim, `sources` / `generated` / `verified` / `status` / `stale_after` à la place des champs maison, `index.md` par répertoire, `log.md` append-only, `okf-validate --strict` en gate. Cette spec nomme les concepts et leurs champs (§ 6) sans figer leur format de stockage, précisément pour que B soit une sérialisation et non une réécriture.

**Chantier C — outil `jcallgraph`.** CLI Python adossé à `javap`, sans build ni dépendance : lecture du bytecode de `target/classes` et des jars de `~/.m2`, arêtes d'appel exactes, traversée transitive à l'intérieur des dépendances, hiérarchie de types pour les candidats du dispatch, extraction d'annotations depuis les `-sources.jar`, sortie JSON et Mermaid. Profil ISOCEL en configuration.

Le cycle 1 est spécifié pour fonctionner **sans** C, en mode dégradé LSP + grep, avec le plafond de confiance correspondant. C améliore le rendement et la fiabilité du cycle 1 ; il ne le conditionne pas.

## 9. Ce que cette spec ne tranche pas

- La calibration de l'échelle `V/C/I/H` reste une convention, comme en v0.3. Le premier run réel la mesurera.
- Le mécanisme de signature des validations humaines (question ouverte n° 3 de v0.3) reste ouvert et devient plus pressant : trois revues de cycle produisent trois signatures à tracer.
- Le multi-dépôts reste ouvert. La traversée dans les dépendances Maven du chantier C en attaque un cas particulier — lire une dépendance figée — mais ne résout pas le cas général d'un legacy réparti sur plusieurs dépôts vivants.
