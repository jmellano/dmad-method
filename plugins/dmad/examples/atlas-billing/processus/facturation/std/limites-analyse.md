---
type: "Analysis Boundary"
title: "Limites de cette analyse"
description: "- Profondeur de traversée : 5. 17 frontières atteintes sur l'ensemble du run. - Deux dispatchs dynamiques non résolus — les implémentations réellement"
tags: ["atlas", "facturation", "STD"]
generated:
  by: "dmad-writer-std/0.4.0"
  at: "2026-09-08T17:00:00Z"
status: "stable"
# — extensions du profil DMAD : voir docs/14-okf.md
module: "billing"
audience: "MOE"
confidence: "high"
last_code_sync: "a1b2c3d"
renders: []
capability: facturation
---

- **Profondeur de traversée : 5.** 17 frontières atteintes sur l'ensemble du run.
- **Deux dispatchs dynamiques non résolus** — les implémentations réellement invoquées en production n'ont pas pu être établies. Les candidats sont enregistrés, aucun n'a été choisi.
- **Un contrat sortant non résolu** sur deux — le placeholder du § 9 est volontaire.
- **Aucune trace d'exécution.** Les chemins décrits sont possibles, pas nécessairement empruntés.
- **Modules hors périmètre :** `legacy-import`, `reporting-v1`, `admin-tools`.

# Liens

- relève de : [facturation](../../../socle/capacites/facturation.md)
