---
type: "Coverage Report"
title: "Couverture de l'analyse"
description: "Ce que le run a atteint, la répartition des niveaux de preuve, et ce qu'il n'a pas couvert."
---

# Couverture de l'analyse — atlas-billing

## Ce qui a été atteint

| Indicateur | Valeur | Poids |
|---|---|---|
| Fichiers atteints | 412 / 1847 (22 %) | faible |
| Fonctions cartographiées | 3108 / 14200 (22 %) | moyen |
| Points d'entrée couverts | 8 / 51 (16 %) | **fort** |
| Hotspots couverts | 18 / 20 (90 %) | **fort** |
| Tables documentées | 12 / 88 (14 %) | moyen |
| **Contrats sortants résolus** | 1 / 2 — barreau 1 : 1 · barreau 4 : 1 | **fort** |

> **La ligne des contrats mesure la qualité des sources, pas le nombre.** Un run
> à 47/47 dont trente sont au barreau 3 — le commentaire manuscrit, qui survit aux
> refactorings et ment alors sans le dire — est un moins bon run qu'un 41/47
> majoritairement au barreau 1. Sans cette ligne, les deux se ressemblent.

## Corpus produit

| Document | Unité | État |
|---|---|---|
| `output/sfd/facturation.md` | BO-FACT-001 | figé le 2026-09-08, 1 correction(s) en revue |
| `output/sfg/facturation.md` | CU-01 | figé le 2026-09-08, 1 correction(s) en revue |
| `output/std/nightly-billing.md` | JOB nightly-billing | figé le 2026-09-07, 1 correction(s) en revue |

**Une revue qui ne demande aucune correction est un signal d'alarme**, pas un
succès : elle signifie que le relecteur n'a pas cherché, ou que le document est
trop vague pour être contesté.

## Répartition des niveaux de preuve

```
V 67 %  ·  C 0 %  ·  I 33 %  ·  H 0 %
```

**Signaux d'alerte**

- `V` > 60 % — suspect : peu de legacy se prouve à ce point

**Effet du Challenger :** 1 claim(s) examinée(s), 1 dégradée(s), scindée(s) ou contredite(s) — soit **100 %**, **hors fourchette** — sous 15 % le Challenger est complaisant, au-dessus de 30 % l'Elucidator produit trop de bruit.

**Questions ouvertes :** 3 — P1 : 1 · P2 : 1 · P3 : 1

## Lecture

22 % du code, mais **100 % des points d'entrée de la facturation et 90 % des hotspots du dépôt**. Les règles de calcul des montants sont couvertes et **prouvées par des tests de caractérisation** — c'est précisément ce que demandait l'objectif du run : changer le barème sans régression comptable.

Les points d'entrée et les hotspots pèsent le plus. Un run qui couvre 22 % des fichiers mais 90 % des zones à risque est un bon run ; un run à 60 % de fichiers qui rate la moitié des points d'entrée est un mauvais run qui en impose.

Trois limites doivent être connues avant d'utiliser cette documentation.

1. **Le comportement du SI comptable en aval n'a pas été analysé** — système externe, hors périmètre. Les règles décrites s'arrêtent à la transmission.
2. **Deux dispatchs dynamiques non résolus** subsistent dans le socle. Rien n'indique qu'ils touchent la facturation, rien ne l'exclut. Les candidats sont enregistrés, aucun n'a été choisi (`OQ-017`).
3. **Un contrat sortant sur deux n'est pas résolu.** Le service de tarification est appelé jusqu'à quarante fois par facture et son contrat reste inconnu : le jour où il tombe, personne ne saura qui appeler (`OQ-024`).

**Sur le fond des artefacts publiés ici.** Ce dossier embarque un échantillon représentatif du run — trois claims sur les quarante et une examinées — parce qu'il sert de fixture de non-régression, pas d'archive. La répartition des niveaux de preuve calculée ci-dessus porte donc sur l'échantillon, pas sur le run complet, qui se répartissait en `V` 34 % · `C` 41 % · `I` 21 % · `H` 4 %.

**Répondre aux cinq questions P1 ferait passer quatorze affirmations d'hypothèse à fait établi**, dont la règle sur les factures à montant nul — la seule qui bloque aujourd'hui le changement de barème en toute sécurité.



# Liens

- voir aussi : [lecture](lecture.md)
- run : [README](../README.md)
