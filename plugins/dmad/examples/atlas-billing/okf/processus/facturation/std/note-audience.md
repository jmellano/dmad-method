---
type: "Reader Guide"
title: "STD nightly-billing — audience et périmètre"
description: "À qui s'adresse la STD du processus de facturation nocturne, ce qu'elle couvre et ce qu'elle exclut."
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
---

> **Audience.** Purement MOE — développeur, architecte, opérateur qui doit intervenir sur la solution. Elle expose ce que la SFD retient hors de son périmètre : noms de classes, patrons nommés, attributs transactionnels, tables, dépendances.
>
> **Périmètre.** Processus de facturation — un job planifié et une route de refacturation manuelle. Le § 1 les catalogue.
>
> **Aucun bloc de code** : la STD porte des références — `fichier:lignes`, signatures, noms de tables (D16).

# Liens

- section de : [DOC-STD-FACT-001](../../../documents/doc-std-fact-001.md)
