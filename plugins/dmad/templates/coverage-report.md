<!-- TEMPLATE : la seule métrique honnête et calculable produite par DMAD. -->

# Couverture de l'analyse — {{run_id}}

## Ce qui a été atteint

| Indicateur | Valeur | Poids |
|---|---|---|
| Fichiers atteints | {{files_reached}} / {{files_total}} ({{files_pct}} %) | faible |
| Fonctions cartographiées | {{fn_reached}} / {{fn_total}} ({{fn_pct}} %) | moyen |
| **Points d'entrée couverts** | {{ep_reached}} / {{ep_total}} ({{ep_pct}} %) | **fort** |
| **Hotspots couverts** | {{hs_reached}} / 20 ({{hs_pct}} %) | **fort** |
| Tables documentées | {{tbl_reached}} / {{tbl_total}} ({{tbl_pct}} %) | moyen |

> Les points d'entrée et les hotspots pèsent le plus : un run qui couvre 20 % des
> fichiers mais 90 % des zones à risque est un bon run. Un run à 60 % de fichiers
> qui rate la moitié des points d'entrée est un mauvais run qui en impose.

## Répartition des niveaux de preuve

```
V {{v_pct}} %  ·  C {{c_pct}} %  ·  I {{i_pct}} %  ·  H {{h_pct}} %
```

{{#if alerts}}
**Signaux d'alerte**
{{#each alerts}}
- {{this}}
{{/each}}
{{/if}}

## Ce qui n'a PAS été couvert

**Exclu au cadrage**
{{#each excluded}}
- `{{path}}` — {{reason}}
{{/each}}

**Frontières de traversée atteintes** — {{boundaries_count}}
{{#each boundary_groups}}
- {{count}} × {{reason}} : {{examples}}
{{/each}}

{{#if unresolved_dispatch}}
**Dispatchs dynamiques non résolus** — {{unresolved_count}}
Ces points masquent potentiellement des règles de gestion.
{{#each unresolved_dispatch}}
- `{{at}}` — candidats : {{candidates}} → `{{open_question}}`
{{/each}}
{{/if}}

## Lecture

{{honest_summary}}

<!-- Exemple de honest_summary :
     "22 % du code, mais 90 % des hotspots et 100 % des points d'entrée de la
     facturation. Les règles de calcul des montants sont couvertes et prouvées
     par 6 tests. En revanche, le comportement du SI comptable en aval n'a pas
     été analysé (hors périmètre) : les règles décrites s'arrêtent à la
     transmission." -->
