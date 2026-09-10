# Task 31 — Identifier les business objects

**Agent :** `carver` · **Cycle :** 2 · **Sortie :** `preuves/business-objects/`

## Principe

Un **business object** est un nœud d'orchestration qui conjugue plusieurs feuilles externes ou plusieurs sous-objets. C'est l'ossature de la vue récursive de la SFD : les BO sont les nœuds, leurs feuilles sont les bords.

L'identification se fait **des feuilles vers la racine** — c'est comme ça qu'on découvre un processus qu'on ne connaît pas.

## Étape 0 — reconnaître les patrons, avant tout le reste

Ce n'est pas de la culture générale. Un Template Method, une Strategy ou une Chain of Responsibility déterminent **où sont les vrais nœuds d'orchestration** : les manquer fait prendre une méthode de dispatch pour un business object, ou l'inverse.

Grille de reconnaissance : `${CLAUDE_PLUGIN_ROOT}/skills/patterns-gof-cqrs/SKILL.md`.

Le patron reconnu est enregistré sur le nœud. Il n'apparaîtra **pas** dans la SFD — le nom d'un patron est un détail d'implémentation — mais il conditionne le découpage et le choix du diagramme.

## Procédure

1. **Marquer les feuilles.** Chaque bout de branche porte sa famille technique (base de données, événement, contrat sortant, fichier, notification) **et** son rôle fonctionnel : traitement ou contrôle.
2. **Critère mécanique de première passe.** Est candidat tout nœud qui invoque au moins deux feuilles, ou au moins un sous-candidat.
3. **Filtrer par pertinence métier.** Un nœud qui n'orchestre que de la plomberie technique — journalisation, conversion, ouverture de transaction — n'est pas un business object. Le filtre est un jugement : il s'écrit et il s'assume.
4. **Nommer par le sens fonctionnel.** `traiterLigne` n'est pas un nom de business object. Le nom dit ce que l'objet **est** pour le métier, pas quelle méthode l'a produit. Un nom qu'un analyste ne reconnaîtrait pas signale un filtre trop laxiste à l'étape précédente.
5. **Assigner les deux étiquettes** : la **profondeur récursive** dans l'arbre, et la **couche métier**.
6. **Remonter la chaîne des appelants**, par itération : la plupart des outils ne rendent qu'un niveau. Un BO dont on n'a pas cherché les appelants est un BO dont on ignore s'il est une racine.

## Ajuster la tension longueur / profondeur

Le nombre de niveaux n'est pas un choix, c'est la **sortie** de la contrainte de lisibilité (`run.yaml`, défaut N ≤ 12, E ≤ 15, McCabe ≤ 10).

- Un niveau dont le diagramme dépasse les seuils : **décomposer** certaines étapes en sous-niveau. On convertit de la longueur en profondeur.
- Un empilement de sous-niveaux triviaux : **fusionner**. L'inverse.

Les deux leviers ne se substituent pas l'un à l'autre : ils s'ajustent en tension, et l'arbitrage se refait à chaque niveau.

## Une variation n'est pas un niveau

Trois codes de traitement qui suivent le même enchaînement ne font pas trois business objects : ils font **une propriété** du business object qu'ils gouvernent. Le test : si deux candidats ont le même arbre de feuilles et ne diffèrent que par une valeur, c'est un seul objet et un paramètre.

## Sortie

```yaml
id: BO-<capacite>-<nnn>
functional_name: "Arrivée à refacturer"
recursive_depth: 2
business_layer: "préparation"
patterns: [TemplateMethod]
own_leaves:
  - {kind: database, ref: "TBL-arrivees", role: traitement}
  - {kind: contract, ref: "CTR-fef-014", role: traitement}
sub_objects: [BO-REFAC-007, BO-REFAC-008]
confidence: I
```
