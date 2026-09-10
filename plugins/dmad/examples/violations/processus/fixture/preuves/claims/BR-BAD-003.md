---
type: BusinessRule
title: BR-BAD-003
id: BR-BAD-003
confidence: C
confidence_reason: 'Deux preuves convergentes : garde dans le code et contrainte CHECK
  en base.'
evidence:
- kind: code
  ref: src/billing/CreditNote.java#L44
  tool: jcallgraph.definition
- kind: schema
  ref: credit_notes CHECK (amount <= invoice_amount)
  tool: schema.constraints
intent:
  statement: Contrainte réglementaire imposée par la doctrine comptable.
  confidence: C
  validated_by: null
produced_by: archaeologist
freshness:
  verified_at_commit: a1b2c3d
  status: fresh
---

Les avoirs sont plafonnés au montant de la facture d'origine.[^ev-1][^ev-2]

[^ev-1]: src/billing/CreditNote.java#L44
[^ev-2]: credit_notes CHECK (amount <= invoice_amount)
