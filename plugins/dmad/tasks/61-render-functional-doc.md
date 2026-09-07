# Task 61 — Rendre la documentation fonctionnelle

**Agent :** `writer-functional` · **Phase :** 6

## Contrainte fondatrice
**Le rédacteur n'a pas accès au code.** Il ne dispose que des claims validées, du glossaire et des diagrammes. Si l'information n'est pas dans une claim, elle n'existe pas.

Cette contrainte est ce qui garantit que **toute phrase publiée a franchi la chaîne de preuve**. Un rédacteur avec le code sous les yeux comblerait les trous par sa propre lecture — laquelle n'aurait traversé ni le Challenger ni les tests.

## Traduction obligatoire

| Code | Documentation fonctionnelle |
|---|---|
| `invoice.status = SKIPPED` | « la facture est archivée sans être transmise » |
| `BillingRun` | « la campagne de facturation » |
| `dispatch()` | « la transmission au service comptable » |
| `InsufficientFundsException` | « le paiement est refusé pour provision insuffisante » |

Interdits : noms de classes, de méthodes, de tables, de fichiers ; « le système appelle » ; références aux frameworks.

## Gradation de la langue selon la confiance

| Niveau | Formulation imposée |
|---|---|
| `V` | « Le système transmet… » |
| `C` | « Le système transmet… » + badge |
| `I` | « D'après l'analyse du code, le système transmettrait… » |
| `H` | « **Hypothèse à confirmer :** cette règle viendrait de… » |

C'est cette gradation qui fait qu'un lecteur pressé, qui ne regarde pas les badges, perçoit quand même l'incertitude. Un badge seul est invisible en lecture rapide ; une formulation conditionnelle ne l'est pas.

## Structure d'un chapitre

```
# <Capacité>   [badge · N affirmations · M à confirmer]
## En une phrase
## Ce que fait le système          ← cas d'usage
## Les règles appliquées           ← une règle = un paragraphe + niveau
## Le parcours                     ← diagrammes, chacun avec sa question
## Les données manipulées          ← ERD traduit
## ⚠️ À confirmer par le métier    ← questions priorisées
## Ce qui n'a pas été analysé      ← frontières atteintes
```

Les deux dernières sections ne sont **jamais omises**, même vides — auquel cas elles affichent « aucune » explicitement. Une section absente se lit comme « rien à signaler » ; une section vide et assumée se lit comme « on a regardé ».

## Quand tu rencontres un trou

Tu ne combles pas, tu ne devines pas : tu émets une `gap_request` (cf. `docs/03-agents.md`).

- `severity: blocking` → relance ciblée de l'Elucidator sur ce point, puis du Challenger
- `severity: degrades` → question ouverte + mention dans « ce qui n'a pas été analysé ». **Le document sort avec son trou visible**, et c'est l'issue voulue.

## Contrôle final
`*verifier` : chaque phrase affirmative doit être traçable à une claim. Une phrase sans claim source est supprimée, pas signalée.
