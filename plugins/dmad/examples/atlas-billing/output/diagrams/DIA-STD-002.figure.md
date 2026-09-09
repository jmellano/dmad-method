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
