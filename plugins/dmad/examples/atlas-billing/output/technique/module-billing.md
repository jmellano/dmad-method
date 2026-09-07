## `src/billing`   [C]

**Rôle** — Émission, calcul et transmission des factures.
**Capacité** — Facturation · **Hotspot** rang 3/20 ⚠️
**Bus factor** — 1 ⚠️ *(87 % des lignes attribuées à un contributeur parti en 2023)*

**Entrées** — `POST /invoices` · `JOB nightly-billing` (cron 0 2 * * *) · `CLI reinvoice`
**Sorties** — SI comptable (HTTP) · tables `invoices`, `invoice_lines`, `billing_runs`
**Dépend de** — `src/catalog` (lecture barèmes) · `src/customer` (lecture, statut litige)
**Dépendu par** — `src/reporting` ⚠️ *lit directement `invoices` sans passer par le module — couplage non prévu par l'architecture, cf. `OQ-021`*

**Points d'attention**

- `AmountCalculator` — arrondi `HALF_UP` à 4 décimales, affichage et export à 2. Écarts possibles sur les cumuls. → `BR-FACT-021` **[V]**
- Flag `billing.skipZeroAmount` — comportement **différent entre la configuration par défaut du dépôt (`false`) et la production (`true`)**. Un développeur qui lance le projet en local n'observe pas le comportement de production. → `BR-FACT-014` **[I]**
- `ReinvoiceCommand` appelle `AccountingGateway.send()` **directement**, sans passer par `InvoiceDispatcher` : les contrôles du dispatcher sont contournés. → `OQ-019`
- 2 dispatchs dynamiques non résolus via `ServiceLocator.get(String)` → `OQ-017`
- Aucun test ne couvre la branche `skipZeroAmount = false`.

**Fichiers clés**

- `BillingRun.java:44` — point d'entrée de la campagne nocturne
- `AmountCalculator.java:88` — calcul et arrondi des montants
- `InvoiceDispatcher.java:212` — garde sur les montants nuls, transmission
- `ports/AccountingGateway.java` — **seam** : port d'export comptable, 3 traversées
- `cli/ReinvoiceCommand.java:47` — chemin alternatif contournant le dispatcher

**Tests** — 14 existants (couverture 41 %) · 6 tests de caractérisation forgés par DMAD

---

## Limites de cette analyse

- **Profondeur de traversée : 5.** 17 frontières atteintes sur l'ensemble du run.
- **2 dispatchs dynamiques non résolus** — les implémentations réellement invoquées en production n'ont pas pu être établies.
- **Aucune trace runtime.** Les chemins décrits sont possibles, pas nécessairement empruntés. La couverture de tests (41 %) ne dit rien de l'usage réel en production.
- **Modules hors périmètre :** `legacy-import`, `reporting-v1`, `admin-tools`.
