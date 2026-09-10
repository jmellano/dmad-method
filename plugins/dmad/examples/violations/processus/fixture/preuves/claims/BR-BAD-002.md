---
type: BusinessRule
title: BR-BAD-002
id: BR-BAD-002
confidence: V
confidence_reason: J'ai lu le code attentivement et cette règle est certaine.
evidence:
- kind: code
  ref: src/order/Order.java#L88
  tool: jcallgraph.definition
produced_by: elucidator
freshness:
  verified_at_commit: a1b2c3d
  status: fresh
---

Une commande annulée ne peut plus être facturée.[^ev-1]

[^ev-1]: src/order/Order.java#L88
