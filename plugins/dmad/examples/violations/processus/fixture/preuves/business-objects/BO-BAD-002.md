---
type: BusinessObject
title: Arrivée à refacturer
id: BO-BAD-002
functional_name: Arrivée à refacturer
capability: facturation
recursive_depth: 1
business_layer: préparation
sub_objects:
- BO-FANTOME-999
confidence: I
confidence_reason: Lecture du code par le modèle, source unique, non challengée.
evidence:
- kind: code
  ref: src/billing/Arrival.java#L12-L80
  tool: jcallgraph.definition
produced_by: carver
---


[^ev-1]: src/billing/Arrival.java#L12-L80
