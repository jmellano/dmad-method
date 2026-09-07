# DMAD

**Documentation Method for Agentic Discovery** — une méthode agentique pour reconstruire, depuis un code legacy, une documentation **fonctionnelle et technique** dont chaque affirmation est prouvée, datée et vérifiable.

> Le pendant inverse de [BMAD](https://github.com/bmad-code-org/BMAD-METHOD).
> BMAD descend d'une intention vers du code. DMAD remonte d'un code vers une intention.
> Ce n'est pas la même méthode dans l'autre sens : **BMAD génère, DMAD enquête.**

## Installation

```
/plugin marketplace add jmellano/dmad-method
/plugin install dmad@dmad-method
```

Puis, dans le dépôt legacy à documenter :

```
/dmad-run
```

## Le problème

Un legacy est un système dont le comportement est connu de la machine et inconnu des humains. Les auteurs sont partis, la doc ment, plus personne n'ose toucher. Chaque évolution coûte trois fois son prix parce qu'on paie d'abord la ré-investigation.

## Le piège que DMAD existe pour éviter

Demander à un LLM de documenter un legacy produit en quelques minutes une documentation fluide, structurée, crédible — et fausse par endroits, **sans qu'on sache lesquels**.

Sur du legacy, une documentation fausse est **pire que pas de documentation** : l'équipe suivante la croit, décide sur cette base, et découvre l'erreur en production.

Toute la méthode est construite autour de ce risque unique. Les [13 façons dont il se manifeste](plugins/dmad/docs/10-antipatterns.md) sont cataloguées, et chaque contrainte de DMAD répond à l'une d'elles.

## Les quatre idées

1. **Aucune affirmation sans preuve.** Chaque phrase porte ses `evidence` : `fichier:lignes`, commit, test, migration. Contraint par schéma — une claim sans preuve est refusée à l'écriture, pas signalée en relecture.
2. **La confiance est dérivée, pas devinée.** Échelle `V` vérifié / `C` corroboré / `I` inféré / `H` hypothèse, calculée depuis la **nature de la preuve** — jamais un pourcentage sorti du modèle.
3. **L'inconnu est un livrable.** Le registre des questions ouvertes est l'ordre du jour de l'atelier métier, et souvent le livrable le plus rentable du run.
4. **Un agent adversarial garde la porte.** Le Challenger ne rédige rien : son seul métier est de faire tomber les affirmations des autres. Seul un test de caractérisation qui passe fait monter une claim au niveau maximal.

## Le pipeline

```
Scoper ─⛔─► Surveyor ─► Cartographer ─► Carver ─⛔─► Elucidator ─┐
 cadrage    inventaire     graphe       capacités  cas d'usage   │
                                                  Archaeologist ─┤
                                                     intention   ▼
                                                             Challenger
                                                             Test Forger
                                                                  │
                                                                 ⛔
                                                                  ▼
                                    Diagram Planner ─► Writers ─► Curator
```

⛔ = gate humain bloquant. Trois gates (quatre en `feature-scan`) empêchent quatre heures d'agents de partir dans la mauvaise direction.

## Voir la méthode en action

**→ [Run de référence : Atlas ERP, capacité Facturation](plugins/dmad/examples/atlas-billing/)**

Un run complet déroulé de bout en bout, où le Challenger trouve deux défauts qu'aucune relecture n'aurait vus : un feature flag actif en production mais inactif par défaut dans le dépôt (documentation vraie en recette, fausse ailleurs), et un « n'est jamais transmise » faux sur le troisième appelant.

## Documentation

Tout est dans [`plugins/dmad/docs/`](plugins/dmad/docs/) — commencer par le [manifeste](plugins/dmad/docs/01-manifeste.md), ou par les [anti-patterns](plugins/dmad/docs/10-antipatterns.md) pour juger si la méthode tient.

Projet Java ? → [profil Java](plugins/dmad/docs/13-profil-java.md).

## Prérequis

- **[Serena](https://github.com/oraios/serena)** (ou un LSP natif) pour la navigation sémantique. Sans lui, DMAD fonctionne en mode dégradé — **et le plafond de confiance du run baisse et s'affiche** dans la documentation produite.
- Accès à l'**historique git complet** : l'intention se reconstruit largement là.
- Optionnel mais décisif : **couverture, traces ou logs de production** — la seule preuve du comportement *réel* plutôt que *possible*.

## État

**v0.3 — méthode spécifiée, outillée et packagée.** Ce qui manque est le seul jalon qui compte : **un run sur un vrai legacy**. Tant qu'il n'a pas eu lieu, DMAD est une spécification cohérente — ce qui ne prouve rien. Voir [l'état et la suite](plugins/dmad/docs/12-roadmap.md).

## Filiation

[BMAD](https://github.com/bmad-code-org/BMAD-METHOD) (orchestration) · Michael Feathers, *Working Effectively with Legacy Code* (seams, characterization tests) · Adam Tornhill (hotspots, behavioral code analysis) · EventStorming « as-is » · C4 / arc42 / ADR.

## Licence

MIT
