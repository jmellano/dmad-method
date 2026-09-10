---
type: "Technical Section"
title: "Séquence technique"
description: "Question : dans quel ordre les composants s'appellent-ils pour une facture, et où sort-on du périmètre ? Confiance : C — corroboré · une frontière no"
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

> **Question :** dans quel ordre les composants s'appellent-ils pour une facture, et où sort-on du périmètre ?
> **Confiance : C — corroboré** · une frontière non franchie en aval

<!-- diagram: DIA-STD-002 · N=5 E=7 McCabe=4 -->
```mermaid
sequenceDiagram
  autonumber
  participant R as BillingRun
  participant D as InvoiceDispatcher
  participant C as AmountCalculator
  participant P as PricingClient
  participant A as AccountingGateway
  R->>D: dispatch(invoice)
  loop par ligne
    D->>C: compute(line)
    C->>P: barème du client
    P-->>C: barème
  end
  alt montant nul et paramètre actif
    D->>D: markSkipped()
  else 
    D->>A: transmettreFacture()
    A-->>D: accusé
  end
  Note over A: comportement aval non analysé
```

# Liens

- section de : [DOC-STD-FACT-001](../../../documents/doc-std-fact-001.md)
