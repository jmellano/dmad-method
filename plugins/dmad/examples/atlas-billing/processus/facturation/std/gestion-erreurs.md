---
type: "Error Catalog"
title: "Gestion des erreurs"
description: "Question : que devient une facture selon l'endroit où l'exécution échoue, et que le support observe-t-il ? Confiance : C — corroboré · aucune trace d"
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

> **Question :** que devient une facture selon l'endroit où l'exécution échoue, et que le support observe-t-il ?
> **Confiance : C — corroboré** · aucune trace d'exécution pour confirmer les fréquences

<!-- diagram: DIA-STD-003 · N=7 E=4 McCabe=1 -->
```mermaid
flowchart TD
  E1["Échec de valorisation"]
  S1["Facture non créée · lot poursuivi"]
  E2["Échec de transmission"]
  S2["Statut FAILED · reprise, 5 tentatives"]
  E3["Échec de tarification"]
  S3["Exception non déclarée · lot interrompu"]
  N["Aucune notification"]
  E1 --> S1
  E2 --> S2
  E3 --> S3
  S3 --> N
```

**Site de levée et effet observable sont distincts, et il faut les lire séparément.** Un échec de tarification est levé sur **une ligne** ; son effet observable est l'interruption de **tout le lot**, parce que l'exception n'est pas déclarée et remonte jusqu'au gestionnaire de campagne. Les confondre produirait deux affirmations contradictoires dans la SFD.

Exceptions **non déclarées** : `PricingUnavailableException` remonte sans être capturée — c'est le chemin qui interrompt le lot.
**Chemin inatteignable** : la branche `skipZeroAmount = false` n'est couverte par aucun test.

# Liens

- relève de : [facturation](../../../socle/capacites/facturation.md)
