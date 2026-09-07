# DMAD — Livrables

## Arborescence de sortie

```
dmad-output/
├── 00-index.md                    # portail, périmètre, couverture, mode d'emploi des badges
│
├── fonctionnel/                   # public : métiers, PO, MOA, nouveaux arrivants
│   ├── 00-vision.md               # à quoi sert le système, pour qui
│   ├── 10-glossaire.md            # vocabulaire métier ↔ vocabulaire du code
│   ├── 20-acteurs.md              # qui utilise quoi, déclencheurs externes
│   ├── 30-capacites/
│   │   └── <capacite>/
│   │       ├── 00-resume.md       # 1 page, badge de confiance
│   │       ├── 10-cas-usage/      # UC-xxx.md, un par cas d'usage
│   │       ├── 20-regles.md       # règles de gestion, chacune avec sa preuve
│   │       ├── 30-parcours.md     # diagrammes activité / séquence métier
│   │       ├── 40-donnees.md      # ERD + dictionnaire, en langage métier
│   │       └── 99-a-confirmer.md  # ⚠️ les questions pour le métier
│   └── 90-zones-d-ombre.md        # ce que DMAD n'a pas su expliquer
│
├── technique/                     # public : développeurs, archis, ops
│   ├── 00-architecture.md         # C4 contexte/conteneurs/composants
│   ├── 10-entrypoints.md          # routes, jobs, consumers, CLI, batchs
│   ├── 20-modules/                # une fiche par module
│   ├── 30-donnees/                # schéma, migrations, ERD complet
│   ├── 40-integrations/           # API sortantes, services, files, contrats
│   ├── 50-transverse/             # auth, erreurs, config, transactions, logs
│   ├── 60-dette-et-risques.md     # hotspots, bus factor, code mort suspecté
│   └── 70-seams.md                # points de découpe sûrs pour faire évoluer
│
├── preuves/
│   ├── claims/                    # une claim = un fichier YAML
│   ├── index.json
│   ├── open-questions.md          # registre consolidé, priorisé
│   ├── challenges.md              # journal des réfutations du Challenger
│   └── couverture.md              # ⚠️ quelle part du code a été atteinte
│
└── tests/characterization/        # les tests forgés qui prouvent les règles
```

## Les deux documents

Ce sont **deux rendus du même graphe**, pas deux rédactions.

| | Fonctionnel | Technique |
|---|---|---|
| Lecteur | métier, PO, MOA | dev, archi, ops |
| Question | « que fait le système et pourquoi ? » | « comment, et où je touche ? » |
| Vocabulaire | métier exclusivement | technique, noms réels du code |
| Renvois | vers les cas d'usage | vers `fichier:lignes` |
| Diagrammes | contexte, activité, séquence métier, ERD simplifié | C4, composants, call graphs, ERD complet, hotspots |
| Interdits | noms de classes, jargon | approximation métier non sourcée |

Chaque page fonctionnelle porte un lien « vue technique » et réciproquement : c'est le même nœud du graphe vu de deux côtés.

## Les trois artefacts qui font la différence

Ce sont eux qui distinguent DMAD d'un générateur de documentation.

### `99-a-confirmer.md` — les questions au métier
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

Ce fichier est **l'ordre du jour de l'atelier métier**. C'est souvent le livrable le plus immédiatement rentable de tout DMAD : il transforme trois heures de réunion floue en trois heures de décisions.

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

**Non couvert :** modules `legacy-import`, `reporting-v1`, `admin-tools`
(hors périmètre — cf. `scope.yaml`).

**Répartition des affirmations :** V 34 % · C 41 % · I 21 % · H 4 %
```

22 % de couverture avec 90 % des hotspots, **c'est un excellent résultat** — mais seulement si c'est dit. Cette page est ce qui empêche un lecteur de prendre une doc partielle pour une doc complète.

### `70-seams.md` — la sortie actionnable
La documentation n'est pas la finalité : **pouvoir modifier le système** l'est. Cette page liste les points de découpe identifiés, avec pour chacun : ce qu'il isole, ce qui le traverse aujourd'hui, le coût estimé, et les tests de caractérisation qui sécuriseraient l'opération.

C'est le pont entre DMAD et ce qui suit — refonte progressive, strangler fig, ou simple évolution.

## En-tête obligatoire

Chaque document généré porte le même bandeau :

```markdown
> **Documentation générée par DMAD** · run `2026-09-07T14:22Z` · commit `a1b2c3d`
> **Périmètre :** feature-scan « facturation » — 22 % du code atteint
> **Confiance globale : C** (min. des chapitres) · 12 questions ouvertes
>
> ⚠️ Cette documentation est **reconstruite depuis le code**. Chaque affirmation
> porte son niveau de preuve : **V** vérifié · **C** corroboré · **I** inféré ·
> **H** hypothèse à valider. Ne prenez pas une affirmation `I` ou `H` pour
> une décision métier établie.
```

Ce bandeau n'est pas une clause de style. C'est ce qui empêche la doc de devenir, dans six mois, une source de vérité qu'on cite sans la questionner.
