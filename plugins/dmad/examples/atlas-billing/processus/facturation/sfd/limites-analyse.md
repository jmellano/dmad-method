---
type: "Analysis Boundary"
title: "Ce qui n'a pas été analysé"
description: "Les frontières atteintes et non franchies par l'analyse de ce processus."
tags: ["atlas", "facturation", "SFD"]
generated:
  by: "dmad-writer-sfd/0.4.0"
  at: "2026-09-08T17:00:00Z"
status: "stable"
# — extensions du profil DMAD : voir docs/14-okf.md
module: "billing"
audience: "hybride MOA/MOE"
confidence: "high"
last_code_sync: "a1b2c3d"
renders: []
capability: facturation
---

- Le traitement en aval du service comptable, hors périmètre.
- Le module de relance, rattaché à la capacité *Recouvrement*.
- Deux points d'appel dynamiques du socle technique, non résolus — ils masquent potentiellement des traitements supplémentaires (`OQ-017`).

# Liens

- relève de : [facturation](../../../socle/capacites/facturation.md)
