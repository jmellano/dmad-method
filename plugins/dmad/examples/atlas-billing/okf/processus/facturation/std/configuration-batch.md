---
type: "Technical Section"
title: "Configuration"
description: "Propriété Valeur ------ Nom du job nightly-billing Déclenchement cron 0 2 Taille de lot 200 factures Politique de rejet skip-limit 10, puis échec de"
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
---

| Propriété | Valeur |
|---|---|
| Nom du job | `nightly-billing` |
| Déclenchement | cron `0 2 * * *` |
| Taille de lot | 200 factures |
| Politique de rejet | `skip-limit` 10, puis échec de la campagne |
| Point d'entrée | `BillingRun.execute()` |
| Contrats couverts | `ACC_INV_TRANSMIT_001` · un contrat non résolu (§ 9) |
| Paramètre déterminant | `billing.skipZeroAmount` — **défaut du dépôt `false`, production `true`** |

# Liens

- section de : [DOC-STD-FACT-001](../../../documents/doc-std-fact-001.md)
