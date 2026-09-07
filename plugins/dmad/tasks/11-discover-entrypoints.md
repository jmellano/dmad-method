# Task 11 — Découvrir les points d'entrée

**Agent :** `surveyor` · **Phase :** 1 · **Sortie :** `facts/entrypoints.json`

## Pourquoi c'est la tâche la plus importante de la phase 1
Les points d'entrée sont les **racines de toute traversée**. En rater un, c'est perdre un pan entier du métier — silencieusement, sans que rien dans la documentation finale ne le signale.

## Les huit familles

| Famille | Où chercher |
|---|---|
| **HTTP** | annotations (`@RestController`, `@RequestMapping`, `@Path`, `Route::`), fichiers de routes, `web.xml`, servlets, OpenAPI |
| **CLI / batch** | `main()`, parseurs d'arguments, scripts shell, JCL |
| **Planifié** | `@Scheduled`, crontab, quartz, `systemd timers`, ordonnanceur externe (Control-M, Rundeck) |
| **Messages** | `@KafkaListener`, `@RabbitListener`, JMS, SQS, consumers |
| **Événements** | listeners applicatifs, hooks, **triggers de base de données** |
| **Fichiers** | dépôts surveillés, imports FTP/SFTP, watchers |
| **Webhooks** | callbacks de prestataires (paiement, transporteur…) |
| **IHM serveur** | JSP/JSF/Thymeleaf avec logique, actions Struts |

## Les points d'entrée qu'on rate systématiquement

Ceux-ci méritent une recherche dédiée parce qu'ils échappent aux annotations :

- **Les triggers de base de données.** Invisibles depuis le code applicatif, et ils portent parfois des règles métier majeures. À chercher dans le DDL, pas dans le code.
- **L'ordonnanceur externe.** Un job Control-M qui appelle une classe `main()` n'apparaît nulle part dans le dépôt. Demander la configuration de l'ordonnanceur au gate 0.
- **Les procédures stockées** appelées directement par un autre système.
- **Les entrées mortes-vivantes** : une route encore exposée mais plus jamais appelée. Croiser avec les logs si disponibles — et à défaut, la déclarer *statut inconnu* plutôt que *active*.

## Sortie
```json
{
  "id": "EP-014",
  "kind": "scheduled",
  "signature": "JOB nightly-billing",
  "handler": "src/billing/BillingRun.java#L44",
  "schedule": "0 0 2 * * *",
  "evidence": { "kind": "code", "ref": "src/billing/BillingRun.java#L41", "tool": "lsp.list_symbols" },
  "reachability": "unknown"
}
```

`reachability` vaut `confirmed` (trace ou log observé), `unknown` (statique seulement) ou `suspected_dead`. **Ne jamais écrire `active` sans preuve d'exécution.**
