---
type: BusinessObject
title: Campagne de facturation
description: Campagne de facturation
dmad_id: BO-FACT-001
tags:
- facturation
sources:
- id: ev-1
  resource: src/billing/BillingRun.java#L44-L120
  author: process:lsp.find_definition
  kind: code
generated:
  by: dmad-carver/0.4.0
  at: '2026-09-08T17:00:00Z'
confidence: I
confidence_reason: 'Nœud d''orchestration identifié par traversée depuis le point
  d''entrée nocturne. Regroupement proposé par le modèle, non challengé sur ce point.

  '
freshness:
  verified_at_commit: a1b2c3d
  status: fresh
recursive_depth: 2
business_layer: orchestration
---



[^ev-1]: src/billing/BillingRun.java#L44-L120

# Liens

- compose : [BO-FACT-002](bo-fact-002.md)
- relève de : [facturation](../capabilities/facturation.md)
