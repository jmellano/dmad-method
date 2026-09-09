---
type: BusinessRule
title: BR-FACT-021
description: Le montant de chaque ligne de facture est calculé avec une précision
  de 4 décimales et un arrondi au demi-supérieur (HALF_UP), puis stocké tel quel.
dmad_id: BR-FACT-021
tags:
- facturation
sources:
- id: ev-1
  resource: src/billing/AmountCalculator.java#L88-L140@a1b2c3d
  author: process:jcallgraph.definition
  kind: code
- id: ev-2
  resource: invoice_lines.amount DECIMAL(12,4)
  author: process:schema.columns
  kind: schema
- id: ev-3
  resource: src/test/characterization/AmountCalculatorCharacterizationTest.java#L22-L58
  author: process:maven.test
  kind: test
  outcome: passing
- id: ev-4
  resource: src/accounting/export/CsvWriter.java#L61
  author: process:jcallgraph.callers
  kind: code
generated:
  by: dmad-elucidator/0.4.0
  at: '2026-09-08T17:00:00Z'
verified:
- by: process:characterization-test
  at: '2026-09-08T17:00:00Z'
confidence: V
confidence_reason: 'Promue en V : le test de caractérisation forgé (CT-FACT-021) passe
  sur le code actuel et couvre les trois cas d''arrondi limites. Le type DECIMAL(12,4)
  en base corrobore mécaniquement la précision.

  '
challenge_outcome: confirmed
freshness:
  verified_at_commit: a1b2c3d
  verified_at: '2026-09-07T14:05:00Z'
  status: fresh
  last_checked: '2026-09-07T14:05:00Z'
---

Le montant de chaque ligne de facture est calculé avec une précision de 4 décimales et un arrondi au demi-supérieur (HALF_UP), puis stocké tel quel. L'affichage et l'export comptable n'en présentent que 2.[^ev-1][^ev-2][^ev-3][^ev-4]

[^ev-1]: src/billing/AmountCalculator.java#L88-L140@a1b2c3d
[^ev-2]: invoice_lines.amount DECIMAL(12,4)
[^ev-3]: src/test/characterization/AmountCalculatorCharacterizationTest.java#L22-L58
[^ev-4]: src/accounting/export/CsvWriter.java#L61

# Liens

- relève de : [facturation](../capabilities/facturation.md)
- intention supposée : [INT-BR-FACT-021](../intents/int-br-fact-021.md)
