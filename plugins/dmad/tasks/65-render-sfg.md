# Task 65 — Rendre la SFG

**Agent :** `writer-sfg` · **Cycle :** 3 · **Sortie :** `dmad-output/sfg/<domaine>.md`

## Ce qui est lu

**La SFD figée. Rien d'autre** (D17). Ni le code, ni le graphe, ni la STD.

## Prérequis bloquant

Le `Curator` a vérifié que la SFD ne se contredit pas. **Une contradiction laissée en SFD devient ici une promesse fausse faite à l'utilisateur**, et le lecteur n'a aucun moyen de la détecter.

Si une contradiction apparaît malgré tout en cours de rédaction : **arrêter et remonter**. Ne pas choisir la version la plus plausible, ne pas écrire une formulation qui concilie. Les deux sections peuvent être vraies à deux moments différents du traitement — et c'est cette distinction qui est l'information.

## L'unité : le cas d'usage

Ce qui se demande, s'arbitre et se livre d'un bloc. **Le découpage se fait par ce qui évolue ensemble**, jamais par les valeurs que prend un paramètre.

Test à rejouer sur chaque candidat *et* sur chaque variation : si deux candidats partagent leurs règles et ne diffèrent que par une valeur, c'est **un** cas d'usage et une propriété.

## Sections de tête

1. **Note d'audience** — à qui, ce qu'on n'y trouvera pas et où c'est écrit, comment le document est organisé **et pourquoi**. Seul endroit où la doctrine est expliquée ; ailleurs elle est appliquée.
2. **Ce que le domaine résout** — le problème métier en une page, **sans le système**. Un lecteur qui s'arrête ici doit avoir compris à quoi sert la chose.
3. **Invariants du domaine** — même table à trois colonnes que les règles.

## Les sept blocs, par cas d'usage, sans exception

| Bloc | Piège |
|---|---|
| **Situation** | décrire le système au lieu de la situation |
| **Acteurs et rôles métier** | glisser un nom d'application |
| **Déclencheur et cadence** | « chaque nuit » sans fuseau horaire — inutilisable |
| **Règles applicables** | énoncé · intention · ce que l'utilisateur voit. Ne pas factoriser vers un autre cas d'usage |
| **Ce que l'utilisateur voit** | oublier l'échec, qui est le cas le plus consulté |
| **Ce qui n'est pas couvert** | **le bloc qu'on oublie** |
| **Traçabilité** | règle → section SFD. Le laisser incomplet « en attendant » |

> **« Ce qui n'est pas couvert » conditionne tout le reste.** Un cas d'usage dont la frontière n'est pas écrite ne peut être l'unité d'évolution de rien.

## Les règles partagées s'arbitrent, elles ne se subissent pas

Une règle présente dans plusieurs cas d'usage a **une décision écrite** : soit elle remonte en invariant du domaine, soit elle est contextualisée dans chacun. La contextualisation révèle souvent ce que la factorisation masquait — deux formulations d'une même règle qui n'ont pas le même effet observable.

## Sections de queue

- **Index inverse** règle → cas d'usage. **Généré, jamais édité.** Compter les règles du corps et les entrées de l'index : un écart est un défaut.
- **Constats** — distinguer ce qui relève de la méthode et ce qui attend un arbitrage. Chaque arbitrage énonce ses options.
- **Historique** — y consigner les **corrections factuelles**, avec ce qui était écrit et pourquoi c'était faux. C'est la seule trace qu'un relecteur aura de la fiabilité du document.

## Interdits d'audience

Aucun nom de composant, d'application, de table, de code technique, de vocabulaire d'exploitation — hors du bloc traçabilité, seul endroit où les identifiants ont droit de cité.

Grep des interdits en fin de passe : constituer la liste une fois par domaine, la rejouer à chaque fois.
