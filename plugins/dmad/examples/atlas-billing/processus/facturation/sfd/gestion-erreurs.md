---
type: "Error Catalog"
title: "Gestion des erreurs du processus"
description: "Les trois sorties anormales du processus, et la distinction entre le site de levée et l'effet observable."
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

| Erreur | Site de levée | Effet observable |
|---|---|---|
| Valorisation impossible | une ligne | facture non créée, campagne poursuivie |
| Transmission refusée | une facture | reprise à la campagne suivante, **cinq fois au maximum** |
| Tarification indisponible | **une ligne** | **la campagne entière s'arrête**, sans notification |

> **Le site de levée et l'effet observable ne sont pas le même fait.** La troisième ligne le montre : l'erreur naît sur une ligne et se voit sur tout le lot. Les confondre produirait deux affirmations contradictoires — et une contradiction laissée ici devient une promesse fausse en SFG.

# Liens

- relève de : [facturation](../../../socle/capacites/facturation.md)
