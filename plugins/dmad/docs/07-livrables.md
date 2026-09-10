# DMAD — Livrables

## Le bundle d'abord, le document ensuite

Depuis la v0.4, **les rédacteurs n'écrivent pas de document** : ils écrivent des **concepts** dans le bundle OKF, et un **plan** les recompose en un fichier par audience (D26).

```
claims, graphe ──► concepts OKF ──► [plan-std.yaml] ──► STD-<processus>.md
                    LIVRABLE 1                            LIVRABLE 2, dérivé
```

```bash
python3 tools/okf-compose.py <bundle> --all <run>
```

Une correction se fait **dans le concept**, jamais dans le fichier composé — une édition faite là est perdue à la régénération suivante.

**Le plan de niveau 1 est imposé** : onze chapitres en STD, dix en SFD, six en SFG. Les sous-sections sont un **résultat de l'analyse** — le nombre de niveaux d'une vue récursive, le nombre de cas d'usage. Une section dont le sujet n'existe pas **ne se supprime pas** : elle porte son constat d'absence et son périmètre.

## Le corpus

Depuis la v0.4, DMAD produit un **corpus à trois documents en cascade d'abstraction** : STD, puis SFD, puis SFG. Ce ne sont pas trois rendus parallèles du même graphe — c'est une suite où chaque document est l'abstraction du précédent, et où **chaque étage est aveugle à l'étage n−2** (D17).

```
dmad-output/
├── 00-index.md                    # portail, périmètre, couverture, mode d'emploi des badges
│
├── std/                           # cycle 1 — un document par point d'entrée
│   └── <point-d-entree>.md
│
├── sfd/                           # cycle 2 — un document par arbre de business objects
│   └── <processus>.md
│
├── sfg/                           # cycle 3 — un document par domaine, découpé par cas d'usage
│   └── <domaine>.md
│
├── preuves/
│   ├── claims/                    # une claim = un fichier
│   ├── contracts/                 # les contrats sortants résolus, avec leur barreau et leur version
│   ├── business-objects/          # les BO, leurs niveaux, leurs feuilles propres
│   ├── index.json
│   ├── open-questions.md          # registre consolidé, priorisé
│   ├── challenges.md              # journal des réfutations du Challenger
│   └── couverture.md              # ⚠️ quelle part du code a été atteinte
│
└── tests/characterization/        # les tests forgés qui prouvent les règles
```

## Les trois documents

| | STD | SFD | SFG |
|---|---|---|---|
| Lecteur | développeur, architecte, ops | analyste, MOE, MOA | utilisateur métier, PO |
| Question | « comment, et où je touche ? » | « que fait le processus, avec quelles données ? » | « qu'est-ce que je peux attendre du système ? » |
| Unité | le point d'entrée | l'arbre de business objects | le cas d'usage |
| Lit | le graphe et les claims | la STD et les claims | la SFD |
| Vocabulaire | technique, noms réels du code | métier, noms fonctionnels | métier exclusivement |
| Références | `fichier:lignes`, signatures | vers les niveaux et les business objects | vers les cas d'usage |

**Interdit commun aux trois — D16 : aucun bloc de code, aucune requête SQL, aucun fragment de configuration.** La STD porte des références ; la SFD et la SFG ignorent jusqu'à l'existence du code. Un lecteur qui veut voir la requête ouvre le dépôt : c'est le prix d'un document dont chaque phrase a franchi la chaîne de preuve, et c'est aussi ce qui l'empêche de vieillir à la première reformulation.

Chaque document porte en tête une **table de correspondance** vers ses voisins — c'est elle qui permet de passer d'une unité documentaire à l'autre (D20).

---

## La STD — dix-sept sections

Ordre imposé. **Aucune section n'est jamais omise** : une section dont le sujet n'existe pas dans le point d'entrée se remplit avec le constat d'absence et son périmètre.

| # | Section | Contenu | Obligatoire ? |
|---|---|---|---|
| 1 | **Cartographie des composants** | vue structurelle : câblage + un diagramme de classes par couche, chacun suivi de sa phrase de lecture. Se termine par **1.5 cohésion et couplage** | ✅ |
| 2 | **Configuration** | tableau `Propriété \| Valeur` — job, steps, taille de lot, politique de rejet, points d'entrée, contrats couverts | ✅ |
| 3 | **Architecture du flux** | enchaînement des étapes + explication des branches conditionnelles | ✅ |
| 4 | **Détail par étape** | un paragraphe par étape, **par références** — signatures et `fichier:lignes`, jamais d'extrait | ✅ |
| 5 | **Traitement unitaire** | phases séquentielles, gardes, comportement transactionnel | ✅ |
| 6 | **Séquence technique** | diagramme de séquence avec noms de classes et de méthodes exacts | ✅ |
| 7 | **Modèle de données** | tables lues / tables écrites + colonnes manipulées | si BDD |
| 8 | **Requêtes clés** | une entrée par requête : **référence, tables et colonnes touchées, intention** — jamais le SQL | si SQL non trivial |
| 9 | **Appels externes** | tableau `Code \| Barreau \| Artefact:version \| Interface \| Méthode \| Contexte`, conditions et comportement d'échec | ✅ |
| 10 | **Événements** | consommés et émis, payload, cardinalité, idempotence | si applicable |
| 11 | **Mapping et transformations** | mappings non triviaux uniquement | si applicable |
| 12 | **Gestion des erreurs** | hiérarchie · propagation · exceptions métier, techniques, **non déclarées** · sources d'infrastructure · **sémantique de la reprise** · sorties dégradées · **chemins inatteignables et pièges d'attribution** | ✅ |
| 13 | **Dépendances** | non-standard uniquement | si pertinent |
| 14 | **Points d'attention** | liste numérotée | ✅ |
| 15 | **Cas de test** | pré-condition / action / attendu | ✅ |
| 16 | **Références croisées** | SFD associée, SFG, STD comparables, objets métier | ✅ |
| 17 | **Historique** | `Version \| Date \| Auteur \| Description` | ✅ |

**Le plus grand gain de la règle « jamais omettre » est le piège d'attribution** : signaler explicitement les artefacts *voisins* qui ressemblent à ce que le lecteur cherche mais n'appartiennent pas au périmètre. C'est ce qui évite qu'un développeur optimise une requête que ce batch n'exécute jamais.

**La section 1.5 — cohésion et couplage.** Elle qualifie les composants réels sur l'échelle de la matrice, du plus fort au plus faible, chaque ligne citant un fait déjà documenté ailleurs dans le document. Elle ne redécouvre rien : elle **rassemble sous le critère**. Une ligne dont le fait est introuvable ailleurs signale soit un manque, soit une qualification faible. Une seconde table fait de même pour les couplages problématiques.

---

## La SFD — vue récursive par business object

La SFD répond à « d'où vient cet objet ? » là où une vue par phase répond à « que fait le processus, dans quel ordre ? ». Elle **complète** les vues classiques sans les remplacer.

**On analyse bas → haut, on rédige haut → bas.** L'analyse part des feuilles et remonte ; la rédaction part du niveau le plus haut et descend. Confondre les deux noie le lecteur dans le détail avant qu'il ait le contexte.

Structure, du plus haut au plus bas :

1. **Principe et cadre** — deux phrases sur le cadre ISO 25010 retenu et sur la lecture par niveaux.
2. **Niveau le plus haut** — le processus vu comme une seule opération, avec ses données d'entrée et de sortie externes. Trois à cinq nœuds.
3. **Arbre de composition** — la décomposition complète en un seul diagramme, sans détail. C'est la carte.
4. **Niveaux intermédiaires, en ordre décroissant** — un ou deux diagrammes par niveau, la prose en complément pour ce qui nuirait à la lisibilité du diagramme.
5. **Niveau le plus bas** — les business objects qui n'invoquent que des feuilles externes. Table condensée si la logique est triviale, diagramme dédié si elle porte du conditionnel intéressant.
6. **Synthèse** — une table à toutes les colonnes : business object, feuilles propres, sous-objets invoqués, profondeur récursive, couche métier.

**Le gabarit ISO 25010 par section de niveau** — six blocs, dans cet ordre :

| Bloc | Ce qu'il porte |
|---|---|
| Opérations de **traitement** | ce qui transforme |
| Opérations de **contrôle** | ce qui branche et orchestre |
| Données de traitement **initiales** | présentes en entrée dès le démarrage |
| Données de traitement **ad-hoc** | chargées en cours d'exécution — signaler les boucles qui font N appels |
| Données de **contrôle** | paramétrage, drapeaux, statuts, seuils : ce qui pilote la décision |
| Sorties **normales** et **anormales** | le pendant en sortie du couple nominal/erreur |

La distinction initiale/ad-hoc est le signal le plus rentable pour un lecteur qui cherche une optimisation ; la distinction traitement/contrôle change ce qu'on documente d'une opération.

---

## La SFG — sept blocs par cas d'usage

Le cas d'usage est **l'unité d'évolution** : ce qui se demande, s'arbitre et se livre d'un bloc.

Sections de tête : note d'audience · ce que le domaine résout, sans le système · invariants du domaine.

Puis, **par cas d'usage, sept blocs, sans exception** :

| Bloc | Ce qu'il contient | Piège |
|---|---|---|
| **Situation** | ce que le lecteur reconnaît : qui commande, qui est livré, qui paye | décrire le système au lieu de la situation |
| **Acteurs et rôles métier** | des personnes et des entités, pas des composants | glisser un nom d'application |
| **Déclencheur et cadence** | ce qui lance, à quelle fréquence, **avec le fuseau horaire** | « chaque nuit » — inutilisable |
| **Règles applicables** | table à trois colonnes : énoncé, intention, ce que l'utilisateur voit | factoriser vers un autre cas d'usage |
| **Ce que l'utilisateur voit** | le résultat en succès **et** en échec | oublier l'échec, qui est le cas le plus consulté |
| **Ce qui n'est pas couvert** | la frontière du cas d'usage | **le bloc qu'on oublie** |
| **Traçabilité** | règle → section SFD ; c'est ici que vivent les identifiants | le laisser incomplet « en attendant » |

> **« Ce qui n'est pas couvert » conditionne tout le reste.** Un cas d'usage dont la frontière n'est pas écrite ne peut être l'unité d'évolution de rien : on ne sait pas si une demande tombe dedans ou à côté.

Sections de queue : index inverse règle → cas d'usage (généré, jamais édité) · constats · historique, où les **corrections factuelles** sont consignées avec ce qui était écrit et pourquoi c'était faux.

**Le risque propre du troisième document.** Une contradiction laissée dans la SFD devient ici une **promesse fausse faite à l'utilisateur**, et le lecteur de la SFG n'a aucun moyen de la détecter — il n'a ni le code, ni le graphe, ni la STD. C'est asymétrique : une erreur de STD se corrige devant un développeur qui la repère ; une erreur de SFG se découvre en production. D'où le contrôle bloquant du cycle 3.

---

## Les trois artefacts qui font la différence

Ce sont eux qui distinguent DMAD d'un générateur de documentation.

### Les questions au métier
Par capacité, la liste des points que le code ne peut pas trancher, formulés **comme des questions à un humain**, pas comme des lacunes :

```markdown
### Facturation — à confirmer

1. **Factures à montant nul.** Le code ne les transmet pas au SI comptable
   (statut `SKIPPED`). Est-ce une règle métier voulue, ou un contournement
   technique d'un incident de 2019 devenu permanent ?
   → *impact si on se trompe : élevé (conformité)* · `BR-FACT-014` · `OQ-012`

2. **Arrondi à 4 décimales** sur les lignes de commande, alors que
   l'affichage en montre 2. Volonté métier ou héritage ?
   → *impact : moyen* · `BR-FACT-021` · `OQ-013`
```

C'est **l'ordre du jour de l'atelier métier** — souvent le livrable le plus immédiatement rentable de tout DMAD : il transforme trois heures de réunion floue en trois heures de décisions.

### `couverture.md` — l'honnêteté mesurée
```markdown
## Couverture de l'analyse

| Indicateur | Valeur |
|---|---|
| Fichiers atteints | 412 / 1 847 (22 %) |
| Fonctions cartographiées | 3 108 / 14 200 (22 %) |
| Points d'entrée couverts | 34 / 51 (67 %) |
| Hotspots couverts | 18 / 20 (90 %) ✅ |
| Tables documentées | 61 / 88 (69 %) |
| Contrats sortants résolus | 41 / 47 — barreau 1 : 33 · barreau 2 : 6 · barreau 3 : 2 · non résolus : 6 |

**Corpus produit :** STD ✅ (12 points d'entrée) · SFD ✅ (4 processus) · SFG ⏸️ (budget)

**Non couvert :** modules `legacy-import`, `reporting-v1`, `admin-tools`
(hors périmètre — cf. `scope.yaml`).

**Répartition des affirmations :** V 34 % · C 41 % · I 21 % · H 4 %
```

22 % de couverture avec 90 % des hotspots, **c'est un excellent résultat** — mais seulement si c'est dit. La ligne des contrats sortants est nouvelle en v0.4 : elle dit non seulement combien ont été résolus, mais **avec quelle qualité de source**.

### Les seams — la sortie actionnable
La documentation n'est pas la finalité : **pouvoir modifier le système** l'est. Pour chaque point de découpe identifié : ce qu'il isole, ce qui le traverse aujourd'hui, le coût estimé, et les tests de caractérisation qui sécuriseraient l'opération.

C'est le pont entre DMAD et ce qui suit — refonte progressive, strangler fig, ou simple évolution.

---

## En-tête obligatoire

Chaque document du corpus porte le même bandeau, complété de sa position dans la cascade :

```markdown
> **Documentation générée par DMAD** · run `2026-09-07T14:22Z` · commit `a1b2c3d`
> **Document :** STD — point d'entrée `GEN_REFACTURATION` (batch)
> **Dérive de :** le graphe et 87 affirmations · **Alimente :** `sfd/refacturation.md`
> **Périmètre :** feature-scan « facturation » — 22 % du code atteint
> **Confiance globale : C** (min. des chapitres) · 12 questions ouvertes
>
> ⚠️ Cette documentation est **reconstruite depuis le code**. Chaque affirmation
> porte son niveau de preuve : **V** vérifié · **C** corroboré · **I** inféré ·
> **H** hypothèse à valider. Ne prenez pas une affirmation `I` ou `H` pour
> une décision métier établie.
```

Ce bandeau n'est pas une clause de style. C'est ce qui empêche la doc de devenir, dans six mois, une source de vérité qu'on cite sans la questionner — et les lignes « dérive de » et « alimente » sont ce qui rend la cascade lisible depuis n'importe quel étage.
