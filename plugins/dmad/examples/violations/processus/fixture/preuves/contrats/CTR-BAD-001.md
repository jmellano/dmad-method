---
type: ExternalContract
title: CTR-BAD-001
id: CTR-BAD-001
call_site: src/billing/InvoiceDispatcher.java#L212
code: SIM_APP_ACH_022
resolution_rung: 1
artifact: acme/erp/accounting-api
http_verb: GET
route: /rechercherCommande
operation: rechercherCommande
confidence: V
evidence:
- kind: artifact
  ref: accounting-api-sources.jar!/AccountingExposeWebService.java
produced_by: contract-resolver
---


[^ev-1]: accounting-api-sources.jar!/AccountingExposeWebService.java
