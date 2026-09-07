# Task 62 — Rendre la documentation technique

**Agent :** `writer-technical` · **Phase :** 6

## Contrainte fondatrice
Comme son homologue fonctionnel : **pas d'accès au code**. Il rend le graphe et les claims.

## Structure (arc42 allégé)

```
00-architecture.md      C4 contexte / conteneurs / composants
10-entrypoints.md       toutes les surfaces d'entrée, avec reachability
20-modules/             une fiche par module
30-donnees/             schéma, migrations, dictionnaire
40-integrations/        API sortantes, contrats, modes de défaillance
50-transverse/          auth, erreurs, config, transactions, logs, jobs
60-dette-et-risques.md  hotspots, bus factor, code mort suspecté
70-seams.md             points de découpe, coût, tests nécessaires
```

## La fiche de module

Le format le plus consulté. Une page maximum.

```markdown
## `src/billing`   [V]
**Rôle** · **Capacité** · **Hotspot** rang 3/20 ⚠️
**Entrées** — les entrypoints
**Sorties** — services externes, tables écrites
**Dépend de** / **Dépendu par** — avec signalement des couplages inattendus
**Points d'attention** — pièges connus, renvois aux claims
**Fichiers clés** — 3 à 5 max, avec numéros de ligne
**Tests** — existants + forgés par DMAD
```

Un « dépendu par » inattendu (`reporting` qui lit `invoices` en direct) est une information architecturale de premier ordre : le signaler explicitement, avec la question ouverte associée.

## Section « limites de l'analyse » — obligatoire

C'est ce qui distingue une documentation professionnelle d'une génération automatique :

```markdown
## Limites de cette analyse
- Profondeur de traversée : 5. 17 frontières atteintes (cf. couverture).
- 2 dispatchs dynamiques non résolus (`ServiceLocator.get(String)`).
- Pas de trace runtime : les chemins décrits sont possibles, pas nécessairement empruntés.
- Modules hors périmètre : legacy-import, reporting-v1, admin-tools.
```

## Ton
Le lecteur est un développeur qui arrive lundi matin. On documente **ce qui est**, y compris ce qui est laid. On ne propose pas de refonte : les seams sont décrits, les décisions appartiennent à l'équipe.
