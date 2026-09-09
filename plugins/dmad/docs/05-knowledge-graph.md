# DMAD — Le Knowledge Graph

## Rôle

Le graphe est **le seul état partagé** de DMAD. Les documents, les diagrammes, les tests et les questions ouvertes en sont des projections. Corriger le graphe corrige tout le reste ; corriger un document ne corrige rien.

Il porte trois strates :

```
  STRATE CORPUS        Document · Diagram              ← v0.4
        ▲  renders / anchors / derives_from
  STRATE MÉTIER        Capability · UseCase · BusinessRule · BusinessObject · Actor · Term · StateMachine
        ▲  realizes / constrains
  STRATE STRUCTURE     Module · Component · Class · Function · Entrypoint
        ▲  reads / writes / calls
  STRATE DONNÉES       DataStore · Table · Column · ExternalService · ExternalContract · Event · DataFlow
```

La strate du corpus est l'ajout de la v0.4. Elle n'existe pas pour décrire le système : elle existe pour que **la cascade soit un objet du graphe** plutôt qu'une convention de rédaction — donc vérifiable.

Les phases 1–2 remplissent le bas (mécanique, `V`). Les phases 3–4 remplissent le haut (interprétatif, `I`/`H`). **La confiance décroît en montant** — et c'est normal : c'est le prix de la remontée vers le sens.

## Types de nœuds

| Nœud | Strate | Origine | Confiance native |
|---|---|---|---|
| `Entrypoint` | structure | Surveyor | `V` |
| `Module` / `Component` | structure | Surveyor | `V` |
| `Class` / `Function` | structure | Cartographer (LSP) | `V` |
| `DataStore` / `Table` / `Column` | données | schema-intelligence | `V` |
| `ExternalService` / `ApiCall` | données | Cartographer | `V` |
| `Event` | données | Cartographer | `V` |
| `Capability` | métier | Carver | `I` → `C` après gate |
| `UseCase` | métier | Elucidator | `I` |
| `BusinessRule` | métier | Elucidator | `I` → `V` si test forgé |
| `Invariant` | métier | Elucidator | `I` |
| `StateMachine` / `State` | métier | Elucidator | `C` si champ d'état réel |
| `Actor` | métier | Elucidator | `I` |
| `Term` (glossaire) | métier | Curator | variable |
| `OpenQuestion` | transverse | tout agent | n/a |
| `Risk` / `Hotspot` | transverse | Surveyor | `V` |
| `ExternalContract` | données | Contract Resolver | dérivée du barreau : 1→`V`, 2→`C`, 3→`I` |
| `BusinessObject` | métier | Carver | `I` |
| `DataFlow` | données | Cartographer | `V` si typé par outil |
| `Diagram` | transverse | Diagram Planner | héritée de son sous-graphe |
| `Document` | transverse | rédacteurs | minimum de ses claims |

## Types d'arêtes

**Mécaniques (issues d'outils, jamais d'une lecture) :**
`calls` · `implements` · `extends` · `reads` · `writes` · `depends_on` · `exposes` · `publishes` · `consumes` · `co_changes_with`

**Interprétatives (issues d'agents) :**
`belongs_to` (structure → capacité) · `realizes` (fonction → cas d'usage) · `constrains` (règle → cas d'usage) · `explains` (intention → règle) · `contradicts` · `questions`

**De cascade (v0.4) :**
`derives_from` (document → document de l'étage inférieur) · `anchors` (section → claim ou section amont) · `renders` (document → claims qu'il publie)

Ces trois-là ne décrivent pas le système analysé : elles décrivent **le corpus lui-même**. C'est ce qui rend la cascade vérifiable — une section sans arête `anchors` est une information apparue de nulle part, et le validateur la refuse.

> **Invariant du graphe :** une arête mécanique ne peut pas être créée par un agent sans appel d'outil correspondant enregistré dans l'evidence store. C'est vérifiable automatiquement, et c'est ce qui rend l'hallucination structurelle détectable.

## Format d'une claim

```yaml
id: BR-FACT-014
type: BusinessRule
capability: facturation
statement: >
  Une facture dont le montant TTC est nul n'est pas transmise au
  système comptable ; elle est archivée avec le statut SKIPPED.
confidence: C
confidence_reason: >
  Deux preuves indépendantes et convergentes (garde dans le code +
  test existant). Non monté en V : aucun test de caractérisation
  n'a encore été forgé sur ce chemin.
evidence:
  - kind: code
    ref: src/billing/InvoiceDispatcher.java#L212-L228
    commit: a1b2c3d
    tool: lsp.find_definition
  - kind: test
    ref: src/test/billing/InvoiceDispatcherTest.java#L88
    outcome: passing
  - kind: schema
    ref: invoices.status ENUM(...,'SKIPPED')
relates_to: [UC-FACT-003, TBL-invoices]
challenged_by: CHK-2026-09-07-031
challenge_outcome: confirmed
open_questions: [OQ-012]
intent:
  statement: >
    Introduit pour éviter le rejet en masse par le SI comptable
    lors de l'import de 2019.
  confidence: H
  evidence:
    - kind: commit
      ref: 9f3e2a1
      message: "fix(billing): skip zero-amount invoices - cf INC-4471"
  validated_by: null       # ← passe en C uniquement quand un humain signe
freshness:
  verified_at_commit: a1b2c3d
  status: fresh
```

Ce format porte tout ce dont la méthode a besoin : la preuve, la raison du niveau, la trace du challenge, la séparation nette **fait / intention**, et le suivi de péremption.

## Séparation fait / intention

Point de design essentiel : une claim porte un `statement` (ce que le code fait, prouvable) **et**, séparément, un bloc `intent` (pourquoi, non prouvable). Les deux ont leur propre niveau de confiance.

Cette séparation permet au rendu de dire :

> « La facture à montant nul n'est pas transmise **[C — corroboré]**.
> *Raisonnement supposé : éviter les rejets en masse du SI comptable (incident de 2019)* **[H — à confirmer]**. »

Ce que ni un LLM libre ni un lecteur pressé ne feraient spontanément — et c'est exactement là que se logent les erreurs de documentation legacy.

## Stockage

Fichiers plats YAML versionnés dans git, un fichier par claim, indexés par un `index.json` généré.

Raisons : diffable en revue, corrigeable à la main par un expert métier, aucune infrastructure à déployer, et l'historique des corrections devient lui-même une source de connaissance. Une base graphe n'apporterait rien à cette échelle et ajouterait une dépendance à installer chez le client.
