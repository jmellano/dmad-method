---
type: ExternalContract
title: CTR-FACT-001
description: CTR-FACT-001
dmad_id: CTR-FACT-001
sources:
- id: ev-1
  resource: accounting-api-4.7.2-sources.jar!/AccountingExposeWebService.java#L44
  author: process:archive.grep
  kind: artifact
- id: ev-2
  resource: src/billing/InvoiceDispatcher.java#L268
  author: process:jcallgraph.callers
  kind: code
generated:
  by: dmad-contract-resolver/0.4.0
  at: '2026-09-08T17:00:00Z'
confidence: V
confidence_reason: 'Annotation de contrat lue dans l''artefact de la dépendance, qui
  fait foi. Invocation confirmée depuis le chemin étudié par recherche de références.

  '
freshness:
  verified_at_commit: a1b2c3d
  status: fresh
resolution_rung: 1
artifact: acme/atlas/accounting-api
artifact_version: 4.7.2
code: ACC_INV_TRANSMIT_001
---



[^ev-1]: accounting-api-4.7.2-sources.jar!/AccountingExposeWebService.java#L44
[^ev-2]: src/billing/InvoiceDispatcher.java#L268
