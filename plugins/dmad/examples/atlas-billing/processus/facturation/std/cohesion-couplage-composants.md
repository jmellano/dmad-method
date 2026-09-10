---
type: "Quality Assessment"
title: "Cohésion et couplage des composants"
description: "Application de la matrice de cohésion et de couplage aux composants du chemin de facturation : ce qui est validé, ce qui est dette."
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
renders: ["BR-FACT-021"]
capability: facturation
---

| Composant / relation | Degré | Fait qui le prouve |
|---|---|---|
| `AmountCalculator` | cohésion **de fonction** ✔ | une seule responsabilité, valoriser une ligne ; prouvée par test de caractérisation (§ 15) |
| `InvoiceDispatcher` | cohésion **séquentielle** ✔ | garde, transmission, marquage d'état s'enchaînent sur le même objet (§ 5) |
| `BillingRun` | cohésion **procédurale** ~ | sélection, boucle et journalisation de campagne partagent l'ordre, pas l'objet |
| `ReinvoiceCommand` → `AccountingGateway` | couplage **de contenu** ✘ | court-circuite `InvoiceDispatcher` et ses gardes (point d'attention 3) |
| `reporting` → table `invoices` | couplage **commun** ✘ | lecture directe de la table sans passer par le module (point d'attention 4) |

Les deux `✘` sont des dettes documentées, pas des découvertes de cette table : elles renvoient à des faits établis ailleurs dans ce document.

# Liens

- relève de : [facturation](../../../socle/capacites/facturation.md)
