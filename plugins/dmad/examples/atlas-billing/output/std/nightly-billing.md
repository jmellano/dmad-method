---
title: "JOB nightly-billing — spécification technique détaillée"
type: STD
status: "complet — une section en constat d'absence, un contrat non résolu"
module: billing
entry_point_type: batch
entry_point_name: "nightly-billing"
tier: 1
version: "atlas-2026.09"
generated_at: "2026-09-07"
generated_by: "sonnet — rendu depuis le graphe et 34 affirmations validées ; aucune lecture de code"
last_code_sync: "a1b2c3d"
confidence: I
unit: entrypoint
unit_ref: "JOB nightly-billing"
feeds: ["sfd/facturation.md"]
frozen_at: "2026-09-07T16:20:00Z"
---

> **Documentation générée par DMAD** · run `atlas-2026-09-07-01` · commit `a1b2c3d`
> **Document :** STD — point d'entrée `nightly-billing` (batch)
> **Dérive de :** le graphe et 34 affirmations · **Alimente :** `../sfd/facturation.md`
> **Périmètre :** feature-scan « Facturation » — 22 % du code atteint, 90 % des zones à risque
> **Confiance globale : I** (minimum des chapitres) · 12 questions ouvertes
>
> ⚠️ Cette documentation est **reconstruite depuis le code**. Chaque affirmation porte
> son niveau de preuve : **V** vérifié · **C** corroboré · **I** inféré · **H** hypothèse
> à valider.
>
> ⚠️ **Outillage partiellement dégradé :** couverture de tests disponible, aucune trace
> d'exécution. Les chemins décrits sont possibles, pas nécessairement empruntés.

## Correspondance avec le reste du corpus

| Ce document couvre | Vu en SFD |
|---|---|
| `JOB nightly-billing` | [Facturation](../sfd/facturation.md) — niveaux N2 à N0 |

---

## 1. Cartographie des composants   [C]

Le batch est câblé en trois couches : un déclencheur planifié, un service d'orchestration, et deux ports sortants.

> **Question :** quels composants ce batch mobilise-t-il, et lesquels franchissent une frontière ?
> **Confiance : C** · deux dispatchs non résolus, cf. § 14

```mermaid
flowchart LR
  SCH[Planificateur] --> RUN[BillingRun]
  RUN --> DISP[InvoiceDispatcher]
  DISP --> CALC[AmountCalculator]
  DISP --> ACC[[port AccountingGateway]]
  CALC --> PRI[[port PricingClient]]
  DISP --> DB[(invoices)]
  CALC --> DBL[(invoice_lines)]
```

`BillingRun` orchestre, `InvoiceDispatcher` décide et transmet, `AmountCalculator` valorise. Les deux ports sont les seules sorties du périmètre.

### 1.5 Cohésion et couplage des composants

| Composant / relation | Degré | Fait qui le prouve |
|---|---|---|
| `AmountCalculator` | cohésion **de fonction** ✔ | une seule responsabilité, valoriser une ligne ; prouvée par test de caractérisation (§ 15) |
| `InvoiceDispatcher` | cohésion **séquentielle** ✔ | garde, transmission, marquage d'état s'enchaînent sur le même objet (§ 5) |
| `BillingRun` | cohésion **procédurale** ~ | sélection, boucle et journalisation de campagne partagent l'ordre, pas l'objet |
| `ReinvoiceCommand` → `AccountingGateway` | couplage **de contenu** ✘ | court-circuite `InvoiceDispatcher` et ses gardes (point d'attention 3) |
| `reporting` → table `invoices` | couplage **commun** ✘ | lecture directe de la table sans passer par le module (point d'attention 4) |

Les deux `✘` sont des dettes documentées, pas des découvertes de cette table : elles renvoient à des faits établis ailleurs dans ce document.

## 2. Configuration   [V]

| Propriété | Valeur |
|---|---|
| Nom du job | `nightly-billing` |
| Déclenchement | cron `0 2 * * *` |
| Taille de lot | 200 factures |
| Politique de rejet | `skip-limit` 10, puis échec de la campagne |
| Point d'entrée | `BillingRun.execute()` |
| Contrats couverts | `ACC_INV_TRANSMIT_001` · un contrat non résolu (§ 9) |
| Paramètre déterminant | `billing.skipZeroAmount` — **défaut du dépôt `false`, production `true`** |

## 3. Architecture du flux   [C]

Trois étapes séquentielles : sélection des commandes éligibles, traitement par lot, clôture de campagne. Une seule branche conditionnelle, sur le montant nul, décrite en § 5.

## 4. Détail par étape   [C]

**Sélection** — `BillingRun.selectEligible()` `src/billing/BillingRun.java:52-78`. Retient les commandes livrées, non facturées, dont le client n'est pas en litige. Le statut de litige est lu **par commande**, pas en lot : voir le point d'attention 5.

**Traitement** — `InvoiceDispatcher.dispatch(Invoice)` `src/billing/InvoiceDispatcher.java:180-280`. Valorise, applique la garde, transmet, marque l'état.

**Clôture** — `BillingRun.close()` `src/billing/BillingRun.java:98-120`. Écrit le compte-rendu de campagne dans `billing_runs`.

## 5. Traitement unitaire   [I]

Par facture : valorisation des lignes, puis garde sur le montant nul, puis transmission.

La garde est en `src/billing/InvoiceDispatcher.java:212`. Elle n'est active que si `billing.skipZeroAmount` vaut `true` — **ce qui est le cas en production et en recette, mais pas dans la configuration par défaut du dépôt**.

Chaque facture est traitée dans sa propre transaction : l'échec de l'une n'annule pas le lot.

## 6. Séquence technique   [C]

> **Question :** dans quel ordre les composants s'appellent-ils pour une facture, et où sort-on du périmètre ?
> **Confiance : C** · une frontière non franchie

```mermaid
sequenceDiagram
  autonumber
  participant R as BillingRun
  participant D as InvoiceDispatcher
  participant C as AmountCalculator
  participant P as PricingClient
  participant A as AccountingGateway
  R->>D: dispatch(invoice)
  loop par ligne
    D->>C: compute(line)
    C->>P: barème du client
    P-->>C: barème
  end
  alt montant nul et paramètre actif
    D->>D: markSkipped()
  else
    D->>A: transmettreFacture()
    A-->>D: accusé
  end
  Note over A: comportement aval non analysé
```

## 7. Modèle de données   [V]

**Tables lues** — `orders`, `order_lines`, `customers` (colonne `dispute_status`), `pricing_scales`
**Tables écrites** — `invoices`, `invoice_lines`, `billing_runs`

Colonnes déterminantes : `invoice_lines.amount` en `DECIMAL(12,4)`, `invoices.status` en énumération à quatre valeurs, `customers.dispute_status`.

## 8. Requêtes clés   [C]

| Référence | Tables | Colonnes | Intention |
|---|---|---|---|
| `OrderRepository.java:88` | `orders`, `order_lines` | `delivered_at`, `invoiced_at` | sélection des commandes livrées non facturées |
| `CustomerRepository.java:41` | `customers` | `dispute_status` | exclusion des clients en litige — **appelée par commande, pas en lot** |

**Les requêtes de `ReportingRepository` sur `invoices` relèvent du module `reporting`, hors périmètre — ne pas les attribuer à ce batch.** C'est le piège d'attribution le plus probable ici : elles portent sur les mêmes tables.

## 9. Appels externes   [I]

| Code | Barreau | Artefact:version | Interface | Méthode | Contexte | Comportement d'échec |
|---|---|---|---|---|---|---|
| `ACC_INV_TRANSMIT_001` | 1 | `acme/atlas/accounting-api:4.7.2` | `AccountingGateway` | `POST /invoices/transmit` | une fois par facture transmise | statut `FAILED`, reprise à la campagne suivante, **cinq tentatives au maximum** |
| `SIM_XXX_XXX_XXX` | 4 | — | `PricingClient` | tarification | **une fois par ligne de commande** | non documenté — voir `OQ-024` |

Le second contrat n'est pas résolu : aucun artefact de sources dans le dépôt local, aucune Javadoc, aucun commentaire près de l'appel. Le placeholder est volontaire — un identifiant plausible se serait propagé sans qu'on puisse le contester.

**La version de l'artefact du premier compte** : le contrat décrit ce que ce module consomme en `4.7.2`, pas ce que le service comptable publie aujourd'hui.

## 10. Événements   [V]

Aucun événement émis ni consommé. Le batch est entièrement synchrone, et sa seule sortie asynchrone potentielle — la notification d'échec — passe par le même port comptable.

## 11. Mapping et transformations   [V]

Aucun mapper généré dans ce chemin. Les transformations sont manuelles dans `InvoiceAssembler.java:33-70`. Le seul mapper du module concerne l'export CSV, hors de ce point d'entrée.

## 12. Gestion des erreurs   [C]

> **Question :** que devient une facture selon l'endroit où l'exécution échoue, et ce que le support observe-t-il ?
> **Confiance : C** · aucune trace d'exécution pour confirmer les fréquences

```mermaid
flowchart TD
  E1[Échec de valorisation] --> S1[Facture non créée · lot poursuivi]
  E2[Échec de transmission] --> S2[Statut FAILED · reprise, 5 tentatives]
  E3[Échec de tarification] --> S3[Exception non déclarée · lot interrompu]
  S3 --> N[Aucune notification]
```

**Site de levée et effet observable sont distincts, et il faut les lire séparément.** Un échec de tarification est levé sur **une ligne** ; son effet observable est l'interruption de **tout le lot**, parce que l'exception n'est pas déclarée et remonte jusqu'au gestionnaire de campagne. Les confondre produirait deux affirmations contradictoires dans la SFD.

Exceptions **non déclarées** : `PricingUnavailableException` remonte sans être capturée — c'est le chemin qui interrompt le lot.
**Chemin inatteignable** : la branche `skipZeroAmount = false` n'est couverte par aucun test.

## 13. Dépendances   [V]

Non standard : `accounting-api:4.7.2`, dont la version fige le contrat du § 9.

## 14. Points d'attention pour le développeur

1. `AmountCalculator` arrondit au demi-supérieur sur quatre décimales ; l'affichage et l'export en montrent deux. Écarts possibles sur les cumuls. → `BR-FACT-021` **[V]**
2. `billing.skipZeroAmount` diffère entre le dépôt (`false`) et la production (`true`). **Un développeur qui lance le projet en local n'observe pas le comportement de production.** → `BR-FACT-014` **[I]**
3. `ReinvoiceCommand.java:47` appelle le port comptable **directement**, sans passer par le dispatcher : les gardes sont contournées. → `OQ-019`
4. `reporting` lit la table `invoices` sans passer par le module. Couplage non prévu par l'architecture. → `OQ-021`
5. Le statut de litige et le barème sont lus **à la demande dans des boucles** : environ 1 400 appels par campagne pour le premier, jusqu'à 40 par facture pour le second. Aucun lot.
6. Deux dispatchs dynamiques non résolus via `ServiceLocator.get(String)`. → `OQ-017`
7. Le contrat de tarification n'est pas résolu. → `OQ-024`

## 15. Cas de test   [V]

| Étape | Description |
|---|---|
| Pré-condition | une commande livrée, non facturée, client sans litige, une ligne à 3 unités |
| Action | exécuter `BillingRun.execute()` |
| Attendu | une facture en statut `TRANSMITTED`, montant de ligne à quatre décimales arrondi au demi-supérieur |
| Pré-condition | une facture à montant nul, `billing.skipZeroAmount` à `true` |
| Action | `InvoiceDispatcher.dispatch()` |
| Attendu | statut `SKIPPED`, aucun appel au port comptable |

Six tests de caractérisation forgés, dont `AmountCalculatorCharacterizationTest` qui promeut `BR-FACT-021` en `V`.

## 16. Références croisées

SFD associée : [Facturation](../sfd/facturation.md) · SFG : [Facturation](../sfg/facturation.md) · Objets métier : `BO-FACT-001` à `BO-FACT-003`

## 17. Historique

| Version | Date | Auteur | Description |
|---|---|---|---|
| 1.0 | 2026-09-07 | DMAD (sonnet) | Rendu initial depuis le graphe |
| 1.1 | 2026-09-07 | revue de cycle 1 | **Correction factuelle** : le § 9 annonçait une reprise indéfinie de la transmission. Elle s'arrête à cinq campagnes, dans une constante que la traversée avait manquée. Signalé par le développeur en revue. |

---

## Limites de cette analyse

- **Profondeur de traversée : 5.** 17 frontières atteintes sur l'ensemble du run.
- **Deux dispatchs dynamiques non résolus** — les implémentations réellement invoquées en production n'ont pas pu être établies. Les candidats sont enregistrés, aucun n'a été choisi.
- **Un contrat sortant non résolu** sur deux — le placeholder du § 9 est volontaire.
- **Aucune trace d'exécution.** Les chemins décrits sont possibles, pas nécessairement empruntés.
- **Modules hors périmètre :** `legacy-import`, `reporting-v1`, `admin-tools`.
