---
type: "Business Rule Set"
title: "Invariants du domaine"
description: "Les règles qui valent pour tous les cas d'usage, avec leur intention."
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
capability: facturation
---

| Invariant | Intention | Ce que l'utilisateur voit |
|---|---|---|
| INV-1 — une livraison n'est facturée qu'une fois | éviter les doublons, plus coûteux à corriger qu'à prévenir **[validé]** | une livraison déjà facturée n'apparaît plus dans les campagnes suivantes |
| INV-2 — un client en litige n'est pas facturé | ne pas aggraver un désaccord en cours **[validé]** | ses livraisons sont reportées, sans limite de durée connue |

# Liens

- relève de : [facturation](../../../socle/capacites/facturation.md)
