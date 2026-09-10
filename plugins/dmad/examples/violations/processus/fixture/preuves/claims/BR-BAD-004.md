---
type: BusinessRule
title: BR-BAD-004
id: BR-BAD-004
confidence: C
confidence_reason: Garde dans le code et valeur confirmée par la configuration observée.
evidence:
- kind: code
  ref: src/billing/DunningService.java#L120
  tool: jcallgraph.definition
- kind: config
  ref: config/application-prod.yml#L44
  tool: grep
conditional_on:
  kind: env_config
  key: dunning.delayDays
  default: '30'
  observed:
    prod: '15'
produced_by: elucidator
freshness:
  verified_at_commit: a1b2c3d
  status: fresh
---

Les relances sont envoyées 15 jours après l'échéance.[^ev-1][^ev-2]

[^ev-1]: src/billing/DunningService.java#L120
[^ev-2]: config/application-prod.yml#L44
