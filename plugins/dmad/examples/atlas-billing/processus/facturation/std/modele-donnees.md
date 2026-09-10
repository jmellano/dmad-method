---
type: "Technical Section"
title: "Modèle de données"
description: "Tables lues — orders, order_lines, customers (colonne dispute_status), pricing_scales Tables écrites — invoices, invoice_lines, billing_runs Colonnes"
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
renders: ["BR-FACT-021"]
capability: facturation
---

**Tables lues** — `orders`, `order_lines`, `customers` (colonne `dispute_status`), `pricing_scales`
**Tables écrites** — `invoices`, `invoice_lines`, `billing_runs`

Colonnes déterminantes : `invoice_lines.amount` en `DECIMAL(12,4)`, `invoices.status` en énumération à quatre valeurs, `customers.dispute_status`.

# Liens

- relève de : [facturation](../../../socle/capacites/facturation.md)
