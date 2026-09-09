---
type: BusinessRule
title: BR-FACT-014
description: 'Lorsque le paramètre billing.skipZeroAmount est actif, une facture dont
  le montant TTC est nul n''est pas transmise au SI comptable : elle est archivée
  avec le statut SKIPPED.'
dmad_id: BR-FACT-014
tags:
- facturation
sources:
- id: ev-1
  resource: src/billing/InvoiceDispatcher.java#L212-L228@a1b2c3d
  author: process:jcallgraph.definition
  kind: code
- id: ev-2
  resource: config/application-prod.yml#L88
  author: process:grep
  kind: config
- id: ev-3
  resource: src/config/BillingConfig.java#L34
  author: process:jcallgraph.definition
  kind: config
- id: ev-4
  resource: invoices.status ENUM('DRAFT','SENT','SKIPPED','FAILED')
  author: process:schema.columns
  kind: schema
- id: ev-5
  resource: src/test/billing/
  kind: absence
generated:
  by: dmad-elucidator/0.4.0
  at: '2026-09-08T17:00:00Z'
status: draft
confidence: I
confidence_reason: 'Dégradée de C à I par CHK-2026-09-07-031 : la règle initialement
  énoncée sans condition est en réalité pilotée par un feature flag actif en production
  mais inactif dans la configuration par défaut du dépôt. Reformulée pour expliciter
  la condition. Pour monter en V, il faudrait un test de caractérisation couvrant
  les deux branches du flag.

  '
conditional_on:
  kind: feature_flag
  key: billing.skipZeroAmount
  default: 'false'
  observed:
    prod: 'true'
    recette: 'true'
    defaut_depot: 'false'
challenge_outcome: demoted
freshness:
  verified_at_commit: a1b2c3d
  verified_at: '2026-09-07T13:20:00Z'
  status: fresh
  last_checked: '2026-09-07T13:20:00Z'
---

Lorsque le paramètre billing.skipZeroAmount est actif, une facture dont le montant TTC est nul n'est pas transmise au SI comptable : elle est archivée avec le statut SKIPPED. Lorsque le paramètre est inactif, elle est transmise normalement.[^ev-1][^ev-2][^ev-3][^ev-4][^ev-5]

[^ev-1]: src/billing/InvoiceDispatcher.java#L212-L228@a1b2c3d
[^ev-2]: config/application-prod.yml#L88
[^ev-3]: src/config/BillingConfig.java#L34
[^ev-4]: invoices.status ENUM('DRAFT','SENT','SKIPPED','FAILED')
[^ev-5]: src/test/billing/

# Liens

- question ouverte : [OQ-012](../open-questions/oq-012.md)
- question ouverte : [OQ-019](../open-questions/oq-019.md)
- réfuté par : [CHK-2026-09-07-031](../challenges/chk-2026-09-07-031.md)
- relève de : [facturation](../capabilities/facturation.md)
- intention supposée : [INT-BR-FACT-014](../intents/int-br-fact-014.md)
