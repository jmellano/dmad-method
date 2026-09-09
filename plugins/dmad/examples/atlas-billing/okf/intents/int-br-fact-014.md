---
type: Intent
title: Intention — BR-FACT-014
description: Introduit pour éviter un rejet en masse par le SI comptable lors de l'incident
  d'import de mars 2019.
dmad_id: INT-BR-FACT-014
confidence: H
sources:
- id: ev-1
  resource: 9f3e2a1
  kind: commit
- id: ev-2
  resource: jira://ATLAS
  kind: absence
generated:
  by: dmad-archaeologist/0.4.0
  at: '2026-09-08T17:00:00Z'
---

Introduit pour éviter un rejet en masse par le SI comptable lors de l'incident d'import de mars 2019.


# Lecture concurrente

règle comptable légitime : une facture à 0 n'est pas émettable

# Lecture concurrente

contournement technique de 2019 devenu permanent par inertie

# Liens

- explique : [BR-FACT-014](../claims/br-fact-014.md)
