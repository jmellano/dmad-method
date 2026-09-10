---
type: BusinessRule
title: BR-BAD-005
id: BR-BAD-005
confidence: C
confidence_reason: Recherche exhaustive effectuée sur l'ensemble du dépôt.
confidence_ceiling_applied: I
evidence:
- kind: code
  ref: src/billing/Invoice.java#L200
  tool: grep
produced_by: cartographer
freshness:
  verified_at_commit: a1b2c3d
  status: fresh
---

Aucun autre appelant ne modifie le statut de la facture.[^ev-1]

[^ev-1]: src/billing/Invoice.java#L200
