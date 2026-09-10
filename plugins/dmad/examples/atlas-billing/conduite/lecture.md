---
type: "Analysis Commentary"
title: "Lecture du rapport de couverture"
description: "L'interprétation des chiffres : ce qu'ils autorisent à conclure, et les trois limites à connaître."
---

22 % du code, mais **100 % des points d'entrée de la facturation et 90 % des hotspots du dépôt**. Les règles de calcul des montants sont couvertes et **prouvées par des tests de caractérisation** — c'est précisément ce que demandait l'objectif du run : changer le barème sans régression comptable.

Les points d'entrée et les hotspots pèsent le plus. Un run qui couvre 22 % des fichiers mais 90 % des zones à risque est un bon run ; un run à 60 % de fichiers qui rate la moitié des points d'entrée est un mauvais run qui en impose.

Trois limites doivent être connues avant d'utiliser cette documentation.

1. **Le comportement du SI comptable en aval n'a pas été analysé** — système externe, hors périmètre. Les règles décrites s'arrêtent à la transmission.
2. **Deux dispatchs dynamiques non résolus** subsistent dans le socle. Rien n'indique qu'ils touchent la facturation, rien ne l'exclut. Les candidats sont enregistrés, aucun n'a été choisi (`OQ-017`).
3. **Un contrat sortant sur deux n'est pas résolu.** Le service de tarification est appelé jusqu'à quarante fois par facture et son contrat reste inconnu : le jour où il tombe, personne ne saura qui appeler (`OQ-024`).

**Sur le fond des artefacts publiés ici.** Ce dossier embarque un échantillon représentatif du run — trois claims sur les quarante et une examinées — parce qu'il sert de fixture de non-régression, pas d'archive. La répartition des niveaux de preuve calculée ci-dessus porte donc sur l'échantillon, pas sur le run complet, qui se répartissait en `V` 34 % · `C` 41 % · `I` 21 % · `H` 4 %.

**Répondre aux cinq questions P1 ferait passer quatorze affirmations d'hypothèse à fait établi**, dont la règle sur les factures à montant nul — la seule qui bloque aujourd'hui le changement de barème en toute sécurité.


# Liens

- voir aussi : [couverture](couverture.md)
- run : [README](../README.md)
