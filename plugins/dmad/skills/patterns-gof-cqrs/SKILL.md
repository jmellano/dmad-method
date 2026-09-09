---
name: patterns-gof-cqrs
description: Reconnaître les patrons de conception dans du code existant et décider où ils ont le droit d'apparaître dans le corpus DMAD. Prérequis du cycle 2 - un patron mal reconnu fait prendre une méthode de dispatch pour un business object.
---

# Patrons de conception — reconnaître, puis taire

Ce skill n'enseigne pas les patrons : ces cours existent partout. Il traite **deux questions propres à la rétro-documentation**.

**Reconnaître** — parce qu'un Template Method, une Strategy ou une Chain of Responsibility déterminent **où sont les vrais nœuds d'orchestration**. Les manquer fait prendre une méthode de dispatch pour un business object, ou l'inverse, et le découpage de la SFD est faux à partir de là.

**Taire** — parce qu'un patron est un **choix d'implémentation**. Il a sa place en STD ; il n'en a aucune en SFD ni en SFG.

## Reconnaître — trois signaux, dans cet ordre

**Signal 1 — la structure de types.**

| Ce qu'on voit | Candidat |
|---|---|
| une abstraction + au moins deux implémentations | **Strategy** (variantes interchangeables) ou **Template Method** (squelette commun à hooks) |
| une classe qui instancie selon un paramètre | **Factory Method** ou **Abstract Factory** |
| une classe qui enveloppe une autre en implémentant la même interface | **Decorator**, **Proxy** ou **Adapter** |
| une classe qui agrège des sous-objets homogènes derrière une interface commune | **Composite** |

**Signal 2 — le corps des méthodes clés.**

| Ce qu'on voit | Candidat |
|---|---|
| une méthode qui appelle plusieurs opérations abstraites en cascade | **Template Method** |
| une cascade de conditions qui délègue à des gestionnaires différents | **Chain of Responsibility** |
| une construction étape par étape terminée par une finalisation | **Builder** |
| une itération sur des abonnés pour les notifier | **Observer** |
| une délégation immédiate à un champ du même type | **Proxy** (contrôle d'accès) ou **Decorator** (ajout de comportement) |

**Signal 3 — le nommage.** Les suffixes `Strategy`, `Handler`, `Command`, `Visitor`, `State`, `Observer`, `Factory`, `Builder` sont un **indice fort et jamais une preuve** : le nommage ment. Toujours croiser avec le signal 1 ou 2.

> **L'erreur type** : conclure « c'est une Strategy » sur la foi du nom. Une vraie Strategy a une famille de variantes **effectivement dispatchées**. Sans les implémentations et sans le site de dispatch, ce n'est qu'un nom — et le nœud n'est pas là où on le croit.

## Ce que la reconnaissance change pour le découpage

| Patron reconnu | Conséquence sur les business objects |
|---|---|
| **Template Method** | le squelette est **un** business object ; ses hooks sont ses opérations, pas des objets frères |
| **Strategy** | le point de dispatch est une opération de **contrôle** ; chaque variante est une propriété du même objet, **pas un niveau de plus** |
| **Chain of Responsibility** | chaque maillon peut être un objet, mais la chaîne elle-même en est un — et c'est elle qui porte la règle d'arrêt |
| **Composite** | la récursion structurelle **n'est pas** une récursion métier : ne pas la transcrire en niveaux d'abstraction |
| **Facade** | le nœud est un point de passage, pas un orchestrateur : candidat au filtre de pertinence |
| **CQRS** | deux arbres distincts, pas un seul — les documenter séparément |

## Taire — le patron est un détail technique

**En STD** : le nom du patron est utile et se nomme. Un développeur qui arrive lundi matin gagne du temps à lire « Template Method à cinq hooks ordonnés ».

**En SFD et en SFG** : jamais. Ce sont des vocables de conception, et une spécification fonctionnelle décrit le comportement, pas sa réalisation.

| Ce que le code fait techniquement | Ce qu'on écrit en SFD |
|---|---|
| « un Template Method à cinq hooks abstraits » | « chaque variante suit les mêmes cinq étapes : regroupement → lignes → émetteur et destinataires → avis d'expédition → assemblage » |
| « une Strategy à trois implémentations » | « selon la nature de l'arrivée, le processus applique un comportement différent : avec commande d'achat obligatoire, ou sans » |
| « une Factory qui instancie selon un nom de composant » | « le processus sélectionne la variante de traitement à partir de la nature de l'arrivée » |
| « un Observer sur le bus d'événements » | « en fin de lot, deux événements déclenchent les traitements aval » |

## L'exception qui vaut d'être connue — l'attribut technique porteur d'une garantie

Un choix d'implémentation reste hors SFD **tant qu'il est interchangeable**. Dès qu'il produit une **garantie observable par le métier**, cette garantie entre en SFD — décrite par son **effet**, jamais par son mécanisme.

Le cas d'école est la transaction propre ouverte pour enregistrer un élément en erreur. Techniquement, c'est un attribut de propagation. Fonctionnellement, c'est **ce qui garantit que le statut d'erreur survit à l'annulation du lot** — sans quoi l'élément fautif serait perdu et retraité indéfiniment sans trace. Le support constate cette garantie ; elle appartient donc à la SFD.

| Formulation | Verdict |
|---|---|
| « `@Transactional(propagation = REQUIRES_NEW)` sur `GererXImpl` » | ❌ mécanisme — STD |
| « une transaction propre, qui survit à l'annulation du lot » | ✅ garantie, mais encore technique |
| « l'élément fautif est enregistré en erreur même quand le lot entier est annulé, et reste retentable au prochain rejeu » | ✅ **la bonne** — effet observable, sans vocabulaire technique |

**Le test** : si retirer l'attribut change **ce que le métier observe**, il y a une garantie fonctionnelle à écrire. Si ça ne change que la performance ou l'élégance, c'est un détail technique.

Ce test vaut au-delà du transactionnel : idempotence, ordre de publication des événements, unicité en base relèvent de la même distinction.

## Où le patron est enregistré

Sur le nœud `BusinessObject`, champ `patterns`. Il conditionne le découpage et le choix du diagramme, il apparaît en STD, et le `Writer:SFD` a l'interdiction de l'écrire.

C'est exactement le rôle d'une information portée par le graphe et filtrée à la rédaction : disponible pour raisonner, invisible pour le lecteur qui n'en a pas besoin.
