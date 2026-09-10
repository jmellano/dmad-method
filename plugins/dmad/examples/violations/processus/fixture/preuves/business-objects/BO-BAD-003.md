---
type: BusinessObject
title: Campagne de facturation
id: BO-BAD-003
functional_name: Campagne de facturation
capability: facturation
recursive_depth: 0
business_layer: orchestration
sub_objects:
- BO-BAD-001
confidence: I
confidence_reason: Lecture du code par le modèle, source unique, non challengée.
evidence:
- kind: code
  ref: src/billing/BillingRun.java#L44-L120
  tool: jcallgraph.definition
produced_by: carver
---


[^ev-1]: src/billing/BillingRun.java#L44-L120
