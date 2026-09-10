---
type: "Business Rule Set"
title: "Règles de gestion du processus"
description: "Les deux règles de gestion établies sur ce processus, avec leur niveau de preuve."
tags: ["atlas", "facturation", "SFD"]
generated:
  by: "dmad-writer-sfd/0.4.0"
  at: "2026-09-08T17:00:00Z"
status: "stable"
# — extensions du profil DMAD : voir docs/14-okf.md
module: "billing"
audience: "hybride MOA/MOE"
confidence: "medium"
last_code_sync: "a1b2c3d"
renders: ["BR-FACT-021", "BR-FACT-014"]
---

| Règle | Énoncé | Niveau |
|---|---|---|
| `BR-FACT-021` | le montant de chaque ligne est calculé au dix-millième, arrondi au demi-supérieur, alors que l'affichage en montre deux décimales | **V** |
| `BR-FACT-014` | une facture à montant nul n'est pas transmise **lorsque le paramètre d'exclusion est actif** — il l'est en production, pas par défaut dans le dépôt | **I** |

# Liens

- section de : [DOC-SFD-FACT-001](../../../documents/doc-sfd-fact-001.md)
- publie : [BR-FACT-021](../../../claims/br-fact-021.md)
- publie : [BR-FACT-014](../../../claims/br-fact-014.md)
