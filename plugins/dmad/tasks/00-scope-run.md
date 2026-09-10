# Task 00 — Cadrer le run

**Agent :** `scoper` · **Phase :** 0 · **Sortie :** `run.yaml`, `glossary-seed.md`

## Objectif
Produire un cadrage assez précis pour qu'un run soit **utile et fini**. La majorité des runs DMAD qui coûtent cher pour rien sont des runs mal cadrés, pas des runs mal exécutés.

## Procédure

### 1. Dimensionner (avant de parler)
```
tokei / cloc                      → LOC par langage
git log --format=%ad | tail -1    → âge du projet
git shortlog -sne --since=1.year  → contributeurs actifs
git log --oneline --since=6.months | wc -l → activité
```
Deux minutes qui changent tout le reste de l'entretien : un projet de 40 kLOC actif et un projet de 900 kLOC dormant n'appellent pas les mêmes questions.

### 2. La question de sortie
> « Dans trois semaines, qu'est-ce que vous devez pouvoir faire que vous ne pouvez pas faire aujourd'hui ? »

| Réponse | `objective.kind` | Ce que ça priorise |
|---|---|---|
| « faire évoluer X » | `evolve` | règles de gestion de X, seams, tests de caractérisation |
| « reprendre la maintenance » | `maintain` | entrypoints, architecture, dette |
| « décider si on refond » | `decide_refactor` | hotspots, couplages, dépendances externes |
| « passer un audit » | `audit` | traçabilité, couverture, règles réglementaires |
| « intégrer des nouveaux » | `onboard` | vue d'ensemble, parcours nominaux |
| « migrer vers Y » | `migrate` | frontières, intégrations, modèle de données |

Si aucune réponse ne vient : **ne pas lancer le run**. Proposer de commencer par un `full-scan` très léger (phases 0–2 uniquement) pour donner de la matière à la discussion.

### 3. Choisir le mode
`feature-scan` si : > 150 kLOC, **ou** l'objectif nomme un domaine, **ou** le budget est serré.
`full-scan` sinon.

### 4. Borner le périmètre
Chaque exclusion se justifie par écrit. Les exclusions typiques :
- généré (`target/`, `dist/`, stubs, protos compilés)
- vendored / dépendances
- modules morts — **à vérifier**, pas à supposer : `git log --since=2.years -- <path>` et recherche d'appels entrants
- domaines hors sujet

### 5. Collecter le vocabulaire (critique en feature-scan)
> « Donnez-moi les mots que vous utilisez en réunion. Pas les termes techniques : les vôtres. »

Viser 5 à 20 termes. Pour chacun, demander les **variantes et l'abréviation maison** — dans un legacy, « avoir » peut s'appeler `cn`, `credit_note` ou `AVR` selon la couche.

### 6. Inventorier les sources non-code
Historique git complet ou tronqué (`git log --oneline | wc -l` vs âge). Tickets accessibles ? Wiki ? ADR ? **Et surtout : qui est encore là, et sur quel domaine.**

### 7. Trancher la confidentialité
Avant le premier appel d'outil. Ce qui peut sortir de la machine, ce qui reste local, ce qui doit être caviardé.

### 8. Annoncer le budget et les plafonds
Ordre de grandeur en temps et en coût, **et** les plafonds de confiance induits par l'outillage disponible. Le plafond se dérive de la question posée (D23) : dire au commanditaire que les appels dynamiques ressortiront en candidats plutôt qu'en certitudes, c'est ce qui évite qu'il le découvre à la livraison.

## Modes d'échec
| Symptôme | Cause | Correctif |
|---|---|---|
| Le run dérive et ne finit pas | périmètre non borné | re-cadrer, ne pas « juste continuer » |
| La doc ne sert à personne | pas d'objectif de sortie | gate 0 refusé trop tôt |
| Feature-scan aveugle | vocabulaire absent ou technique | redemander au métier, pas au dev |
| Surprise à la livraison | plafonds non annoncés | les dire au gate 0 |
