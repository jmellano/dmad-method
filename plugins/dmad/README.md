# DMAD

**Documentation Method for Agentic Discovery** — une méthode agentique pour reconstruire, depuis un code legacy, un **corpus de trois documents en cascade d'abstraction** — technique, fonctionnel détaillé, fonctionnel général — dont chaque affirmation est prouvée, datée et vérifiable.

> DMAD est le pendant inverse de [BMAD](https://github.com/bmad-code-org/BMAD-METHOD).
> BMAD descend d'une intention vers du code. DMAD remonte d'un code vers une intention.
> Ce n'est pas la même méthode dans l'autre sens : **BMAD génère, DMAD enquête.**

## Le problème

Un legacy est un système dont le comportement est connu de la machine et inconnu des humains. Les auteurs sont partis, la doc ment, plus personne n'ose toucher. Chaque évolution coûte trois fois son prix parce qu'on paie d'abord la ré-investigation.

## Le piège à éviter

Demander à un LLM de documenter un legacy produit en quelques minutes une documentation fluide, structurée, crédible — et fausse par endroits, sans qu'on sache lesquels. **Sur du legacy, une doc fausse est pire que pas de doc**, parce que l'équipe suivante la croira.

Tout DMAD est construit autour de ce risque unique. Les treize façons dont il se manifeste sont cataloguées dans [les anti-patterns](docs/10-antipatterns.md) ; chaque garde-fou de la méthode répond à l'un d'eux.

## Le corpus

```
code ──────► STD ──────► SFD ──────► SFG
             technique    fonctionnel   métier
             détaillée    détaillée     générale

             un point     un arbre de   un cas
             d'entrée     business obj. d'usage
```

Chaque document est **l'abstraction du précédent**, et **aveugle à l'étage n−2** : la SFD ne lit pas le code, la SFG ne lit ni le code ni la STD. Ce n'est pas trois rendus du même graphe — c'est une suite, et c'est ce qui garantit qu'un niveau abstrait n'est pas une seconde lecture indépendante qui divergera.

**Aucun des trois ne contient de bloc de code.** La STD porte des références ; les deux autres ignorent jusqu'à l'existence du code.

## Les quatre idées

1. **Aucune affirmation sans preuve.** Chaque phrase porte ses `evidence` : `fichier:lignes`, commit, test, migration, trace. Contrôlé mécaniquement — une claim sans preuve est refusée à l'écriture.
2. **La confiance est dérivée, pas devinée.** Échelle `V` vérifié / `C` corroboré / `I` inféré / `H` hypothèse, calculée depuis la nature de la preuve — jamais un pourcentage sorti du modèle.
3. **L'inconnu est un livrable.** Le registre des questions ouvertes est l'ordre du jour de l'atelier métier, et souvent le livrable le plus rentable du run.
4. **Un agent adversarial garde la porte.** Le `Challenger` ne rédige rien : son seul métier est de faire tomber les affirmations des autres. Seul un test de caractérisation qui passe fait monter une claim au niveau maximal.

## Le pipeline — trois cycles

```
Cycle 0   Scoper ─⛔─►
Cycle 1   Surveyor ─► Cartographer ─► Contract Resolver ─► Challenger ─► Writer:STD ─⛔─►
Cycle 2   Carver ─⛔─► Elucidator ─► Challenger ─► Test Forger ─► Writer:SFD ─⛔─►
Cycle 3   Archaeologist ─► Curator ─► Challenger ─► Writer:SFG ─⛔
```

⛔ = gate ou revue humaine. Chaque cycle est scellé par une revue qui peut demander **corrections et compléments** ; le cycle suivant ne démarre pas sur un document non figé.

**Le budget épuisé s'arrête sur un document terminé**, jamais au milieu d'un cycle. Une STD seule est un livrable qui se défend.

## Voir la méthode en action

**→ [Run de référence : Atlas ERP, capacité Facturation](examples/atlas-billing/)**

Un run complet déroulé de bout en bout : le cadrage, le découpage validé par un expert, deux claims aux régimes opposés, un challenge qui trouve deux défauts invisibles en relecture, et le corpus qui en sort — [STD](examples/atlas-billing/output/std/nightly-billing.md), [SFD](examples/atlas-billing/output/sfd/facturation.md), [SFG](examples/atlas-billing/output/sfg/facturation.md).

## Structure du dépôt

```
plugins/dmad/
├── .claude-plugin/plugin.json
├── agents/         les agents, exécutables
├── skills/         /dmad-run — l'orchestrateur — et deux prérequis embarqués
│                   (code-intelligence-java, patterns-gof-cqrs)
├── docs/           la méthode : manifeste, phases, capabilities, graphe,
│                   diagrammes, livrables, décisions, anti-patterns, profil Java
├── tasks/          20 procédures opérationnelles
├── templates/      gabarits de sortie
├── checklists/     les gates et les definitions of done
├── workflows/      full-scan et feature-scan
├── schemas/        JSON Schema — l'application mécanique des principes
├── tools/          validate.py       artefacts contre schémas
│                   check-corpus.py   documents contre invariants du corpus
│                   diagram-engine.py rend, compte, et refuse au-delà du seuil
│                   freshness.py      péremption, et sa propagation vers le haut
│                   coverage.py       les chiffres ; l'interprétation reste écrite
│                   okf-export.py     le graphe en bundle Open Knowledge Format
│                   okf-compose.py    bundle + plan → STD, SFD, SFG composées
│                   scaffold.py       les concepts à remplir, depuis le plan
│                   selftest.sh       prouve que les garde-fous mordent
└── examples/       run de référence + fixtures de violation
```

## Documentation de la méthode

| | |
|---|---|
| [01 — Manifeste](docs/01-manifeste.md) | pourquoi, 10 principes, échelle de confiance |
| [02 — Méthode](docs/02-methode.md) | le corpus, les trois cycles, les gates, les modes, le routage des modèles |
| [03 — Agents](docs/03-agents.md) | le casting, les périmètres de lecture, les plafonds |
| [04 — Capabilities](docs/04-capabilities.md) | contrats outils, dégradation, matrice agents × capabilities |
| [05 — Knowledge Graph](docs/05-knowledge-graph.md) | schéma, format des claims, séparation fait/intention |
| [06 — Diagrammes](docs/06-diagrammes.md) | les quatre diagrammes cardinaux, seuils paramétrables, règles anti-hairball |
| [07 — Livrables](docs/07-livrables.md) | les trois documents, les dix-sept sections de la STD, les artefacts qui font la différence |
| [08 — Décisions](docs/08-decisions.md) | les arbitrages, ce qui a été écarté et pourquoi — dont D15 à D22 |
| [10 — Anti-patterns](docs/10-antipatterns.md) | les 13 défaillances de la rétro-doc, et leur parade |
| [11 — Glossaire](docs/11-glossaire.md) | le vocabulaire de la méthode |
| [09 — Mettre en œuvre](docs/09-usage.md) | installation, correspondance avec Claude Code, coût, confidentialité |
| [13 — Profil Java](docs/13-profil-java.md) | où chercher quoi dans un legacy JVM, les pièges Spring/JPA/AOP |
| [14 — Couche de preuve OKF](docs/14-okf.md) | le graphe en bundle conformant, et pourquoi l'intention y devient un concept propre |
| [12 — État et suite](docs/12-roadmap.md) | ce qui existe, ce qui manque, ce que DMAD ne deviendra pas |

## Installer

### Classique — depuis le marketplace

```
/plugin marketplace add jmellano/dmad-method
/plugin install dmad@dmad-method
```

`/plugin list` doit afficher `dmad@dmad-method` en **enabled**. Puis `/dmad-run` dans le dépôt legacy.

> Le marketplace sert la **branche par défaut**. Une version en cours de développement sur une autre branche passe par le mode développement.

### Développement — itérer sur le plugin

```bash
claude --plugin-dir /chemin/vers/dmad-method/plugins/dmad
```

Puis `/reload-plugins` après chaque modification. C'est le seul mode qui ne demande pas de réinstaller à chaque changement.

### Développement — valider le packaging

Plus proche de l'installation réelle, à employer avant publication :

```
/plugin marketplace add /chemin/vers/dmad-method     # le DÉPÔT, pas le plugin
/plugin install dmad@dmad-method
```

```bash
claude plugin validate /chemin/vers/dmad-method/plugins/dmad
claude plugin validate /chemin/vers/dmad-method
```

Les deux doivent afficher `Validation passed`. Un manifeste invalide s'installe silencieusement de travers.

### Ce qu'il n'y a pas à installer

**Aucun serveur MCP** (D24). Tout le corpus voyage avec le plugin — rien à copier dans le projet analysé. Les outils sont en Python 3 et demandent `pyyaml` et `jsonschema`.

Détails, coût et confidentialité : [09 — Mettre en œuvre](docs/09-usage.md).
Projet Java ? Lis d'abord le [profil Java](docs/13-profil-java.md).

## Vérifier que les garde-fous mordent

```bash
./tools/selftest.sh          # huit sections, tout doit passer
```

Le selftest valide les schémas, vérifie que le run de référence passe, rend ses six diagrammes, propage une péremption, calcule sa couverture — et surtout vérifie que **toutes les violations connues sont refusées** : quinze sur les artefacts (claim sans preuve, auto-promotion en `V`, intention promue sans validation humaine, contrat sans version d'artefact, business object nommé d'après une méthode, SFD sans ancrage…) et treize sur les documents (bloc de code, section manquante, diagramme écrit à la main ou retouché après rendu, cas d'usage à six blocs, SFG produite malgré une contradiction non résolue…).

Un principe qui n'est pas contraint par un outil est un vœu pieux. **Et chaque message d'erreur nomme la décision qu'il applique** : un message qui ne dit pas quelle règle il fait respecter se fait contourner, puis supprimer, au premier agacement.

## Prérequis

- Une **capability `code-intelligence`** : `jcallgraph`, analyseur tree-sitter, en nominal ; la recherche textuelle en repli. **Le plafond de confiance se dérive de la question posée, pas de l'outil** (D23) — une hiérarchie de types est `V`, un appel virtuel rend des candidats en `C`, une réflexion est `I` et ouvre une question. La dégradation reste affichée dans la documentation produite.
- Accès à l'**historique git complet** (l'intention se reconstruit largement là).
- Optionnel mais décisif : **couverture, traces ou logs de production** — la seule preuve du comportement réel plutôt que possible.

## État

**v0.4 — corpus à trois documents spécifié.** Ce qui manque est le seul jalon qui compte : **un run sur un vrai legacy**. Tant qu'il n'a pas eu lieu, DMAD est une spécification cohérente — ce qui ne prouve rien. Voir [l'état et la suite](docs/12-roadmap.md).

## Filiation

[BMAD](https://github.com/bmad-code-org/BMAD-METHOD) (orchestration) · Michael Feathers, *Working Effectively with Legacy Code* (seams, characterization tests) · Adam Tornhill (hotspots, behavioral code analysis) · EventStorming « as-is » · C4 / arc42 / ADR (formats de sortie).
