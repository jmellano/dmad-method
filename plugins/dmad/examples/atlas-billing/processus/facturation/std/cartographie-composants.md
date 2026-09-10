---
type: "Technical Section"
title: "Cartographie des composants"
description: "Le batch est câblé en trois couches : un déclencheur planifié, un service d'orchestration, et deux ports sortants. Question : quels composants ce batc"
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

Le batch est câblé en trois couches : un déclencheur planifié, un service d'orchestration, et deux ports sortants.

> **Question :** quels composants ce batch mobilise-t-il, et lesquels franchissent une frontière ?
> **Confiance : C — corroboré** · deux dispatchs non résolus, cf. § 7

<!-- diagram: DIA-STD-001 · N=8 E=7 McCabe=1 -->
```mermaid
flowchart LR
  SCH(("Planificateur"))
  RUN["BillingRun"]
  DISP["InvoiceDispatcher"]
  CALC["AmountCalculator"]
  ACC[["port AccountingGateway"]]
  PRI[["port PricingClient"]]
  DB[("invoices")]
  DBL[("invoice_lines")]
  SCH --> RUN
  RUN --> DISP
  DISP --> CALC
  DISP --> ACC
  CALC --> PRI
  DISP --> DB
  CALC --> DBL
```

`BillingRun` orchestre, `InvoiceDispatcher` décide et transmet, `AmountCalculator` valorise. Les deux ports sont les seules sorties du périmètre.

# Liens

- relève de : [facturation](../../../socle/capacites/facturation.md)
