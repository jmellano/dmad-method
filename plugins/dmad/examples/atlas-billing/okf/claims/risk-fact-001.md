---
type: Risk
title: RISK-FACT-001
description: Le module src/billing est le 3e hotspot du dépôt (churn x complexité)
  et 87 % de ses lignes sont attribuées à un unique contributeur, parti en 2023.
dmad_id: RISK-FACT-001
tags:
- facturation
sources:
- id: ev-1
  resource: src/billing/@a1b2c3d
  author: process:git.churn
  kind: code
- id: ev-2
  resource: src/billing/
  author: process:git.shortlog
  kind: code
- id: ev-3
  resource: git shortlog --since=2023-06
  kind: absence
generated:
  by: dmad-surveyor/0.4.0
  at: '2026-09-08T17:00:00Z'
confidence: V
confidence_reason: 'Fait mécanique : mesures produites par git log et git shortlog
  sur l''historique complet, sans interprétation. Rien à prouver au-delà de l''exécution
  de l''outil.

  '
freshness:
  verified_at_commit: a1b2c3d
  verified_at: '2026-09-07T10:14:00Z'
  status: fresh
---

Le module src/billing est le 3e hotspot du dépôt (churn x complexité) et 87 % de ses lignes sont attribuées à un unique contributeur, parti en 2023. Son bus factor est de 1.[^ev-1][^ev-2][^ev-3]

[^ev-1]: src/billing/@a1b2c3d
[^ev-2]: src/billing/
[^ev-3]: git shortlog --since=2023-06

# Liens

- en relation avec : [BR-FACT-021](br-fact-021.md)
- en relation avec : [BR-FACT-014](br-fact-014.md)
- relève de : [facturation](../capabilities/facturation.md)
