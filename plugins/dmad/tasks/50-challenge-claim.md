# Task 50 — Réfuter une claim

**Agent :** `challenger` · **Phase :** 5 · **Modèle :** opus · **Sortie :** `challenges/`

## La consigne exacte

Elle n'est pas « vérifie cette affirmation ». Elle est :

> **« Trouve le chemin de code qui rend cette affirmation fausse. »**

La formulation change matériellement le résultat. Un LLM à qui on demande de vérifier confirme ; à qui on demande de falsifier, cherche.

## Les 9 angles

### 1 — Preuve trahie *(le plus rentable)*
Ouvrir les lignes citées. **Disent-elles ce que la claim leur fait dire ?**

L'erreur dominante d'un LLM n'est pas d'inventer du code inexistant — c'est de **citer du vrai code en lui faisant dire autre chose**. La citation exacte donne une impression de rigueur qui désarme la vérification humaine. C'est pourquoi cet angle passe en premier, pas en dernier.

### 2 — Garde oubliée
Remonter les appelants. Un `if` en amont court-circuite-t-il ce chemin ?

### 3 — Feature flag / configuration
Le comportement dépend-il d'un flag, d'une variable d'environnement, d'un profil de build, d'un paramètre en base ? Comparer **la valeur par défaut du dépôt et la valeur observée en production** — c'est là que se cachent les docs vraies en local et fausses en prod.

### 4 — Polymorphisme
`find_implementations`, `type_hierarchy`. Une sous-classe redéfinit-elle ce comportement ? Un décorateur, un proxy, un intercepteur AOP s'interpose-t-il ?

### 5 — Chemin d'erreur
Que se passe-t-il en cas d'échec ? La règle tient-elle encore ? Un `catch` qui avale l'exception invalide beaucoup d'affirmations.

### 6 — Transaction
Un rollback peut-il annuler l'effet décrit ? L'effet de bord (mail, appel externe) survit-il au rollback alors que l'écriture en base est annulée ?

### 7 — Exhaustivité
« Toujours », « jamais », « aucun autre » : prouvé sur **tous** les appelants, ou sur celui qu'on a lu ? Vérifier `find_references` **et** le plafond de la capability : au `grep`, aucune affirmation d'exhaustivité n'est recevable.

### 8 — Code mort
Ce chemin est-il atteignable ? Croiser graphe d'appels et couverture. Une règle dans du code mort n'est pas une règle en vigueur.

### 9 — Concurrence
Deux exécutions simultanées invalident-elles l'invariant ? Lecture-modification-écriture sans verrou, contrainte d'unicité absente.

## Discipline anti-complaisance

1. **Contexte séparé.** Le Challenger ne voit pas le raisonnement de l'Elucidator, uniquement la claim finale et le code. Il ne peut pas hériter de ses angles morts.
2. **Quota de doute.** Aucun finding sur une capacité entière ⇒ produire obligatoirement les **3 claims les plus fragiles** avec l'argument de fragilité. Zéro finding sur 40 claims signale un Challenger complaisant, pas une documentation parfaite.
3. **Angles écartés justifiés.** Un angle non examiné doit l'être pour une raison écrite (`angles_skipped`), pas par omission.

## Résultats

| Résultat | Effet |
|---|---|
| `confirmed` | maintenue — **pas de promotion**, seul le Test Forger promeut |
| `demoted` | niveau abaissé, raison journalisée |
| `contradicted` | retirée de la doc, convertie en question ouverte |
| `split` | la claim en cachait deux (typiquement les deux branches d'un flag) |
| `reformulate` | vraie mais mal formulée, renvoyée à l'Elucidator |

## Repère de calibration
Sur un legacy réel, **15 à 30 % de claims dégradées, reformulées ou scindées** est le taux attendu. Nettement moins : le Challenger est complaisant. Nettement plus : l'Elucidator travaille avec un outillage dégradé ou un périmètre mal cadré.
