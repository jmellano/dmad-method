# Task 70 — Calculer la couverture

**Agent :** `curator` · **Phase :** 6 · **Sortie :** `preuves/couverture.md`

## Pourquoi c'est un livrable et non une métrique interne
C'est la **seule mesure honnête et calculable** que produit DMAD — par opposition à un pourcentage de confiance, qui serait une opinion déguisée en chiffre. Elle permet de revendiquer un bon résultat partiel plutôt que de laisser croire à l'exhaustivité.

## Les cinq indicateurs

| Indicateur | Calcul | Poids |
|---|---|---|
| Fichiers atteints | touchés par ≥1 traversée / périmètre | faible |
| Fonctions cartographiées | nœuds `Function` / fonctions recensées | moyen |
| **Entrypoints couverts** | tracés / recensés | **fort** |
| **Hotspots couverts** | documentés / top 20 | **fort** |
| Tables documentées | reliées à ≥1 claim / schéma | moyen |

Les entrypoints et les hotspots pèsent le plus. **Un run qui couvre 20 % des fichiers mais 90 % des hotspots et 100 % des entrypoints est un excellent run.** Un run à 60 % de fichiers qui rate la moitié des entrypoints est un mauvais run qui en impose.

## Ajouter la répartition des niveaux

```
V 34 % · C 41 % · I 21 % · H 4 %
```

Avec les signaux d'alerte du gate 5 : `V` > 60 % suspect, `H` > 25 % = historique manquant, `I` > 50 % = outillage dégradé.

## Rédiger le non-couvert
Ne pas se contenter du pourcentage. Nommer **quoi** et **pourquoi** :

```markdown
**Non couvert :** modules `legacy-import`, `reporting-v1`, `admin-tools`
(exclus au gate 0). 17 frontières de traversée atteintes, dont 2 dispatchs
dynamiques non résolus qui masquent potentiellement des règles.
```

La mention des frontières est ce qui empêche un lecteur de confondre « non couvert par choix » et « non couvert par limite technique ».
