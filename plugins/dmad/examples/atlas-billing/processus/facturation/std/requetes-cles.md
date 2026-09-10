---
type: "Technical Section"
title: "Requêtes clés"
description: "Référence Tables Colonnes Intention ------------ OrderRepository.java:88 orders, order_lines delivered_at, invoiced_at sélection des commandes livrée"
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

| Référence | Tables | Colonnes | Intention |
|---|---|---|---|
| `OrderRepository.java:88` | `orders`, `order_lines` | `delivered_at`, `invoiced_at` | sélection des commandes livrées non facturées |
| `CustomerRepository.java:41` | `customers` | `dispute_status` | exclusion des clients en litige — **appelée par commande, pas en lot** |

**Les requêtes de `ReportingRepository` sur `invoices` relèvent du module `reporting`, hors périmètre — ne pas les attribuer à ce batch.** C'est le piège d'attribution le plus probable ici : elles portent sur les mêmes tables.

# Liens

- relève de : [facturation](../../../socle/capacites/facturation.md)
