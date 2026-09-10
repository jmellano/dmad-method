---
module: billing
audience: Utilisateurs métier des SCA
confidence: medium
unite_evolution: cas d'usage
perimetre: la facturation des livraisons, vue de l'utilisateur
last_code_sync: a1b2c3d
generated_at: '2026-09-08'
generated_by: dmad-writer-sfg/0.4.0 — composé depuis le bundle OKF
type: SFG
title: SFG — Facturation
unit: domain
unit_ref: Facturation
derives_from:
- output/SFD-facturation.md
---

# SFG — Facturation

Ce document s'adresse aux personnes qui **reçoivent, contestent ou relancent** des factures. Il dit ce que le système fait pour elles, et ce qu'elles peuvent en attendre.

Vous n'y trouverez ni écran, ni délai technique, ni nom de composant : ces informations sont dans les documents techniques du même domaine, référencés en fin de chaque cas d'usage.

Le document est découpé **par cas d'usage** — c'est-à-dire par ce qui se demande, s'arbitre et se livre d'un seul bloc. Une demande d'évolution porte sur un cas d'usage entier, jamais sur une moitié. C'est pourquoi chaque cas d'usage dit aussi ce qu'il **ne** couvre pas.

Les intentions — la colonne « pourquoi » — sont des reconstructions. Celles qui n'ont pas été confirmées par un humain portent la mention **[H]**.

## 1. Ce que le domaine résout

Une entreprise livre des marchandises à ses clients tout au long du mois. Chaque livraison doit être facturée : au bon montant, au bon client, une seule fois, et transmise à la comptabilité pour être encaissée et suivie.

Le problème n'est pas de calculer un total. Il est de le faire **sans oubli et sans doublon**, sur plusieurs milliers de livraisons par mois, alors que certains clients contestent, que les barèmes varient d'un contrat à l'autre, et qu'une facture partie deux fois coûte plus cher à corriger qu'à éviter.

## 2. Invariants du domaine

| Invariant | Intention | Ce que l'utilisateur voit |
|---|---|---|
| INV-1 — une livraison n'est facturée qu'une fois | éviter les doublons, plus coûteux à corriger qu'à prévenir **[validé]** | une livraison déjà facturée n'apparaît plus dans les campagnes suivantes |
| INV-2 — un client en litige n'est pas facturé | ne pas aggraver un désaccord en cours **[validé]** | ses livraisons sont reportées, sans limite de durée connue |

## 3. Les cas d'usage

### 3.1 CU-01 — Facturer les livraisons de la nuit

#### Situation
Chaque nuit, l'entreprise facture les livraisons de la journée. Le client reçoit une facture, la comptabilité l'enregistre, et le recouvrement peut la suivre. Personne n'intervient : c'est le cas d'usage le plus fréquent, et celui dont les erreurs se voient le plus tard.

#### Acteurs et rôles métier
Le **client livré**, qui reçoit la facture. Le **service comptable**, qui l'enregistre. Le **gestionnaire de facturation**, qui constate le résultat le lendemain matin.

#### Déclencheur et cadence
Automatique, chaque nuit à **02:00:00 Europe/Paris**. Aucun déclenchement manuel de la campagne complète n'existe.

#### Règles applicables
| Règle | Intention | Ce que l'utilisateur voit |
|---|---|---|
| RG-001 — seules les livraisons effectuées et non encore facturées entrent dans la campagne | ne facturer que ce qui a été livré **[validé]** | une livraison du jour même apparaît dès la nuit suivante |
| RG-002 — le montant de chaque ligne est calculé au dix-millième, alors que la facture et l'export comptable en affichent deux décimales | *reprise des contrats au pourcentage en 2017, où l'arrondi à deux décimales créait des écarts cumulés sur les gros volumes* **[H — à confirmer]** | des écarts de quelques centimes entre le cumul des lignes et le total affiché, sur les très gros volumes |
| RG-003 — une facture dont le montant total est nul n'est pas transmise à la comptabilité : elle est archivée en l'état | *introduit après l'incident d'import de mars 2019, pour éviter un rejet en masse par la comptabilité* **[H — à confirmer]** | environ 340 factures par an n'arrivent jamais en comptabilité, sans notification |

> ⚠️ **RG-003 ne s'applique pas partout.** Elle dépend d'un réglage qui n'est pas le même selon l'environnement, et la refacturation manuelle (CU-02) ne l'applique pas du tout.

#### Ce que l'utilisateur voit
**En cas de succès** — le lendemain matin, un compte-rendu de campagne indiquant le nombre de factures produites et transmises.

**En cas d'échec** — deux situations très différentes. Si une facture échoue à la transmission, elle est reprise les nuits suivantes, **cinq fois au maximum**, puis abandonnée sans alerte. Si le service de tarification est indisponible, **la campagne entière s'arrête** et aucune facture n'est produite cette nuit-là — sans notification.

#### Ce qui n'est pas couvert
La relance et le recouvrement des factures impayées, qui relèvent d'un autre domaine. La refacturation à la demande, qui est le CU-02. Les avoirs et les régularisations, qui n'ont pas été analysés. Le traitement des factures une fois arrivées en comptabilité.

#### Traçabilité
| Règle | Section SFD |
|---|---|
| RG-001 | [`SFD-facturation.md`](../okf/documents/doc-sfd-fact-001.md) § 4 — N2, opérations de contrôle |
| RG-002 | [`SFD-facturation.md`](../okf/documents/doc-sfd-fact-001.md) § 6 — N0, opérations de traitement · `BR-FACT-021` |
| RG-003 | [`SFD-facturation.md`](../okf/documents/doc-sfd-fact-001.md) § 5 — N1, données de contrôle · `BR-FACT-014` |

### 3.2 CU-02 — Refacturer une livraison à la demande

#### Situation
Une facture est erronée, perdue, ou doit être réémise après correction. Le support la refait à la demande, pour une livraison précise.

#### Acteurs et rôles métier
L'**opérateur du support**, qui déclenche. Le **client**, qui reçoit la nouvelle facture. Le **service comptable**, qui l'enregistre.

#### Déclencheur et cadence
À la demande, sans cadence. Aucune trace du volume réel : ce cas d'usage n'est pas mesuré.

#### Règles applicables
| Règle | Intention | Ce que l'utilisateur voit |
|---|---|---|
| RG-004 — la refacturation recalcule le montant et transmet la facture, **sans appliquer la règle RG-003** | *échappatoire laissée au support pour les cas que la campagne automatique ne sait pas traiter* **[H — à confirmer]** | une facture à montant nul refaite par le support **arrive** en comptabilité, alors que la même facture produite la nuit n'y arrive pas |

> ⚠️ C'est la divergence la plus contre-intuitive du domaine, et la question ouverte `OQ-019` porte précisément dessus : est-ce voulu ?

#### Ce que l'utilisateur voit
**En cas de succès** — la facture est réémise et transmise immédiatement.

**En cas d'échec** — aucun comportement de reprise n'a été identifié. L'opérateur doit relancer lui-même.

#### Ce qui n'est pas couvert
L'annulation d'une facture déjà transmise. La correction d'une facture sans réémission. Le contrôle de doublon entre la facture d'origine et la refacturation — **rien n'indique qu'il existe**.

#### Traçabilité
| Règle | Section SFD |
|---|---|
| RG-004 | [`SFD-facturation.md`](../okf/documents/doc-sfd-fact-001.md) § 5 — N1, opérations de contrôle · `OQ-019` |

## 4. Index inverse — quelle règle pour quel cas d'usage

| Règle | Cas d'usage |
|---|---|
| INV-1 | CU-01, CU-02 |
| INV-2 | CU-01 |
| RG-001 | CU-01 |
| RG-002 | CU-01 |
| RG-003 | CU-01 |
| RG-004 | CU-02 |

## 5. Ce que la rédaction a révélé

**De méthode.** Le découpage initial suivait les deux points d'entrée techniques. Il a fallu écrire les deux sections en entier pour voir que la vraie ligne de partage n'est pas là : ce qui distingue CU-01 de CU-02 n'est pas le déclencheur mais **le jeu de règles appliqué**. Un cas d'usage se découpe par ce qui évolue ensemble.

**Arbitrage attendu — RG-003 et RG-004.** Deux chemins produisent des résultats différents pour la même facture. Trois options : aligner la refacturation sur la campagne, documenter l'échappatoire comme volontaire, ou supprimer la règle des deux côtés si l'incident de 2019 n'a plus lieu d'être. La réponse à `OQ-012` décide des trois.

**Arbitrage attendu — RG-002.** L'intention n'a pas pu être validée : personne dans l'équipe actuelle ne sait pourquoi la précision est passée à quatre décimales en 2017. Le commit existe, son auteur est parti. Soit on l'accepte comme une contrainte héritée, soit on la requestionne avant le changement de barème.

## 6. Historique

| Date | Version | Nature |
|---|---|---|
| 2026-09-08 | 1.0 | Rédaction initiale depuis la SFD figée |
| 2026-09-08 | 1.1 | **Correction factuelle.** La version 1.0 écrivait qu'un échec de transmission entraînait une reprise indéfinie, et présentait cela comme une garantie de non-perte. C'était faux : la reprise s'arrête à cinq campagnes, puis la facture est abandonnée sans alerte. La source de l'erreur était une dérivation trop rapide de la SFD, qui disait « reprise à la campagne suivante » sans dire jusqu'à quand. La formulation corrigée est plus utile que l'originale : elle nomme le moment où le support doit intervenir. |
| 2026-09-08 | 1.2 | Deux intentions validées et tracées en revue de cycle 3. La troisième (RG-002) reste en hypothèse. |
