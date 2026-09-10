---
type: BusinessRule
title: BR-BAD-008
id: BR-BAD-008
confidence: C
confidence_reason: Deux preuves convergentes au moment de l'analyse, non challengées.
evidence:
- kind: code
  ref: src/Fixture.java#L1-L5
  tool: jcallgraph.definition
  note: if (invoice.getTotal().signum() == 0) { invoice.markSkipped(); return; }
produced_by: elucidator
freshness:
  verified_at_commit: aaa1111
  status: fresh
---

<!-- Violation : du code dans une note. Fermer excerpt sans fermer note déplace la porte. -->

Une règle dont la note contient le code au lieu de le décrire.
