# Partie E — Le premier run réel

> Spec détaillée. Vue d'ensemble : [reste à faire](2026-09-09-dmad-reste-a-faire.md)
> **Dépend de** : A1 et A2. **Bloque** : D2, et l'arbitrage de la question ouverte de B.

## Ce que c'est

**Pas un chantier de développement. Le seul jalon qui compte.**

La roadmap v0.3 le disait déjà : tant qu'aucun run réel n'a eu lieu, DMAD est une spécification cohérente — ce qui ne prouve rien. La v0.4 vient d'ajouter trois cents lignes de méthode à une spécification qui n'a jamais rencontré de code.

Ce n'est pas un reproche à la conception : c'est la raison pour laquelle la partie E vient avant B et C dans l'ordre recommandé.

## Le périmètre

Le plus petit run utile est déjà cadré dans `examples/std-seule/` :

- **un point d'entrée**, connu à l'avance — `known_entrypoints` renseigné, donc pas d'étape de localisation
- **`corpus: [std]`** — un seul document
- **un développeur**, pas d'expert métier

Il exerce néanmoins **tout le cycle 1**, y compris la résolution des contrats, qui est la partie la plus neuve et la moins éprouvée de la v0.4.

**Ce qu'il n'exerce pas** : le gate 3, l'élucidation, les tests de caractérisation, l'intention, et deux des trois revues. C'est assumé. Un run complet sur un premier essai mesurerait trop de choses à la fois pour qu'on sache laquelle a mal marché.

## Prérequis

| | Pourquoi |
|---|---|
| **A1** | sans les contrôles mécaniques, on mesure ce qu'un relecteur a bien voulu voir |
| **A2** | A1 en dépend |
| le projet résout ses dépendances | sinon le run est plafonné à `I` et ne mesure pas le cas nominal |
| `profile.contract_convention` renseigné | sinon la résolution des contrats retombe au barreau 3 et le lot le plus neuf n'est pas testé |

Le reste de la partie A n'est pas requis. En particulier **A5 manque**, donc les diagrammes seront écrits à la main et les seuils de D15 ne seront pas mesurés — à noter comme une limite du run, pas à corriger avant.

---

## Le protocole de mesure

C'est la partie qui demande de la discipline, parce qu'elle se fait **pendant** le run et ne se rattrape pas après.

### Mesure 1 — le coût réel par étape

Relever, pour chacune des cinq étapes du cycle 1 : **tokens consommés, durée, modèle**.

L'hypothèse du design est que le modèle fort n'est payé qu'au découpage et à la réfutation. Elle n'a jamais été vérifiée, et le cycle 1 en teste déjà une moitié : le Challenger y tourne en modèle fort sur un registre mécanique, ce qui est peut-être un gaspillage.

**Ce que le chiffre décide** : si le cycle 1 coûte plus qu'une journée d'un développeur qui lirait le code, la méthode ne se vend pas — et c'est mieux de le savoir sur un point d'entrée que sur douze.

### Mesure 2 — le taux de findings du Challenger

Nombre de claims dégradées, reformulées, scindées ou invalidées, sur le total.

| Résultat | Interprétation |
|---|---|
| **< 5 %** | Challenger complaisant. Tout l'édifice de confiance s'effondre : c'est lui qui protège le reste |
| **15 à 30 %** | le repère attendu |
| **> 50 %** | la cartographie ou la résolution produit trop de bruit, pas assez de faits |

**Attention à un biais propre au cycle 1** : le registre y est mécanique, donc le taux devrait y être *plus bas* qu'au cycle 2. Un 8 % au cycle 1 n'a pas la même signification qu'un 8 % au cycle 2. Le noter comme tel plutôt que de conclure trop vite.

### Mesure 3 — la justesse par échantillonnage

**Tirer cinq claims au hasard, ouvrir le code aux lignes citées, vérifier que la phrase correspond.**

Dix minutes. C'est le seul contrôle qui détecte l'erreur dominante des modèles — citer du vrai code en lui faisant dire autre chose — parce qu'une relecture intégrale d'un texte crédible et bien sourcé ne déclenche aucune alarme.

**Plus d'une erreur sur cinq condamne le run.** Ce n'est pas une figure de style : il faut alors repasser le Challenger avec des consignes durcies, et re-mesurer.

### Mesure 4 — spécifique à la v0.4 : la répartition par barreau

Combien de contrats résolus, et à quel barreau. C'est la mesure de la **qualité des sources**, et elle dit si la partie la plus neuve de la méthode fonctionne.

Un run à 47/47 dont trente sont au barreau 3 est un moins bon run qu'un 41/47 majoritairement au barreau 1 — et sans cette ligne, les deux se ressemblent.

**Ce que le chiffre décide** : si le barreau 1 est rarement atteint, c'est soit que `contract_convention` est mal renseigné, soit que la chaîne de résolution est plus variable que la conception ne le suppose. Dans les deux cas, la partie C doit en tenir compte avant d'être écrite.

### Mesure 5 — les invariants ont-ils mordu

Combien de fois les contrôles d'A1 ont refusé quelque chose, et lesquels.

**Un contrôle qui ne se déclenche jamais est suspect** : soit il est mal écrit, soit il vérifie quelque chose qui n'arrive pas. Les deux méritent d'être su. Le contrôle D16 — aucun bloc de code — est celui qui devrait se déclencher le plus, parce qu'il contredit l'habitude de tous les modèles.

---

## Le livrable du run

Pas seulement une STD. **Une entrée de journal.**

C'est la pratique du corpus `skills-doc`, et c'est de loin la partie la plus utile de ses skills : chacun se termine par un journal daté des applications réelles, *y compris les règles qui se sont révélées fausses et ont été remplacées*.

Trois questions à documenter :

1. **Qu'est-ce que le run a révélé** que la conception ne prévoyait pas ?
2. **Quelle règle de la méthode a dû être corrigée** — et la faute était-elle dans la règle, dans le prompt de l'agent, ou dans le contrôle ?
3. **Quel constat est réutilisable** ailleurs — et si oui, le remonter dans la méthode plutôt que le laisser dans le journal.

> Une règle qui ne fait que **répéter un avertissement** au lieu de supprimer l'ambiguïté doit être remplacée par une décision. Un avertissement se réoublie ; une décision se vérifie.

**Où l'écrire** : `docs/journal/AAAA-MM-JJ-<projet>-<point-entree>.md`, versionné avec la méthode. Une leçon qui vit hors du dépôt diverge de ce qu'elle est censée corriger.

---

## Les critères de succès

**Le critère principal, et il est humain** : le commanditaire répond « oui » à *« est-ce que ça vous débloque ? »*.

Les critères mesurés :

- moins d'une erreur sur cinq à l'échantillonnage
- le Challenger a trouvé au moins une chose qu'une relecture n'aurait pas trouvée
- au moins un contrat résolu au barreau 1
- la revue de cycle 1 a demandé des corrections — **une revue qui n'en demande aucune est un signal d'alarme**, pas un succès : elle signifie que le relecteur n'a pas cherché, ou que la STD est trop vague pour être contestée

## Ce qui doit sortir du run, en plus des chiffres

Une réponse à la question laissée ouverte en partie B : **comment les gens lisent-ils réellement ces documents ?** C'est le facteur qui décidera s'il faut éclater le corpus en concepts OKF liés — vérifiable mécaniquement, moins confortable à lire — ou le laisser en documents.

Cette question ne se tranche pas en réunion. Elle se tranche en regardant quelqu'un ouvrir une STD pour modifier un batch.

---

## Après

Un second run, sur le même point d'entrée, en `corpus: [std, sfd]`. Il exerce le gate 3, l'élucidation, les tests de caractérisation et une deuxième revue — et il mesure ce que la cascade coûte réellement, ce qu'aucun run à un seul document ne peut dire.

Puis, et seulement alors, le corpus complet.
