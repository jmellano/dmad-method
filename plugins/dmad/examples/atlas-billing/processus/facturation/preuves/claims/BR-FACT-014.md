---
type: BusinessRule
title: BR-FACT-014
description: 'Lorsque le paramètre billing.skipZeroAmount est actif, une facture dont
  le montant TTC est nul n''est pas transmise au SI comptable : elle est archivée
  avec le statut SKIPPED. Lorsq…'
id: BR-FACT-014
capability: facturation
confidence: I
confidence_reason: 'Dégradée de C à I par CHK-2026-09-07-031 : la règle initialement
  énoncée sans condition est en réalité pilotée par un feature flag actif en production
  mais inactif dans la configuration par défaut du dépôt. Reformulée pour expliciter
  la condition. Pour monter en V, il faudrait un test de caractérisation couvrant
  les deux branches du flag.

  '
evidence:
- kind: code
  ref: src/billing/InvoiceDispatcher.java#L212-L228
  commit: a1b2c3d
  tool: jcallgraph.definition
- kind: config
  ref: config/application-prod.yml#L88
  tool: grep
- kind: config
  ref: src/config/BillingConfig.java#L34
  tool: jcallgraph.definition
- kind: schema
  ref: invoices.status ENUM('DRAFT','SENT','SKIPPED','FAILED')
  tool: schema.columns
- kind: absence
  ref: src/test/billing/
  note: aucun test ne couvre la branche flag=false
conditional_on:
  kind: feature_flag
  key: billing.skipZeroAmount
  default: 'false'
  observed:
    prod: 'true'
    recette: 'true'
    defaut_depot: 'false'
intent:
  statement: 'Introduit pour éviter un rejet en masse par le SI comptable lors de
    l''incident d''import de mars 2019.

    '
  confidence: H
  evidence:
  - kind: commit
    ref: 9f3e2a1
    note: '2019-03-15 18:47 — fix(billing): skip zero-amount invoices - cf INC-4471'
  - kind: absence
    ref: jira://ATLAS
    note: aucune trace de validation métier associée à INC-4471
  competing_hypotheses:
  - 'règle comptable légitime : une facture à 0 n''est pas émettable'
  - contournement technique de 2019 devenu permanent par inertie
  validated_by: null
  question: OQ-012
relates_to:
- UC-FACT-003
challenged_by:
- CHK-2026-09-07-031
challenge_outcome: demoted
open_questions:
- OQ-012
- OQ-019
produced_by: elucidator
claim_status: challenged
freshness:
  verified_at_commit: a1b2c3d
  verified_at: '2026-09-07T13:20:00Z'
  status: fresh
  last_checked: '2026-09-07T13:20:00Z'
---

Lorsque le paramètre billing.skipZeroAmount est actif, une facture dont le montant TTC est nul n'est pas transmise au SI comptable : elle est archivée avec le statut SKIPPED. Lorsque le paramètre est inactif, elle est transmise normalement.[^ev-1][^ev-2][^ev-3][^ev-4][^ev-5]

[^ev-1]: src/billing/InvoiceDispatcher.java#L212-L228
[^ev-2]: config/application-prod.yml#L88
[^ev-3]: src/config/BillingConfig.java#L34
[^ev-4]: invoices.status ENUM('DRAFT','SENT','SKIPPED','FAILED')
[^ev-5]: src/test/billing/

# Liens

- question ouverte : [OQ-012](../questions/OQ-012.md)
- question ouverte : [OQ-019](../questions/OQ-019.md)
- réfuté par : [CHK-2026-09-07-031](../challenges/CHK-2026-09-07-031.md)
- relève de : [facturation](../../../../socle/capacites/facturation.md)
