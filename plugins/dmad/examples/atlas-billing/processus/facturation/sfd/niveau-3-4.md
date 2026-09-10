---
type: "Summary Table"
title: "Synthèse des niveaux"
description: "La table récapitulative : business objects, feuilles propres, sous-objets, profondeur, couche métier."
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
renders: []
capability: facturation
---

| Business object | Feuilles propres | Sous-objets | Profondeur | Couche métier |
|---|---|---|---|---|
| Campagne de facturation | compte-rendu de campagne | Facture à émettre | 2 | orchestration |
| Facture à émettre | factures · service comptable · statuts de litige *(ad-hoc, en boucle)* | Ligne valorisée | 1 | préparation |
| Ligne valorisée | lignes de facture · service de tarification *(ad-hoc, en boucle)* | — | 0 | calcul |

# Liens

- relève de : [facturation](../../../socle/capacites/facturation.md)
