---
name: code-intelligence-java
description: Ce que l'analyse de code prouve, et ce qu'elle ne prouve pas. Le plafond de confiance se dérive de la question posée, pas de l'outil employé. À lire avant la première traversée, pas après le premier doute.
---

# Ce que l'analyse de code prouve

Ce skill n'explique pas comment naviguer dans du code. Il explique **ce qu'une réponse vaut**, question par question — parce que c'est de là que la confiance est dérivée, et non du nom de l'outil qui a répondu.

L'implémentation de référence de la capability `code-intelligence` est **`jcallgraph`**, un analyseur tree-sitter. Pas de serveur à lancer, pas d'index à faire chauffer, pas de classpath à résoudre.

## Le plafond se dérive de la question

| Ce qu'on demande | Plafond | Pourquoi |
|---|---|---|
| symboles déclarés dans un fichier | `V` | lecture syntaxique exhaustive |
| hiérarchie de types, implémentations d'une interface | `V` | c'est écrit dans les sources |
| appel statique, appel sur type déclaré | `V` | la cible est écrite |
| appelants d'une méthode | `V` si tout le périmètre est indexé, `C` sinon | l'exhaustivité dépend de ce qui a été lu |
| appel virtuel ou d'interface | `C` — **candidats, jamais un choix** | le type dynamique n'est pas connu statiquement |
| injection de dépendances, fabrique par chaîne | `C`, avec `unresolved_dispatch` | le câblage est ailleurs, souvent hors du code |
| réflexion, chargement par nom | `I`, et une question ouverte | rien dans les sources ne le dit |
| comportement modifié par aspect ou proxy | **hors de portée** | à signaler, jamais à supposer |

**Le plafond s'applique par arête du graphe, pas au run entier.** Un dispatch non résolu ne dégrade pas ce que l'outil a par ailleurs prouvé exhaustivement — et réciproquement, une hiérarchie de types bien lue n'autorise aucune affirmation d'exhaustivité sur un appel dynamique voisin.

## Les questions qu'aucun analyseur ne traite

Ce sont celles qu'on perd le plus de temps à poser au mauvais outil.

**« Où sont les occurrences de ce code métier ? »** Un identifiant dans un commentaire ou une javadoc n'est pas un symbole. C'est une recherche textuelle, et elle se croise ensuite avec l'analyse pour confirmer que la classe trouvée est bien invoquée depuis le chemin étudié.

**« Quel contrat porte cet appel sortant ? »** L'annotation vit dans l'artefact d'une dépendance, hors du périmètre analysé. C'est de la lecture d'archive — voir la task 13 et son échelle à quatre barreaux.

**« Ce comportement est-il modifié quelque part ? »** Un aspect, un intercepteur, un proxy modifient une méthode sans la mentionner. Aucune traversée d'appels ne les trouve. C'est un angle du Challenger, pas une requête d'outil.

## Ce qu'on ne fait jamais sur un dispatch non résolu

**On ne choisit pas le candidat le plus probable.** On pose un nœud dédié :

```yaml
unresolved_dispatch:
  at: "src/…/InvoiceService.java#L88"
  expression: "gateway.send(Invoice)"
  declared_type: "com.acme.AccountingGateway"
  candidates: ["HttpAccountingGateway", "LegacyFileGateway", "NoopGateway"]
  resolution: unknown
  open_question: OQ-0xx
```

L'outil peut **réduire** la liste — une interface à implémentation unique dans le périmètre indexé est résolue — mais il ne tranche jamais par vraisemblance. Choisir silencieusement, c'est laisser bâtir trois pages sur une supposition.

## Repli, et ce qu'il coûte

| Repli | Plafond global | Ce qu'on perd |
|---|---|---|
| recherche textuelle | `I` | l'exhaustivité. **Aucune affirmation d'exhaustivité n'est autorisée**, quelle que soit la qualité de la lecture |

Le plafond n'est pas une punition : c'est ce qui rend la dégradation **visible dans le document produit** au lieu d'être silencieuse. Il se déclare au gate 0 et s'affiche dans le bandeau des trois documents.

## Rendre le projet analysable

Un analyseur syntaxique n'a pas besoin que le projet compile — c'est sa principale vertu sur un legacy, où la compilation est souvent le premier obstacle et parfois un obstacle définitif.

Deux choses restent utiles quand elles sont disponibles, et **aucune n'est bloquante** :

- **Les dépendances résolues**, pour la traversée vers l'intérieur des artefacts et la résolution des contrats sortants au barreau 1. Sans elles, la résolution retombe au barreau du commentaire manuscrit, celui qui survit aux refactorings et ment alors sans le dire.
- **La version du langage**, pour que l'analyse syntaxique ne bute pas sur une construction récente.

Ce qui manque se déclare dans `scope.yaml` et s'affiche dans le bandeau. Un projet qui ne compile pas n'est plus un run dégradé : c'est un run normal dont certains contrats ne seront pas résolus, et qui le dit.
