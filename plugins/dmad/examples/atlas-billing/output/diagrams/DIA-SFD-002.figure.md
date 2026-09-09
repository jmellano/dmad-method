> **Question :** comment le processus se décompose-t-il, et jusqu'où ?
> **Confiance : I — inféré** · regroupements proposés par l'analyse, validés au gate de découpage

<!-- diagram: DIA-SFD-002 · N=9 E=8 McCabe=1 -->
```mermaid
flowchart TD
  N2["N2 — Campagne de facturation"]
  N1["N1 — Facture à émettre"]
  N0["N0 — Ligne valorisée"]
  CR[("compte-rendu de campagne")]
  INV[("factures")]
  ACC[["service comptable"]]
  LIT[("statuts de litige")]
  LIG[("lignes de facture")]
  TAR[["service de tarification"]]
  N2 --> N1
  N1 --> N0
  N2 -.-> CR
  N1 -.-> INV
  N1 -.-> ACC
  N1 -.-> LIT
  N0 -.-> LIG
  N0 -.-> TAR
```
