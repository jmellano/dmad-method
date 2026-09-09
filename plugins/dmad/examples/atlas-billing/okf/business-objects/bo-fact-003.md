---
type: BusinessObject
title: Ligne valorisée
description: Ligne valorisée
dmad_id: BO-FACT-003
tags:
- facturation
sources:
- id: ev-1
  resource: src/billing/AmountCalculator.java#L88-L140
  author: process:jcallgraph.definition
  kind: code
generated:
  by: dmad-carver/0.4.0
  at: '2026-09-08T17:00:00Z'
confidence: I
confidence_reason: 'Objet atomique : n''invoque que des feuilles externes. Le calcul
  lui-même est prouvé par test de caractérisation, mais son rattachement à cet objet
  reste une proposition du modèle.

  '
freshness:
  verified_at_commit: a1b2c3d
  status: fresh
recursive_depth: 0
business_layer: calcul
---



[^ev-1]: src/billing/AmountCalculator.java#L88-L140

# Liens

- appelle le contrat : [CTR-FACT-002](../contracts/ctr-fact-002.md)
- relève de : [facturation](../capabilities/facturation.md)
