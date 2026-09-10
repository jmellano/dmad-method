---
type: "Technical Section"
title: "Architecture du flux"
description: "Trois étapes séquentielles : sélection des commandes éligibles, traitement par lot, clôture de campagne. Une seule branche conditionnelle, sur le mont"
tags: ["atlas", "facturation", "STD"]
generated:
  by: "dmad-writer-std/0.4.0"
  at: "2026-09-08T17:00:00Z"
status: "stable"
# — extensions du profil DMAD : voir docs/14-okf.md
module: "billing"
audience: "MOE"
confidence: "high"
last_code_sync: "a1b2c3d"
renders: []
---

Trois étapes séquentielles : sélection des commandes éligibles, traitement par lot, clôture de campagne. Une seule branche conditionnelle, sur le montant nul, décrite en § 5.

# Liens

- section de : [DOC-STD-FACT-001](../../../documents/doc-std-fact-001.md)
