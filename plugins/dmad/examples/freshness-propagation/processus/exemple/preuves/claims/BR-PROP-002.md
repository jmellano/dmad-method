---
type: BusinessRule
title: BR-PROP-002
id: BR-PROP-002
capability: propagation
confidence: C
confidence_reason: 'Deux preuves convergentes, et aucune modification depuis la vérification.

  '
evidence:
- kind: schema
  ref: example.amount DECIMAL(12,4)
  tool: schema.columns
produced_by: elucidator
freshness:
  verified_at_commit: aaa1111
  status: fresh
---

Une règle dont le code n'a pas bougé. Elle reste fraîche, et sa fraîcheur ne sauve pas les documents qui publient aussi la précédente.
