---
type: "Contract Catalog"
title: "Appels externes"
description: "Code Barreau Artefact:version Interface Méthode Contexte Comportement d'échec --------------------- ACC_INV_TRANSMIT_001 1 acme/atlas/accounting-api:"
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
renders: ["CTR-FACT-001", "CTR-FACT-002"]
---

| Code | Barreau | Artefact:version | Interface | Méthode | Contexte | Comportement d'échec |
|---|---|---|---|---|---|---|
| `ACC_INV_TRANSMIT_001` | 1 | `acme/atlas/accounting-api:4.7.2` | `AccountingGateway` | `POST /invoices/transmit` | une fois par facture transmise | statut `FAILED`, reprise à la campagne suivante, **cinq tentatives au maximum** |
| `SIM_XXX_XXX_XXX` | 4 | — | `PricingClient` | tarification | **une fois par ligne de commande** | non documenté — voir `OQ-024` |

Le second contrat n'est pas résolu : aucun artefact de sources dans le dépôt local, aucune Javadoc, aucun commentaire près de l'appel. Le placeholder est volontaire — un identifiant plausible se serait propagé sans qu'on puisse le contester.

**La version de l'artefact du premier compte** : le contrat décrit ce que ce module consomme en `4.7.2`, pas ce que le service comptable publie aujourd'hui.

# Liens

- section de : [DOC-STD-FACT-001](../../../documents/doc-std-fact-001.md)
- publie : [CTR-FACT-001](../../../contracts/ctr-fact-001.md)
- publie : [CTR-FACT-002](../../../contracts/ctr-fact-002.md)
