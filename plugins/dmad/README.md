# DMAD

**Documentation Method for Agentic Discovery** — une méthode agentique pour reconstruire, depuis un code legacy, une documentation **fonctionnelle et technique** dont chaque affirmation est prouvée, datée et vérifiable.

> DMAD est le pendant inverse de [BMAD](https://github.com/bmad-code-org/BMAD-METHOD).
> BMAD descend d'une intention vers du code. DMAD remonte d'un code vers une intention.
> Ce n'est pas la même méthode dans l'autre sens : **BMAD génère, DMAD enquête.**

## Le problème

Un legacy est un système dont le comportement est connu de la machine et inconnu des humains. Les auteurs sont partis, la doc ment, plus personne n'ose toucher. Chaque évolution coûte trois fois son prix parce qu'on paie d'abord la ré-investigation.

## Le piège à éviter

Demander à un LLM de documenter un legacy produit en quelques minutes une documentation fluide, structurée, crédible — et fausse par endroits, sans qu'on sache lesquels. **Sur du legacy, une doc fausse est pire que pas de doc**, parce que l'équipe suivante la croira.

Tout DMAD est construit autour de ce risque unique. Les treize façons dont il se manifeste sont cataloguées dans [les anti-patterns](docs/10-antipatterns.md) ; chaque garde-fou de la méthode répond à l'un d'eux.

## Les quatre idées

1. **Aucune affirmation sans preuve.** Chaque phrase porte ses `evidence` : `fichier:lignes`, commit, test, migration, trace. Contrôlé mécaniquement — une claim sans preuve est refusée à l'écriture.
2. **La confiance est dérivée, pas devinée.** Échelle `V` vérifié / `C` corroboré / `I` inféré / `H` hypothèse, calculée depuis la nature de la preuve — jamais un pourcentage sorti du modèle.
3. **L'inconnu est un livrable.** Le registre des questions ouvertes est l'ordre du jour de l'atelier métier, et souvent le livrable le plus rentable du run.
4. **Un agent adversarial garde la porte.** Le `Challenger` ne rédige rien : son seul métier est de faire tomber les affirmations des autres. Seul un test de caractérisation qui passe fait monter une claim au niveau maximal.

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

⛔ = gate humain bloquant. Les trois gates (quatre en `feature-scan`) empêchent quatre heures d'agents de partir dans la mauvaise direction.

## Voir la méthode en action

**→ [Run de référence : Atlas ERP, capacité Facturation](examples/atlas-billing/)**

Un run complet déroulé de bout en bout : le cadrage, le découpage validé par un expert, deux claims aux régimes opposés, un challenge qui trouve deux défauts invisibles en relecture, et la [documentation fonctionnelle](examples/atlas-billing/output/fonctionnel/facturation.md) qui en sort.

## Structure du dépôt

```
plugins/dmad/
├── .claude-plugin/plugin.json
├── agents/         les 12 agents, exécutables
├── skills/         /dmad-run — l'orchestrateur
├── .mcp.json       Serena, Sequential Thinking, Context7
├── docs/           la méthode : manifeste, phases, capabilities, graphe,
│                   diagrammes, livrables, décisions, anti-patterns, profil Java
├── tasks/          16 procédures opérationnelles
├── templates/      gabarits de sortie
├── checklists/     les gates et les definitions of done
├── workflows/      full-scan et feature-scan
├── schemas/        JSON Schema — l'application mécanique des principes
├── tools/          validate.py, selftest.sh
└── examples/       run de référence + fixtures de violation
```

## Documentation de la méthode

| | |
|---|---|
| [01 — Manifeste](docs/01-manifeste.md) | pourquoi, 10 principes, échelle de confiance |
| [02 — Méthode](docs/02-methode.md) | les 8 phases, les gates, les modes, le routage des modèles |
| [03 — Agents](docs/03-agents.md) | le casting, les périmètres de lecture, les plafonds |
| [04 — Capabilities](docs/04-capabilities.md) | contrats outils, dégradation, matrice agents × capabilities |
| [05 — Knowledge Graph](docs/05-knowledge-graph.md) | schéma, format des claims, séparation fait/intention |
| [06 — Diagrammes](docs/06-diagrammes.md) | catalogue de 13 vues, règles anti-hairball |
| [07 — Livrables](docs/07-livrables.md) | arborescence de sortie, les trois artefacts qui font la différence |
| [08 — Décisions](docs/08-decisions.md) | 10 arbitrages, ce qui a été écarté et pourquoi |
| [10 — Anti-patterns](docs/10-antipatterns.md) | les 13 défaillances de la rétro-doc, et leur parade |
| [11 — Glossaire](docs/11-glossaire.md) | le vocabulaire de la méthode |
| [09 — Mettre en œuvre](docs/09-usage.md) | installation, correspondance avec Claude Code, coût, confidentialité |
| [13 — Profil Java](docs/13-profil-java.md) | où chercher quoi dans un legacy JVM, les pièges Spring/JPA/AOP |
| [12 — État et suite](docs/12-roadmap.md) | ce qui existe, ce qui manque, ce que DMAD ne deviendra pas |

## Installer

```
/plugin marketplace add jmellano/dmad-method
/plugin install dmad@dmad-method
```

Puis `/dmad-run` dans le dépôt legacy. Tout le corpus (méthode, tâches, schémas, templates, outils) voyage avec le plugin — rien à copier dans le projet analysé.

Détails, coût et confidentialité : [09 — Mettre en œuvre](docs/09-usage.md).
Projet Java ? Lis d'abord le [profil Java](docs/13-profil-java.md).

## Vérifier que les garde-fous mordent

```bash
python3 tools/validate.py examples/atlas-billing   # doit passer
./tools/selftest.sh                                # + les 6 violations refusées
```

Valide les schémas, vérifie que le run de référence passe, et surtout que les **cinq violations connues sont toutes refusées** : claim sans preuve, auto-promotion en `V`, intention promue sans validation humaine, règle conditionnelle énoncée sans sa condition, dépassement du plafond d'une capability dégradée.

Un principe qui n'est pas contraint par un schéma est un vœu pieux : `tools/validate.py` est le point d'application mécanique du manifeste.

## Prérequis

- Une **capability `code-intelligence`** : Serena ou un LSP natif en nominal ; tree-sitter/ctags ou grep en dégradé — avec plafond de confiance réduit et **affiché dans la documentation produite**.
- Accès à l'**historique git complet** (l'intention se reconstruit largement là).
- Optionnel mais décisif : **couverture, traces ou logs de production** — la seule preuve du comportement réel plutôt que possible.

## État

**v0.2 — méthode spécifiée et outillée.** Ce qui manque est le seul jalon qui compte : **un run sur un vrai legacy**. Tant qu'il n'a pas eu lieu, DMAD est une spécification cohérente — ce qui ne prouve rien. Voir [l'état et la suite](docs/12-roadmap.md).

## Filiation

[BMAD](https://github.com/bmad-code-org/BMAD-METHOD) (orchestration) · Michael Feathers, *Working Effectively with Legacy Code* (seams, characterization tests) · Adam Tornhill (hotspots, behavioral code analysis) · EventStorming « as-is » · C4 / arc42 / ADR (formats de sortie).
