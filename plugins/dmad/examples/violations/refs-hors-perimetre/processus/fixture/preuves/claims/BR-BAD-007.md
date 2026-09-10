---
type: BusinessRule
title: BR-BAD-007
id: BR-BAD-007
confidence: C
confidence_reason: Deux preuves convergentes au moment de l'analyse, non challengées.
evidence:
- kind: code
  ref: src/Fixture.java#L300-L400
  tool: jcallgraph.definition
produced_by: elucidator
freshness:
  verified_at_commit: aaa1111
  status: fresh
---

<!-- Violation : la preuve cite une plage qui n'existe pas dans le fichier. C'est ainsi qu'une cartographie faite dans une copie hors périmètre passe au vert. -->

Une règle dont la preuve pointe au-delà de la fin du fichier cité.
