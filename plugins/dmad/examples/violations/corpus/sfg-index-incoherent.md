---
type: SFG
title: "Fixture"
unit: domain
unit_ref: Fixture
derives_from: ["SFD-fixture.md"]
generated_by: "modèle — fixture de non-régression"
---

<!-- Violation : l'index inverse ne compte plus les mêmes règles. -->

## 1. Ce que le domaine résout

Sans objet dans ce domaine.

## 2. Invariants du domaine

Sans objet dans ce domaine.

## 3. Les cas d'usage

### 3.1 CU-01 — Refacturation

#### Situation

Un magasin est livré et doit être refacturé.

#### Acteurs et rôles métier

Le magasin, la centrale, le fournisseur.

#### Déclencheur et cadence

Chaque nuit à 02:15:00 Europe/Paris.

#### Règles applicables

| Règle | Intention | Ce que l'utilisateur voit |
|---|---|---|
| RG-001 — une arrivée sans commande n'est pas refacturée | éviter les litiges | rien ne part |

#### Ce que l'utilisateur voit

En succès une facture, en échec une notification.

#### Ce qui n'est pas couvert

Les avoirs.

#### Traçabilité

| Règle | Section SFD |
|---|---|
| RG-001 | SFD § 3 |

## 4. Index inverse — quelle règle pour quel cas d'usage

| — | — |

## 5. Ce que la rédaction a révélé

Sans objet dans ce domaine.

## 6. Historique

Sans objet dans ce domaine.
