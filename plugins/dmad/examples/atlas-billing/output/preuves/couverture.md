# Couverture de l'analyse — atlas-2026-09-07-01

## Ce qui a été atteint

| Indicateur | Valeur | Poids |
|---|---|---|
| Fichiers atteints | 412 / 1 847 (22 %) | faible |
| Fonctions cartographiées | 3 108 / 14 200 (22 %) | moyen |
| **Points d'entrée couverts** | 8 / 8 de la capacité (100 %) · 8 / 51 du dépôt | **fort** |
| **Hotspots couverts** | 18 / 20 (90 %) ✅ | **fort** |
| Tables documentées | 12 / 12 de la capacité (100 %) · 12 / 88 du dépôt | moyen |
| **Contrats sortants résolus** | 1 / 2 — barreau 1 : 1 · barreau 4 : 1 | **fort** |

> Les points d'entrée et les hotspots pèsent le plus : un run qui couvre 22 % des
> fichiers mais 90 % des zones à risque est un bon run. Un run à 60 % de fichiers
> qui rate la moitié des points d'entrée est un mauvais run qui en impose.

> **La ligne des contrats mesure la qualité des sources, pas seulement le nombre.**
> Un run à 47/47 dont trente sont au barreau 3 — le commentaire manuscrit, qui
> survit aux refactorings et ment alors sans le dire — est un moins bon run qu'un
> 41/47 majoritairement au barreau 1. Sans cette ligne, les deux se ressemblent.

## Corpus produit

| Document | Unité | État |
|---|---|---|
| [`std/nightly-billing.md`](../std/nightly-billing.md) | point d'entrée `nightly-billing` | figée le 2026-09-07, une correction en revue |
| [`sfd/facturation.md`](../sfd/facturation.md) | arbre `Campagne de facturation` | figée le 2026-09-08, une correction en revue |
| [`sfg/facturation.md`](../sfg/facturation.md) | deux cas d'usage | figée le 2026-09-08, deux intentions validées sur trois |

Les trois revues ont demandé des corrections. **Une revue qui n'en demande aucune
serait un signal d'alarme** : elle signifierait que le relecteur n'a pas cherché,
ou que le document est trop vague pour être contesté.

## Répartition des niveaux de preuve

```
V 34 %  ·  C 41 %  ·  I 21 %  ·  H 4 %
```

Aucun signal d'alerte : la répartition est dans les bornes attendues pour un legacy réel.
Le taux de `V` (34 %) s'explique par 6 tests de caractérisation forgés et par un schéma de données richement contraint.

**Effet du Challenger :** 41 claims examinées, 9 dégradées, 2 scindées, 1 contredite — soit **29 %**, dans la fourchette attendue (15–30 %).

## Ce qui n'a PAS été couvert

**Exclu au cadrage**
- `src/legacy-import` — arrêté en 2021, aucun appel entrant (vérifié)
- `src/reporting-v1` — remplacé, hors objectif
- `vendor/` — dépendances tierces

**Frontières de traversée atteintes** — 17
- 11 × frontière d'infrastructure : appels au SI comptable, envois de mail, accès FTP
- 4 × limite de profondeur (5) : socle technique commun
- 2 × dispatch dynamique non résolu

**Dispatchs dynamiques non résolus** — 2
Ces points masquent potentiellement des règles de gestion.
- `src/core/ServiceLocator.java:88` — candidats : `BillingService`, `LegacyBillingService` → `OQ-017`
- `src/core/HandlerRegistry.java:34` — candidats non déterminés → `OQ-017`

## Lecture

22 % du code, mais **100 % des points d'entrée de la facturation et 90 % des hotspots du dépôt**. Les règles de calcul des montants sont couvertes et **prouvées par 6 tests de caractérisation** — c'est précisément ce que demandait l'objectif du run (changer le barème sans régression comptable).

En revanche, deux limites doivent être connues avant d'utiliser cette documentation :

1. **Le comportement du SI comptable en aval n'a pas été analysé** (système externe, hors périmètre). Les règles décrites s'arrêtent à la transmission.
2. **Deux dispatchs dynamiques non résolus** subsistent dans le socle. Rien n'indique qu'ils touchent la facturation, mais rien ne l'exclut non plus.
3. **Un contrat sortant sur deux n'est pas résolu.** Le service de tarification est appelé jusqu'à quarante fois par facture, et son contrat reste inconnu : le jour où il tombe, personne ne saura qui appeler (`OQ-024`).

**Répondre aux 5 questions P1 ferait passer 14 affirmations d'hypothèse à fait établi**, dont la règle sur les factures à montant nul — la seule qui bloque aujourd'hui le changement de barème en toute sécurité.
