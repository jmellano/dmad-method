---
type: "Change Log"
title: "Historique du document"
description: "Les versions, dont les corrections factuelles avec ce qui était écrit et pourquoi c'était faux."
tags: ["atlas", "facturation", "SFG"]
generated:
  by: "dmad-writer-sfg/0.4.0"
  at: "2026-09-08T17:00:00Z"
status: "draft"
# — extensions du profil DMAD : voir docs/14-okf.md
module: "billing"
audience: "Utilisateurs métier"
confidence: "medium"
unite_evolution: "cas d'usage"
last_code_sync: "a1b2c3d"
renders: []
---

| Date | Version | Nature |
|---|---|---|
| 2026-09-08 | 1.0 | Rédaction initiale depuis la SFD figée |
| 2026-09-08 | 1.1 | **Correction factuelle.** La version 1.0 écrivait qu'un échec de transmission entraînait une reprise indéfinie, et présentait cela comme une garantie de non-perte. C'était faux : la reprise s'arrête à cinq campagnes, puis la facture est abandonnée sans alerte. La source de l'erreur était une dérivation trop rapide de la SFD, qui disait « reprise à la campagne suivante » sans dire jusqu'à quand. La formulation corrigée est plus utile que l'originale : elle nomme le moment où le support doit intervenir. |
| 2026-09-08 | 1.2 | Deux intentions validées et tracées en revue de cycle 3. La troisième (RG-002) reste en hypothèse. |

# Liens

- section de : [DOC-SFG-FACT-001](../../../documents/doc-sfg-fact-001.md)
