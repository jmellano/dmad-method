---
type: "Process Overview"
title: "Processus général du système d'information"
description: "Le processus vu comme une seule opération, avec ses entrées et ses sorties externes."
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

# Liens

- section de : [DOC-SFD-FACT-001](../../../documents/doc-sfd-fact-001.md)
