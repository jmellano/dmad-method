---
type: "Business Use Case"
title: "CU-02 — Refacturer une livraison à la demande"
description: "Cas d'usage CU-02 : sept blocs, dont la frontière explicite de ce qui n'est pas couvert."
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
renders: ["BR-FACT-014", "BR-FACT-021"]
capability: facturation
---

### Situation
Une facture est erronée, perdue, ou doit être réémise après correction. Le support la refait à la demande, pour une livraison précise.

### Acteurs et rôles métier
L'**opérateur du support**, qui déclenche. Le **client**, qui reçoit la nouvelle facture. Le **service comptable**, qui l'enregistre.

### Déclencheur et cadence
À la demande, sans cadence. Aucune trace du volume réel : ce cas d'usage n'est pas mesuré.

### Règles applicables

| Règle | Intention | Ce que l'utilisateur voit |
|---|---|---|
| RG-004 — la refacturation recalcule le montant et transmet la facture, **sans appliquer la règle RG-003** | *échappatoire laissée au support pour les cas que la campagne automatique ne sait pas traiter* **[H — à confirmer]** | une facture à montant nul refaite par le support **arrive** en comptabilité, alors que la même facture produite la nuit n'y arrive pas |

> ⚠️ C'est la divergence la plus contre-intuitive du domaine, et la question ouverte `OQ-019` porte précisément dessus : est-ce voulu ?

### Ce que l'utilisateur voit
**En cas de succès** — la facture est réémise et transmise immédiatement.

**En cas d'échec** — aucun comportement de reprise n'a été identifié. L'opérateur doit relancer lui-même.

### Ce qui n'est pas couvert
L'annulation d'une facture déjà transmise. La correction d'une facture sans réémission. Le contrôle de doublon entre la facture d'origine et la refacturation — **rien n'indique qu'il existe**.

### Traçabilité

| Règle | Section SFD |
|---|---|
| RG-004 | [`SFD-facturation.md`](../../../socle/capacites/facturation.md) § 5 — N1, opérations de contrôle · `OQ-019` |

# Liens

- relève de : [facturation](../../../socle/capacites/facturation.md)
