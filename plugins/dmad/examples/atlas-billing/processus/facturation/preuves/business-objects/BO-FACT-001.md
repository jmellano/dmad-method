---
type: BusinessObject
title: Campagne de facturation
id: BO-FACT-001
functional_name: Campagne de facturation
capability: facturation
recursive_depth: 2
business_layer: orchestration
patterns:
- TemplateMethod
own_leaves:
- kind: database
  ref: billing_runs
  role: traitement
  availability: initiale
sub_objects:
- BO-FACT-002
confidence: I
confidence_reason: 'Nœud d''orchestration identifié par traversée depuis le point
  d''entrée nocturne. Regroupement proposé par le modèle, non challengé sur ce point.

  '
evidence:
- kind: code
  ref: src/billing/BillingRun.java#L44-L120
  tool: jcallgraph.definition
produced_by: carver
freshness:
  verified_at_commit: a1b2c3d
  status: fresh
---


[^ev-1]: src/billing/BillingRun.java#L44-L120

# Liens

- compose : [BO-FACT-002](BO-FACT-002.md)
- relève de : [facturation](../../../../socle/capacites/facturation.md)
