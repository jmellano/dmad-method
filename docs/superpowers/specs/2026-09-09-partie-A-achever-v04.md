# Partie A — Achever la v0.4

> Spec détaillée. Vue d'ensemble : [reste à faire](2026-09-09-dmad-reste-a-faire.md) · Conception : [v0.4](2026-09-09-dmad-v04-corpus-std-sfd-sfg-design.md)
> **Dépend de** : rien. **Bloque** : la partie E (par A1 et A2), et la partie B (par A2).

## Le problème

La v0.4 a **écrit** ses invariants. Elle ne les **contraint** pas.

`tools/validate.py` s'annonce comme « le point d'application mécanique des principes du manifeste », et son en-tête dit : *une claim sans preuve, une exclusion sans justification ou une question sans destinataire sont refusées ici, pas signalées en relecture*. Il tient cette promesse pour la v0.3 — six violations connues, six refus, vérifiés par `selftest.sh`.

Pour la v0.4, il ne vérifie rien. D16, D17 et D18 vivent dans des prompts d'agents et des cases à cocher de checklists. Un agent distrait, un modèle moins doué, une reprise de session : rien ne les rattrape.

Le manifeste dit lui-même qu'un principe non contraint par un schéma est un vœu pieux. C'est aujourd'hui le seul endroit du projet où l'écart entre le discours et le code est visible de l'extérieur.

---

## A1 — Contraindre les invariants v0.4

### Ce qu'il faut vérifier

| # | Invariant | Décision | Porte sur |
|---|---|---|---|
| 1 | Aucune clôture de bloc de langage (`java`, `sql`, `xml`, `yaml`, `properties`…) dans un document du corpus | D16 | Markdown |
| 2 | Tout `ExternalContract` porte `artifact_version` non vide | D18 | YAML |
| 3 | `resolution_rung` entre 1 et 4, et la confiance dérivée du barreau | D18 | YAML |
| 4 | Toute section de niveau d'une SFD référence au moins un ancrage de sa STD | D17 | Markdown + graphe |
| 5 | Toute règle de SFG référence au moins une règle de sa SFD | D17 | Markdown + graphe |
| 6 | Tout diagramme porte sa question, et ses métriques respectent `scope.diagram_thresholds` | D15, R1 | plan de diagrammes |
| 7 | Sept blocs par cas d'usage de SFG, dont « ce qui n'est pas couvert », non vide | — | Markdown |
| 8 | L'index inverse de la SFG compte autant d'entrées que le corps a de règles | — | Markdown |
| 9 | Une contradiction non résolue dans la SFD interdit la production de la SFG | — | état du Curator |
| 10 | `derives_from` d'un document résout vers un document **figé** | D19 | YAML + fichiers |

### La difficulté réelle

**Quatre de ces contrôles portent sur du Markdown**, pas sur des artefacts structurés. `validate.py` ne sait aujourd'hui faire qu'une chose : router un fichier YAML vers un schéma JSON et appliquer des règles croisées sur des claims chargées en mémoire.

Deux options.

**Étendre `validate.py` d'un mode corpus.** Un seul outil, une seule commande, un seul point d'entrée pour les gates. Mais on alourdit un outil qui marche, et on mélange deux natures de vérification.

**Écrire `tools/check-corpus.py`, séparé.** L'outil de schémas reste ce qu'il est ; le nouveau ne connaît que des documents. `selftest.sh` appelle les deux. C'est l'option recommandée : les deux outils échouent pour des raisons différentes, et un message d'erreur qui mélange « ta claim viole le schéma » et « ta SFD contient un bloc SQL » n'aide personne.

### Forme des messages d'erreur

**Chaque message nomme la décision qu'il applique.**

```
dmad-output/std/GEN_REFAC.md:412 — D16 : bloc de code ```java dans un document du corpus.
    La STD porte des références (fichier:lignes, signatures), jamais d'extrait.

dmad-output/sfd/refacturation.md — D17 : la section « N2 — Arrivée à refacturer »
    ne référence aucun ancrage de std/GEN_REFAC.md.
    Une section sans ancrage est une information apparue de nulle part.
```

Ce n'est pas de la cosmétique. Un message qui ne dit pas quelle règle il fait respecter se fait contourner, puis supprimer, au premier agacement — et la règle disparaît avec lui.

### Fixtures

Chaque garde-fou reçoit sa violation dans `examples/violations/`, et `selftest.sh` vérifie qu'elle est refusée. C'est la règle déjà appliquée aux six violations v0.3 : **un garde-fou non testé n'est pas un garde-fou.**

Nouveau sous-dossier nécessaire — les violations actuelles sont des claims YAML, celles-ci sont des documents :

```
examples/violations/
├── claims/                  (existant, 6 fixtures)
└── corpus/
    ├── std-avec-bloc-de-code.md
    ├── std-avec-bloc-sql.md
    ├── sfd-section-sans-ancrage.md
    ├── sfg-regle-sans-tracabilite.md
    ├── sfg-cas-usage-a-six-blocs.md
    ├── sfg-index-inverse-incoherent.md
    ├── contrat-sans-version.yaml
    └── diagramme-sans-question.yaml
```

### Fin de lot

`./tools/selftest.sh` refuse les dix violations, chaque message nomme sa décision, et le run de référence continue de passer.

---

## A2 — Les schémas des types v0.4

`claim.schema.json` refuse aujourd'hui les nouveaux types : son `enum` ne les contient pas, et son motif d'identifiant (`^(BR|UC|INV|CAP|ST|ACT|TERM|RISK)-…`) non plus.

### Fichiers à créer

**`schemas/external-contract.schema.json`**

```yaml
id: CTR-<module>-<nnn>            # motif à ajouter
call_site: "<fichier>#L<n>"       # requis
code: "<code de contrat>"         # requis sauf au barreau 4
resolution_rung: 1                # requis, 1..4
artifact: "<groupe/artefact>"     # requis aux barreaux 1 et 2
artifact_version: "<version>"     # REQUIS aux barreaux 1 et 2 — refus sinon
http_verb / route / operation     # optionnels, remplis au barreau 1
confidence: V                     # dérivée : 1→V, 2→C, 3→I, 4→aucune claim
```

La dérivation confiance ↔ barreau est une **règle croisée**, pas une contrainte de schéma : un barreau 3 déclaré en `V` doit être refusé avec un message qui explique pourquoi.

**`schemas/business-object.schema.json`**

`functional_name` (requis), `recursive_depth`, `business_layer`, `own_leaves[]` (chacune typée : `database` / `event` / `contract` / `file` / `notification`, et de rôle `traitement` ou `contrôle`), `sub_objects[]`, `patterns[]`.

Une règle croisée à ajouter : **un `functional_name` qui ressemble à un identifiant de code** — camelCase commençant par un verbe, présence de parenthèses — est refusé. C'est la règle « nommer par le sens, pas par la méthode », et c'est celle qu'un agent pressé enfreint en premier.

**`schemas/document.schema.json`**

`kind` (`STD` / `SFD` / `SFG`), `unit`, `unit_ref`, `derives_from[]`, `feeds[]`, `frozen_at`, `frozen_by`.

**Extensions** : `claim.schema.json` (enum de types, motifs d'identifiants), et les `ROUTES` de `validate.py`.

### L'objection à traiter d'entrée

La partie B va changer la sérialisation de tout cela. Écrire ces schémas maintenant, c'est accepter de les réécrire.

Le calcul reste favorable : ils sont petits, A1 en dépend, et l'alternative est de **ne rien contraindre pendant toute la durée de B** — c'est-à-dire pendant le premier run réel, précisément le moment où l'on a besoin de savoir si les garde-fous mordent.

### Fin de lot

Un contrat sans version, un contrat au barreau 3 déclaré en `V`, un business object nommé `traiterLigne` et une SFD sans `derives_from` sont refusés, chacun avec son message.

---

## A3 — Porter le run de référence au corpus

`examples/atlas-billing/output/` rend encore `fonctionnel/` et `technique/`. C'est le **seul endroit où les trois gabarits seront éprouvés avant un vrai projet**, et c'est la vitrine de la méthode : quiconque évalue DMAD ouvre ce dossier.

À produire, pour la capacité Facturation :

- `output/std/invoice-dispatcher.md` — les dix-sept sections, dont au moins une remplie par un constat d'absence, et une section 9 avec **au moins un contrat résolu au barreau 1** et un non résolu au barreau 4. Le run de référence doit montrer les deux, sinon il ne montre pas l'échelle.
- `output/sfd/facturation.md` — la vue récursive, avec le gabarit six blocs sur au moins deux niveaux, et une donnée ad-hoc chargée en boucle signalée.
- `output/sfg/facturation.md` — deux cas d'usage à sept blocs, un index inverse cohérent, et une intention marquée `H`.
- les tables de correspondance croisées entre les trois.

Le run de référence porte déjà deux trouvailles du Challenger — un feature flag actif en production mais inactif par défaut dans le dépôt, et un « n'est jamais transmise » faux sur le troisième appelant. **Elles doivent survivre au portage** : ce sont elles qui prouvent que la méthode trouve ce qu'une relecture ne trouve pas.

### Fin de lot

`validate.py` et `check-corpus.py` passent sur `examples/atlas-billing`.

---

## A4 — Les documents non relus contre la v0.4

| Document | Ce qui manque |
|---|---|
| `docs/05-knowledge-graph.md` | les types de nœuds v0.4 (`ExternalContract`, `BusinessObject`, `DataFlow`, `Diagram`, `Document`) dans la table des origines et confiances natives ; les arêtes `derives_from` et `anchors` |
| `docs/10-antipatterns.md` | trois entrées nouvelles et le tableau de correspondance |
| `QUICKSTART-java.md` | les trois cycles au lieu des phases, le choix du corpus au gate 0, la convention de contrat, le renvoi à `examples/std-seule` |
| `settings.example.json` | les règles `deny` visent deux rédacteurs qui n'existent plus. Il en faut trois — et la SFG doit être coupée du **graphe** autant que du code, ce que la v0.3 n'avait pas à exprimer |
| `examples/violations/README.md` | les fixtures ajoutées en A1 |
| `docs/04-capabilities.md` | `diagram-engine` reste décrit comme un contrat sans implémentation ; cohérent avec A5, à relire après |

### Les trois anti-patterns

Chacun est une défaillance identifiée pendant la conception, pas une hypothèse.

**A14 — Le contrat périmé par un bump de version.** Un code de contrat relevé dans un artefact Maven reste plausible indéfiniment après que la dépendance a changé de version. Le document continue d'affirmer un contrat que le module ne consomme plus. *Parade :* `artifact_version` obligatoire, et la fraîcheur qui compare la version documentée à la version résolue.

**A15 — La cascade percée.** Un rédacteur qui descend d'un étage pour combler un trou : lire le code depuis la SFD, la STD depuis la SFG. Le document redevient une lecture indépendante — et deux lectures indépendantes divergent. *Parade :* `disallowedTools`, règles `deny`, et la `gap_request` qui remonte d'un cycle.

**A16 — Le faux barreau.** Présenter un code lu dans un commentaire manuscrit comme s'il venait du contrat. **Un code faux ressemble exactement à un code vrai** ; seul le barreau écrit fait la différence. *Parade :* `resolution_rung` obligatoire et la confiance dérivée.

---

## A5 — Le `diagram-engine`

Dette héritée de la v0.3, que la v0.4 aggrave en multipliant les diagrammes.

La règle R3 dit : *« Généré depuis le graphe, jamais rédigé. Les agents décrivent un sous-graphe et une intention ; le moteur rend. Un diagramme ne peut donc pas contredire la doc — les deux sortent de la même source. »*

Aujourd'hui le contrat existe et **le rendu n'existe pas**. Les rédacteurs écrivent du Mermaid à la main. Trois conséquences, dans l'ordre de gravité :

1. **Un diagramme peut contredire le texte qui l'entoure**, ce que R3 était censé rendre impossible par construction.
2. **Le badge de confiance n'est pas calculé** depuis le sous-graphe : il est recopié, donc invérifiable.
3. **Les seuils de D15 ne sont pas mesurés.** Personne ne compte les nœuds et les arêtes d'un diagramme écrit à la main — ni l'auteur, ni le relecteur.

Le troisième point rend D15 inopérant tant qu'A5 n'est pas fait : on a paramétré un seuil que rien ne mesure.

**Périmètre minimal** : un rendu Mermaid pour les quatre diagrammes cardinaux, prenant un sous-graphe et une question, retournant la source **et ses métriques** (N, E, participants). Le reste du catalogue peut attendre.

### Fin de lot

Un rédacteur qui écrit une syntaxe de diagramme est refusé ; les diagrammes du run de référence sont rendus depuis le graphe et portent leurs métriques.

---

## A6 — Fraîcheur et couverture calculées

### `tools/freshness.py`

Spécifié depuis la v0.3, jamais écrit. Pour chaque claim, comparer `freshness.verified_at_commit` à l'état actuel et classer : `fresh` · `shifted` (les références ont bougé, le sens tient) · `stale` (à re-soumettre) · `broken` (à re-cartographier).

**Ce que la v0.4 ajoute, et qui est le vrai travail : la propagation vers le haut.**

```
claim périmée  →  section de STD qui la cite  →  section de SFD qui l'ancre  →  règle de SFG
```

Sans elle, une SFG peut rester marquée fraîche alors que son socle a bougé. C'est le pire cas possible : **le document le plus cru est le plus périmé**, et son lecteur est celui qui a le moins de moyens de s'en apercevoir.

À ajouter aussi : la comparaison de `artifact_version` documentée à la version résolue par le build. C'est la parade d'A14, et c'est mécanique.

### Couverture

Décrite dans les templates, calculée à la main. À automatiser, avec la ligne nouvelle :

```
Contrats sortants résolus | 41 / 47 — barreau 1 : 33 · 2 : 6 · 3 : 2 · non résolus : 6
```

Elle mesure la **qualité des sources**, pas seulement le nombre de contrats trouvés. Un run à 47/47 dont trente sont au barreau 3 est un moins bon run qu'un 41/47 majoritairement au barreau 1 — et sans cette ligne, les deux se ressemblent.

---

## Ordre et fin de partie

```
A1 ─┬─► A3 ─► A4
A2 ─┘
A5 (indépendant, mais D15 reste inopérant sans lui)
A6 (indépendant, ou remplacé par B6 si B est priorisé)
```

**A1 et A2 sont le prérequis de la partie E.** Le reste peut attendre le retour du terrain, et sera meilleur pour l'avoir attendu.

La partie A est finie quand `./tools/selftest.sh` refuse tout ce que la v0.4 interdit, et que le run de référence le prouve.
