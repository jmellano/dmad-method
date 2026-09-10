---
type: BusinessRule
title: BR-BAD-011
id: BR-BAD-011
confidence: C
confidence_reason: Deux preuves convergentes au moment de l'analyse, non challengées.
evidence:
- kind: code
  ref: src/Fixture.java#L1-L5
  tool: jcallgraph.definition
produced_by: elucidator
freshness:
  verified_at_commit: aaa1111
  status: fresh
intent:
  statement: Introduit pour éviter les rejets comptables.
  confidence: C
  validated_by:
    who: Commanditaire
    when: '2026-09-09T10:00:00Z'
    gate: conduite/gates/gate-inexistant.md#decision
---

<!-- Violation : une validation d'intention qui cite un gate inexistant. -->

Une règle dont l'intention se dit validée par l'agent qui l'a produite.
