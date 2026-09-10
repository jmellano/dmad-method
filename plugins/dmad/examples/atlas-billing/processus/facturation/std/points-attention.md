---
type: "Technical Section"
title: "Points d'attention pour le développeur"
description: "1. AmountCalculator arrondit au demi-supérieur sur quatre décimales ; l'affichage et l'export en montrent deux. Écarts possibles sur les cumuls. → BR-"
tags: ["atlas", "facturation", "STD"]
generated:
  by: "dmad-writer-std/0.4.0"
  at: "2026-09-08T17:00:00Z"
status: "stable"
# — extensions du profil DMAD : voir docs/14-okf.md
module: "billing"
audience: "MOE"
confidence: "high"
last_code_sync: "a1b2c3d"
renders: []
capability: facturation
---

1. `AmountCalculator` arrondit au demi-supérieur sur quatre décimales ; l'affichage et l'export en montrent deux. Écarts possibles sur les cumuls. → `BR-FACT-021` **[V]**
2. `billing.skipZeroAmount` diffère entre le dépôt (`false`) et la production (`true`). **Un développeur qui lance le projet en local n'observe pas le comportement de production.** → `BR-FACT-014` **[I]**
3. `ReinvoiceCommand.java:47` appelle le port comptable **directement**, sans passer par le dispatcher : les gardes sont contournées. → `OQ-019`
4. `reporting` lit la table `invoices` sans passer par le module. Couplage non prévu par l'architecture. → `OQ-021`
5. Le statut de litige et le barème sont lus **à la demande dans des boucles** : environ 1 400 appels par campagne pour le premier, jusqu'à 40 par facture pour le second. Aucun lot.
6. Deux dispatchs dynamiques non résolus via `ServiceLocator.get(String)`. → `OQ-017`
7. Le contrat de tarification n'est pas résolu. → `OQ-024`

# Liens

- relève de : [facturation](../../../socle/capacites/facturation.md)
