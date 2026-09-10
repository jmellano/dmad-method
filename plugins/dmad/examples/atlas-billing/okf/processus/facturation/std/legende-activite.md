---
type: "Notation Legend"
title: "Légende — diagramme d'activité"
description: "Conventions de lecture des diagrammes de activite employés dans ce document."
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
---

Ces diagrammes se lisent de gauche à droite ou de haut en bas, chaque nœud étant une opération ou une donnée, chaque flèche un enchaînement.

| Forme | Ce qu'elle désigne |
|---|---|
| rectangle | une opération du processus |
| cylindre | une donnée persistée — table, fichier |
| double rectangle | une frontière du système — service externe, port |
| cercle | un point de départ ou d'arrivée |
| flèche pointillée | une lecture ou une écriture, par opposition à un enchaînement |

# Liens

- section de : [DOC-STD-FACT-001](../../../documents/doc-std-fact-001.md)
