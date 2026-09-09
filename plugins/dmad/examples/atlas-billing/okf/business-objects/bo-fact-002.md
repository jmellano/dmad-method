---
type: BusinessObject
title: Facture à émettre
description: Facture à émettre
dmad_id: BO-FACT-002
tags:
- facturation
sources:
- id: ev-1
  resource: src/billing/InvoiceDispatcher.java#L180-L280
  author: process:jcallgraph.definition
  kind: code
generated:
  by: dmad-carver/0.4.0
  at: '2026-09-08T17:00:00Z'
confidence: I
confidence_reason: 'Nœud d''orchestration confirmé par la traversée, mais le statut
  de litige est lu à la demande dans une boucle : le coût réel n''a pas été mesuré.

  '
freshness:
  verified_at_commit: a1b2c3d
  status: fresh
recursive_depth: 1
business_layer: préparation
---



[^ev-1]: src/billing/InvoiceDispatcher.java#L180-L280

# Liens

- compose : [BO-FACT-003](bo-fact-003.md)
- appelle le contrat : [CTR-FACT-001](../contracts/ctr-fact-001.md)
- relève de : [facturation](../capabilities/facturation.md)
