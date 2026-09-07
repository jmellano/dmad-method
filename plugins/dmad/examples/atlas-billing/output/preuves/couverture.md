# Couverture de l'analyse — atlas-2026-09-07-01

## Ce qui a été atteint

| Indicateur | Valeur | Poids |
|---|---|---|
| Fichiers atteints | 412 / 1 847 (22 %) | faible |
| Fonctions cartographiées | 3 108 / 14 200 (22 %) | moyen |
| **Points d'entrée couverts** | 8 / 8 de la capacité (100 %) · 8 / 51 du dépôt | **fort** |
| **Hotspots couverts** | 18 / 20 (90 %) ✅ | **fort** |
| Tables documentées | 12 / 12 de la capacité (100 %) · 12 / 88 du dépôt | moyen |

> Les points d'entrée et les hotspots pèsent le plus : un run qui couvre 22 % des
> fichiers mais 90 % des zones à risque est un bon run. Un run à 60 % de fichiers
> qui rate la moitié des points d'entrée est un mauvais run qui en impose.

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

**Répondre aux 5 questions P1 ferait passer 14 affirmations d'hypothèse à fait établi**, dont la règle sur les factures à montant nul — la seule qui bloque aujourd'hui le changement de barème en toute sécurité.
