---
type: "Decomposition"
title: "Étapes de transformation du traitement"
description: "L'arbre de composition : la décomposition complète du processus en trois niveaux, sans détail."
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
capability: facturation
---

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

# Liens

- relève de : [facturation](../../../socle/capacites/facturation.md)
