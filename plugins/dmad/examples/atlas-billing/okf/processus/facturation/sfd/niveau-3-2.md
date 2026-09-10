---
type: "Business Object View"
title: "N1 — Facture à émettre"
description: "La constitution d'une facture, ses deux gardes, et le statut de litige lu à la demande dans une boucle."
tags: ["atlas", "facturation", "SFD"]
generated:
  by: "dmad-writer-sfd/0.4.0"
  at: "2026-09-08T17:00:00Z"
status: "stable"
# — extensions du profil DMAD : voir docs/14-okf.md
module: "billing"
audience: "hybride MOA/MOE"
confidence: "medium"
last_code_sync: "a1b2c3d"
renders: []
---

Ancré dans [`STD-facturation.md`](../../../documents/doc-std-fact-001.md) § 5 et § 9.

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

# Liens

- section de : [DOC-SFD-FACT-001](../../../documents/doc-sfd-fact-001.md)
