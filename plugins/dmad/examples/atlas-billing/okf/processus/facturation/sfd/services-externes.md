---
type: "Service Catalog"
title: "Services externes sollicités"
description: "Les deux services externes du processus : le service comptable en sortie, le service de tarification en cours de calcul."
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

| Service | Sollicité par | Cardinalité | Contrat |
|---|---|---|---|
| Service comptable | N1 — Facture à émettre | une fois par facture transmise | résolu |
| Service de tarification | N0 — Ligne valorisée | **une fois par ligne**, jusqu'à quarante par facture | **non résolu** |

Le second n'a pas de contrat établi : le jour où il tombe, personne ne saura qui appeler.

# Liens

- section de : [DOC-SFD-FACT-001](../../../documents/doc-sfd-fact-001.md)
