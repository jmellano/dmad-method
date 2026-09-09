# Task 43 — Classer les opérations et les données (ISO 25010)

**Agent :** `elucidator` · **Cycle :** 2 · **Sortie :** enrichissement des claims et des business objects

## Principe

La partie fonctionnelle d'une spécification couvre exactement **deux sujets**, et rien d'autre : les **opérations** — en nominal et en erreur — et les **sources et puits de données** qu'elles utilisent.

Tout le reste — choix techniques, patrons d'implémentation, noms de classes, threads, transactions — est **hors périmètre de la SFD**. C'est le premier filtre à appliquer sur ce qu'on documente, et il élimine plus de matière qu'on ne l'imagine.

## Les trois classifications

### Opérations : traitement ou contrôle

| | Ce que c'est | Ce qu'on en documente |
|---|---|---|
| **Traitement** | l'opération **transforme** : mapping, calcul, agrégation | la transformation, sa précision, ses règles |
| **Contrôle** | l'opération **branche et orchestre** : conditions, dispatch, boucles, gardes | la condition, ses valeurs, ce vers quoi elle aiguille |

Ce n'est pas cosmétique : ça change ce qu'on écrit d'une opération. Une méthode de mapping est du traitement pur ; une méthode qui aiguille selon une source d'arrivée est du contrôle qui délègue à des traitements. Documenter la seconde comme la première fait disparaître la logique métier du document.

### Données consommées : traitement ou contrôle, initiales ou ad-hoc

| | Ce que c'est |
|---|---|
| **Traitement — initiales** | présentes en entrée dès le démarrage |
| **Traitement — ad-hoc** | chargées à la demande pendant l'exécution |
| **Contrôle** | paramétrage, drapeaux, statuts, seuils. N'apparaissent pas en sortie, mais **conditionnent sa forme** |

**La distinction initiale/ad-hoc est le signal le plus rentable de tout le cycle 2.** Une donnée ad-hoc chargée dans une boucle est un appel par itération — exactement ce que cherche un lecteur venu pour un problème de temps de réponse. Signaler explicitement les boucles concernées, avec leur cardinalité si elle est connue.

### Données produites : normales ou anormales

Le pendant en sortie du couple nominal/erreur des opérations. **Tout `throw`, tout retour anticipé et tout message destiné à un utilisateur produit une sortie anormale**, donc une claim : les chemins d'erreur *sont* des règles métier.

## Séparer le site de levée et l'effet observable

Une erreur se lève quelque part et produit un effet ailleurs, et **les deux ne sont pas le même fait**. Un lot qui échoue en bloc puis se rejoue unité par unité produit un effet unitaire observé, alors que le site de levée est le lot.

Documenter les deux séparément. Les confondre produit des affirmations contradictoires entre sections — et une contradiction en SFD devient une promesse fausse en SFG.

## Le gabarit de sortie, par section de niveau

Six blocs, dans cet ordre, pour chaque niveau de la vue récursive :

1. Opérations de **traitement**
2. Opérations de **contrôle**
3. Données de traitement **initiales**
4. Données de traitement **ad-hoc**
5. Données de **contrôle**
6. Sorties **normales** et **anormales**

Un bloc vide se remplit avec le constat d'absence, jamais supprimé.
