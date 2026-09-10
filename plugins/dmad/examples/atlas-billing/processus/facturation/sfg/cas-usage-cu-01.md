---
type: "Business Use Case"
title: "CU-01 — Facturer les livraisons de la nuit"
description: "Cas d'usage CU-01 : sept blocs, dont la frontière explicite de ce qui n'est pas couvert."
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
Chaque nuit, l'entreprise facture les livraisons de la journée. Le client reçoit une facture, la comptabilité l'enregistre, et le recouvrement peut la suivre. Personne n'intervient : c'est le cas d'usage le plus fréquent, et celui dont les erreurs se voient le plus tard.

### Acteurs et rôles métier
Le **client livré**, qui reçoit la facture. Le **service comptable**, qui l'enregistre. Le **gestionnaire de facturation**, qui constate le résultat le lendemain matin.

### Déclencheur et cadence
Automatique, chaque nuit à **02:00:00 Europe/Paris**. Aucun déclenchement manuel de la campagne complète n'existe.

### Règles applicables

| Règle | Intention | Ce que l'utilisateur voit |
|---|---|---|
| RG-001 — seules les livraisons effectuées et non encore facturées entrent dans la campagne | ne facturer que ce qui a été livré **[validé]** | une livraison du jour même apparaît dès la nuit suivante |
| RG-002 — le montant de chaque ligne est calculé au dix-millième, alors que la facture et l'export comptable en affichent deux décimales | *reprise des contrats au pourcentage en 2017, où l'arrondi à deux décimales créait des écarts cumulés sur les gros volumes* **[H — à confirmer]** | des écarts de quelques centimes entre le cumul des lignes et le total affiché, sur les très gros volumes |
| RG-003 — une facture dont le montant total est nul n'est pas transmise à la comptabilité : elle est archivée en l'état | *introduit après l'incident d'import de mars 2019, pour éviter un rejet en masse par la comptabilité* **[H — à confirmer]** | environ 340 factures par an n'arrivent jamais en comptabilité, sans notification |

> ⚠️ **RG-003 ne s'applique pas partout.** Elle dépend d'un réglage qui n'est pas le même selon l'environnement, et la refacturation manuelle (CU-02) ne l'applique pas du tout.

### Ce que l'utilisateur voit
**En cas de succès** — le lendemain matin, un compte-rendu de campagne indiquant le nombre de factures produites et transmises.

**En cas d'échec** — deux situations très différentes. Si une facture échoue à la transmission, elle est reprise les nuits suivantes, **cinq fois au maximum**, puis abandonnée sans alerte. Si le service de tarification est indisponible, **la campagne entière s'arrête** et aucune facture n'est produite cette nuit-là — sans notification.

### Ce qui n'est pas couvert
La relance et le recouvrement des factures impayées, qui relèvent d'un autre domaine. La refacturation à la demande, qui est le CU-02. Les avoirs et les régularisations, qui n'ont pas été analysés. Le traitement des factures une fois arrivées en comptabilité.

### Traçabilité

| Règle | Section SFD |
|---|---|
| RG-001 | [`SFD-facturation.md`](../../../socle/capacites/facturation.md) § 4 — N2, opérations de contrôle |
| RG-002 | [`SFD-facturation.md`](../../../socle/capacites/facturation.md) § 6 — N0, opérations de traitement · `BR-FACT-021` |
| RG-003 | [`SFD-facturation.md`](../../../socle/capacites/facturation.md) § 5 — N1, données de contrôle · `BR-FACT-014` |

# Liens

- relève de : [facturation](../../../socle/capacites/facturation.md)
