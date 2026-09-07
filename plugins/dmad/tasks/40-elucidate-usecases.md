# Task 40 — Reconstituer les cas d'usage

**Agent :** `elucidator` · **Phase :** 4 · **Sortie :** claims `UseCase`

## Procédure

Pour chaque entrypoint de la capacité :

1. **Déclencheur** — qui ou quoi lance l'exécution, avec quelle fréquence, sous quelle condition
2. **Acteur** — humain, système, automate ; interne ou externe
3. **Préconditions** — ce qui doit être vrai pour que le flux nominal démarre (gardes en tête de méthode, contraintes de base)
4. **Flux nominal** — étapes successives, chacune avec ses règles et ses preuves
5. **Flux alternatifs** — chaque branche significative : cas limites, erreurs métier, court-circuits
6. **Postconditions** — état du système après, en particulier les états possibles des entités touchées
7. **Effets de bord** — envois, écritures externes, événements publiés

## Ce qui distingue un vrai cas d'usage d'une paraphrase de code

| Paraphrase (inutile) | Cas d'usage (utile) |
|---|---|
| « la méthode `dispatch()` appelle `gateway.send()` » | « la facture est transmise au service comptable » |
| « boucle sur les lignes » | « chaque ligne de commande est valorisée puis totalisée » |
| « if status != DRAFT return » | « une facture déjà émise ne peut pas être réémise » |

**Le test :** un lecteur métier doit pouvoir lire le flux sans jamais rencontrer un nom de classe.

## Les chemins d'erreur sont des règles métier

L'erreur la plus courante est de traiter les branches d'erreur comme du détail technique. Un `throw new InsufficientFundsException()` **est** une règle de gestion : c'est un refus, avec une condition et un message adressé à un humain.

Règle opérationnelle : **tout `throw`, tout retour anticipé et tout message d'erreur destiné à un utilisateur produit une claim.**

## Le piège de la complétude
Un cas d'usage avec 40 branches n'est pas exhaustif : il est illisible, et c'est souvent le signe que l'entrypoint en cache plusieurs. Au-delà de ~8 flux alternatifs, envisager la scission.

## Sortie
Structure `use_case` complète (cf. `agents/elucidator.md`), chaque étape portant ses `rules` et ses `evidence`. Le cas d'usage n'est pas une narration : c'est une structure attaquable étape par étape par le Challenger.
