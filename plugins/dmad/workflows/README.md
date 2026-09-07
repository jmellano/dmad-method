# Workflows DMAD

Deux workflows, un seul pipeline d'agents. La différence tient à **par où on entre** et à **ce qu'on accepte de ne pas couvrir**.

| | `full-scan` | `feature-scan` |
|---|---|---|
| Entrée | tous les entrypoints recensés | un vocabulaire métier → localisation → confirmation humaine |
| Découpage | capacités du système | sous-capacités de la feature |
| Gates | 3 | **4** (un gate de localisation en plus) |
| Épuisement du budget | on arrête sur une capacité terminée | on réduit la profondeur de traversée |
| Avertissement obligatoire | non | oui — frontières non franchies |
| Défaut pour | < 150 kLOC, reprise de maintenance | > 150 kLOC, objectif sur un domaine nommé |

## Le gate supplémentaire du feature-scan

Le `feature-scan` ajoute un gate après la **localisation** : l'humain confirme quels points d'entrée candidats appartiennent réellement à la fonctionnalité.

C'est le meilleur rapport coût/valeur de toute la méthode. Dix minutes d'un humain qui regarde une liste de candidats évitent des heures de traversée dans la mauvaise direction — et surtout, évitent de produire une documentation cohérente sur le mauvais périmètre, ce qui est bien pire que de ne rien produire.

## Deux règles de budget

**`full-scan`** — quand le budget s'épuise, on termine la capacité en cours et on s'arrête. Une capacité documentée en entier vaut mieux que six ébauches, et la couverture le dira clairement.

**`full-scan`, phase 1** — si le recensement révèle un volume incompatible avec le budget, le Surveyor le remonte immédiatement, avant la cartographie. Découvrir le dépassement en phase 4 fait perdre l'intégralité des phases 2 et 3.

## Ordre de traitement

Dans les deux workflows, la phase 4 est ordonnée par `hotspot_rank`. On élucide d'abord ce qui bouge et fait mal. Si le run s'arrête tôt, il s'est arrêté après avoir traité le plus important — pas après avoir traité l'ordre alphabétique.
