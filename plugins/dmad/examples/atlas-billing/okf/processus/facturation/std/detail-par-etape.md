---
type: "Technical Section"
title: "Détail par étape"
description: "Sélection — BillingRun.selectEligible() src/billing/BillingRun.java:52-78. Retient les commandes livrées, non facturées, dont le client n'est pas en l"
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
renders: ["BR-FACT-014"]
---

**Sélection** — `BillingRun.selectEligible()` `src/billing/BillingRun.java:52-78`. Retient les commandes livrées, non facturées, dont le client n'est pas en litige. Le statut de litige est lu **par commande**, pas en lot : voir le point d'attention 5.

**Traitement** — `InvoiceDispatcher.dispatch(Invoice)` `src/billing/InvoiceDispatcher.java:180-280`. Valorise, applique la garde, transmet, marque l'état.

**Clôture** — `BillingRun.close()` `src/billing/BillingRun.java:98-120`. Écrit le compte-rendu de campagne dans `billing_runs`.

# Liens

- section de : [DOC-STD-FACT-001](../../../documents/doc-std-fact-001.md)
- publie : [BR-FACT-014](../../../claims/br-fact-014.md)
