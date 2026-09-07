# Task 41 — Extraire les règles de gestion

**Agent :** `elucidator` · **Phase :** 4 · **Sortie :** claims `BusinessRule`, `Invariant`

## Où chercher, par fiabilité décroissante

| Lieu | Fiabilité | Note |
|---|---|---|
| **Contraintes de base** (`NOT NULL`, `CHECK`, `UNIQUE`, FK, défauts) | **très haute** | déclaratif, non contournable → niveau `V` gratuit |
| Gardes et retours anticipés | haute | conditions d'éligibilité, exclusions |
| Validations (formats, plages, obligations) | haute | |
| Chemins d'erreur et messages | haute | souvent la vraie règle métier |
| Calculs | haute mais piégeuse | voir ci-dessous |
| Valeurs magiques (seuils, plafonds, codes) | haute sur le *quoi*, `H` sur le *pourquoi* | |
| Ordre des opérations, transactions | moyenne | |
| Noms de tests | moyenne | intention formulée par un humain |
| Configuration, feature flags | **basse** | le comportement dépend de l'environnement |

**Commencer par la base de données.** Les contraintes déclaratives donnent des règles de niveau `V` sans effort ni risque d'hallucination. C'est le meilleur rendement de toute la méthode, et c'est presque toujours négligé.

## Les quatre pièges nommés

### Les calculs
Documenter **la précision, le mode d'arrondi et le type**, pas seulement la formule. Un `float` au lieu d'un `decimal`, un `HALF_UP` au lieu d'un `HALF_EVEN`, un `setScale(2)` au lieu de `(4)` : ce sont des règles de gestion à conséquences comptables.

### La configuration
Une règle pilotée par un flag n'est pas une règle : **c'est deux règles et un interrupteur.** Remplir `conditional_on` avec la clé, la valeur par défaut **et les valeurs observées par environnement**. Le schéma exige que la condition apparaisse dans l'énoncé.

C'est la source numéro un de documentation vraie en recette et fausse en production — et la plus difficile à détecter en relecture, parce que rien ne cloche dans la phrase.

### Le code mort
Une règle dans du code jamais appelé n'est pas une règle en vigueur. Croiser avec le graphe d'appels et la couverture **avant** d'énoncer. Si le doute persiste : l'énoncer en précisant que son atteignabilité n'est pas établie.

### La surcharge
Une règle définie dans une classe mère peut être redéfinie ailleurs. Vérifier `find_implementations` et `type_hierarchy` avant toute affirmation d'exhaustivité. (Le Challenger attaquera précisément là, angle 4.)

## Forme d'un énoncé

- **Une règle = une phrase.** Un « et » coordonnant deux conditions indépendantes cache deux règles.
- **Vocabulaire métier**, même en lisant du Java.
- **Portée explicite** : « toujours » et « jamais » exigent d'avoir vérifié tous les appelants ; sinon « sur le chemin X ».
- **Aucun verbe d'opinion.** L'incertitude s'exprime par le niveau de confiance, jamais par un adverbe.
- **Localisation ligne à ligne.** Une règle qui pointe un fichier de 800 lignes n'est pas vérifiable, donc pas publiable.

## Invariants
Un invariant est une propriété **toujours vraie**, pas une règle appliquée à un moment. Sources fiables : contraintes de base, assertions, tests portant sur des propriétés. Un invariant déduit d'une lecture de code est plafonné à `I` — et sera systématiquement attaqué sur l'angle 9 (concurrence).
