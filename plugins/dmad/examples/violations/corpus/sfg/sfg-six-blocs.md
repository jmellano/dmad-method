---
title: "Facturation — règles métier par cas d'usage"
type: SFG
unit: use_case
unit_ref: CU-01
derives_from: ["sfd/refacturation.md"]
generated_by: "modèle — fixture de non-régression"
---

<!-- Violation : « Ce qui n'est pas couvert » manque — le bloc qu'on oublie, et le plus structurant. -->

## CU-01 — Refacturation d'une arrivée

### Situation

Un magasin reçoit une livraison et doit être refacturé.

### Acteurs et rôles métier

Le magasin livré, la centrale, le fournisseur.

### Déclencheur et cadence

Chaque nuit à 02:15:00 Europe/Paris.

### Règles applicables

| Règle | Intention | Ce que l'utilisateur voit |
|---|---|---|
| RG-001 — une arrivée sans commande n'est pas refacturée | éviter les litiges | rien ne part |

### Ce que l'utilisateur voit

En succès, une facture. En échec, une notification par arrivée.

### Traçabilité

| Règle | Section SFD |
|---|---|
| RG-001 | sfd/refacturation.md § N2 |

## Index inverse — règle → cas d'usage

| RG-001 | CU-01 |
