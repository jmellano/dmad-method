> **Question :** avec qui la constitution d'une facture dialogue-t-elle, et dans quel ordre ?
> **Confiance : C — corroboré** · une frontière non franchie en aval

<!-- diagram: DIA-SFD-003 · N=4 E=7 McCabe=3 -->
```mermaid
sequenceDiagram
  autonumber
  participant C as Campagne
  participant F as Facture à émettre
  participant L as Statuts de litige
  participant SC as Service comptable
  C->>F: constituer la facture d'une commande
  F->>L: le client est-il en litige ?
  L-->>F: statut
  F->>F: totaliser les lignes valorisées
  alt montant nul et paramètre actif
    F->>F: archiver sans transmettre
  else 
    F->>SC: transmettre
    SC-->>F: accusé de réception
  end
  Note over SC: traitement aval hors périmètre
```
