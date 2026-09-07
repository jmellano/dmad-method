# Task 20 — Construire le Knowledge Graph

**Agent :** `cartographer` · **Phase :** 2 · **Sortie :** `graph/`, `boundaries.yaml`

## Principe
**On part des points d'entrée, jamais de l'arborescence.** Un dossier `utils/` de 200 fichiers ne dit rien du métier ; une route `POST /invoices/{id}/dispatch` dit tout.

## Procédure par entrypoint

1. `find_definition` du handler
2. `find_callees` récursif, profondeur bornée (`scope.budget.max_traversal_depth`, défaut 5)
3. À chaque nœud : tables lues/écrites (résolution ORM + requêtes littérales)
4. À chaque nœud : franchissement de frontière ? (HTTP sortant, file, disque, process, appel système)
5. Arrêt et **journalisation** sur : profondeur max · frontière d'infrastructure · bibliothèque tierce · budget épuisé · dispatch non résolu

## L'invariant

```
∀ arête mécanique e : ∃ evidence(e).tool
```

Vérifié par `*verifier`. Une arête sans trace d'outil est **supprimée** et convertie en question ouverte. C'est ce qui rend l'hallucination structurelle détectable au lieu d'être une affaire de confiance envers le modèle.

## Journal des frontières

Chaque arrêt est enregistré, pas subi :

```yaml
boundary_hit:
  from: "src/billing/InvoiceDispatcher.java#L212"
  reason: infra              # depth_limit | infra | third_party | budget | unresolved_dynamic
  target: "com.acme.accounting.Client.send()"
  impact: "les règles appliquées côté SI comptable ne sont pas documentées"
  suggests_open_question: true
```

Ce journal alimente le rapport de couverture et la page « zones d'ombre ». **Une traversée s'arrête toujours quelque part ; ce qui distingue une bonne carte, c'est qu'elle dessine ses propres bords.**

## Le dispatch dynamique

Réflexion, IoC, `eval`, dispatch par chaîne, appel via configuration : le LSP ne résout pas. **Ne pas deviner.** Poser un nœud dédié :

```yaml
unresolved_dispatch:
  at: "src/core/ServiceLocator.java#L88"
  expression: "get(String beanName)"
  candidates:                      # par nom ou par interface implémentée
    - "BillingService"
    - "LegacyBillingService"
  resolution: unknown
  open_question: OQ-017
```

Fréquent et central dans les legacy à conteneur IoC. Le traiter explicitement évite qu'un modèle en aval choisisse silencieusement un candidat et bâtisse trois pages dessus.

## Nommage
Le LLM intervient uniquement pour **nommer et regrouper** — jamais pour créer une arête. Les regroupements qu'il propose sont plafonnés à `I` ; les arêtes issues d'outils sont en `V`.
