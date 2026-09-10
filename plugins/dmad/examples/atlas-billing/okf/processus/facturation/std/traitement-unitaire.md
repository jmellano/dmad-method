---
type: "Technical Section"
title: "Traitement unitaire"
description: "Par facture : valorisation des lignes, puis garde sur le montant nul, puis transmission. La garde est en src/billing/InvoiceDispatcher.java:212. Elle"
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

Par facture : valorisation des lignes, puis garde sur le montant nul, puis transmission.

La garde est en `src/billing/InvoiceDispatcher.java:212`. Elle n'est active que si `billing.skipZeroAmount` vaut `true` — **ce qui est le cas en production et en recette, mais pas dans la configuration par défaut du dépôt**.

Chaque facture est traitée dans sa propre transaction : l'échec de l'une n'annule pas le lot.

# Liens

- section de : [DOC-STD-FACT-001](../../../documents/doc-std-fact-001.md)
- publie : [BR-FACT-014](../../../claims/br-fact-014.md)
