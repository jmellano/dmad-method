---
type: "Test Case Set"
title: "Cas de test"
description: "Étape Description ------ Pré-condition une commande livrée, non facturée, client sans litige, une ligne à 3 unités Action exécuter BillingRun.execute"
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

| Étape | Description |
|---|---|
| Pré-condition | une commande livrée, non facturée, client sans litige, une ligne à 3 unités |
| Action | exécuter `BillingRun.execute()` |
| Attendu | une facture en statut `TRANSMITTED`, montant de ligne à quatre décimales arrondi au demi-supérieur |
| Pré-condition | une facture à montant nul, `billing.skipZeroAmount` à `true` |
| Action | `InvoiceDispatcher.dispatch()` |
| Attendu | statut `SKIPPED`, aucun appel au port comptable |

Six tests de caractérisation forgés, dont `AmountCalculatorCharacterizationTest` qui promeut `BR-FACT-021` en `V`.

# Liens

- relève de : [facturation](../../../socle/capacites/facturation.md)
