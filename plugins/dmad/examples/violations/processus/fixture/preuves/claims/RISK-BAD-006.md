---
type: Risk
title: RISK-BAD-006
id: RISK-BAD-006
confidence: V
confidence_reason: L'analyse du dépôt montre clairement que ce module est le plus
  critique.
evidence:
- kind: code
  ref: src/payment/
  note: beaucoup de modifications récentes
produced_by: surveyor
freshness:
  verified_at_commit: a1b2c3d
  status: fresh
---

Le module de paiement est le point le plus risqué du dépôt.[^ev-1]

[^ev-1]: src/payment/
