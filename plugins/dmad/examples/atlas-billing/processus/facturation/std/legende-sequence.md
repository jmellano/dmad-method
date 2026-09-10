---
type: "Notation Legend"
title: "Légende — diagramme de séquence"
description: "Conventions de lecture des diagrammes de sequence employés dans ce document."
tags: ["légende", "notation"]
generated:
  by: "dmad-diagram-planner/0.4.0"
  at: "2026-09-08T17:00:00Z"
status: "stable"
# — extensions du profil DMAD : voir docs/14-okf.md
module: "billing"
audience: "MOE"
confidence: "high"
renders: []
capability: facturation
---

Ces diagrammes montrent **qui parle à qui, et dans quel ordre**. Le temps descend.

| Élément | Ce qu'il désigne |
|---|---|
| colonne | un participant : composant du périmètre, ou acteur externe |
| flèche pleine | un appel |
| flèche pointillée | une réponse |
| bloc `alt` | une alternative — une seule branche s'exécute |
| bloc `loop` | une répétition, dont la cardinalité est dite en note |
| note | une frontière non franchie par l'analyse |

# Liens

- relève de : [facturation](../../../socle/capacites/facturation.md)
