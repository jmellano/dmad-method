> **Question :** qu'entre-t-il et que sort-il de la facturation nocturne, vue de l'extérieur ?
> **Confiance : C — corroboré**

<!-- diagram: DIA-SFD-001 · N=7 E=6 McCabe=1 -->
```mermaid
flowchart LR
  IN["Commandes livrées non facturées"]
  BAR["Barèmes clients"]
  LIT["Statuts de litige"]
  P(("Facturation nocturne"))
  FAC["Factures transmises"]
  ARC["Factures archivées sans envoi"]
  CR["Compte-rendu de campagne"]
  IN --> P
  BAR --> P
  LIT --> P
  P --> FAC
  P --> ARC
  P --> CR
```
