> **Question :** quels composants ce batch mobilise-t-il, et lesquels franchissent une frontière ?
> **Confiance : C — corroboré** · deux dispatchs non résolus, cf. § 14

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
