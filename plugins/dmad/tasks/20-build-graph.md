# Task 20 — Construire le Knowledge Graph

**Agent :** `cartographer` · **Phase :** 2 · **Sortie :** `graph/`, `boundaries.yaml`

## Principe
**On part des points d'entrée, jamais de l'arborescence.** Un dossier `utils/` de 200 fichiers ne dit rien du métier ; une route `POST /invoices/{id}/dispatch` dit tout.

## Procédure par entrypoint

1. `find_definition` du handler
2. `find_callees` **récursif**, profondeur bornée (`scope.budget.max_traversal_depth`, défaut 5)
3. À chaque nœud : tables lues/écrites (résolution ORM + requêtes littérales)
4. À chaque nœud : franchissement de frontière ? (HTTP sortant, file, disque, process, appel système)
5. **Typer chaque feuille** — voir ci-dessous
6. Arrêt et **journalisation** sur : profondeur max · frontière d'infrastructure · bibliothèque tierce · budget épuisé · dispatch non résolu

## La transitivité est un travail, pas un appel

La plupart des outils de navigation ne rendent **qu'un niveau** : les appelants directs, les appelés directs. Une liste d'appelants directs n'est pas une carte.

La remontée comme la descente se font **par itération** — appelant, puis appelants de cet appelant, et ainsi de suite jusqu'à la borne. Un nœud dont on n'a pas cherché les appelants est un nœud dont on ignore s'il est une racine, et le graphe s'en trouve amputé de ses vraies entrées.

## Une feuille non typée est une traversée inachevée

Chaque bout de branche porte sa famille :

| Famille | Ce que c'est |
|---|---|
| `database` | lecture ou écriture persistante |
| `event` | événement publié ou consommé |
| `contract` | appel sortant vers un service tiers — **le contrat est résolu en task 13**, pas ici |
| `file` | lecture ou écriture de fichier, dépôt distant |
| `notification` | courriel, message, alerte |
| `boundary` | arrêt journalisé, sans franchissement documenté |

Le typage est ce qui permet aux tables de synthèse de la STD et de la SFD d'exister. Sans lui, un appel sortant se lit comme un appel interne de plus — et disparaît des entrées-sorties du système, qui sont précisément ce que le lecteur cherche.

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

Réflexion, IoC, `eval`, dispatch par chaîne, appel via configuration : aucune analyse statique ne résout. **Ne pas deviner.** Poser un nœud dédié :

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
