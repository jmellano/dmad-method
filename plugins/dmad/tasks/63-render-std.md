# Task 63 — Rendre la STD

**Agent :** `writer-std` · **Cycle :** 1 · **Sortie :** `dmad-output/std/<point-d-entree>.md`

## Les deux contraintes

**Pas d'accès au code.** Le graphe et les claims, rien d'autre.

**Aucun bloc de code, aucune requête, aucune configuration.** Des **références** : `fichier:lignes`, signatures, noms de tables et de colonnes (D16). C'est la conformité ISO 25010, et c'est ce qui rend la première contrainte tenable — tant qu'un extrait est permis, aller lire le code a un motif légitime.

## Un document par point d'entrée

C'est l'unité que cherche le lecteur : il ouvre la STD parce qu'il doit modifier un batch, une route, un consumer. Le frontmatter porte `entry_point_type` et `entry_point_name`.

## Les dix-sept sections

Grille complète : `${CLAUDE_PLUGIN_ROOT}/docs/07-livrables.md`. Gabarit : `${CLAUDE_PLUGIN_ROOT}/templates/std.md`.

## Ne jamais omettre une section

Une section dont le sujet n'existe pas se remplit avec le constat d'absence **et son périmètre** :

| Situation | ❌ | ✅ |
|---|---|---|
| Aucune requête native | supprimer la section | « Aucune requête annotée dans ce chemin. Trois mécanismes d'accès : dérivation par nom, API de critères, sauvegarde en lot. **Les requêtes de `XJpaRepository` l.44-91 relèvent du flux Y — ne pas les attribuer ici.** » |
| Aucun mapper | supprimer la section | « Aucun mapper généré dans ce chemin. Les transformations sont manuelles dans `<méthodes>`. Le seul mapper du module concerne Z, hors périmètre. » |
| Aucun événement | supprimer la section | « Point d'entrée synchrone, aucun événement émis ni consommé. » |

**Le plus grand gain est le piège d'attribution** : signaler les artefacts *voisins* qui ressemblent à ce que le lecteur cherche mais n'appartiennent pas au périmètre. C'est ce qui évite qu'un développeur optimise une requête que ce batch n'exécute jamais.

## Section 1.5 — cohésion et couplage

Clôt la cartographie des composants. Table ordonnée du plus fort — cohésion de fonction — au plus faible — cohésion accidentelle, puis une seconde table pour les couplages problématiques.

```markdown
| Composant / relation | Degré | Fait qui le prouve |
|---|---|---|
| `AbstractDocumentStrategy` | cohésion **de fonction** ✔ | Template Method à 5 hooks ordonnés (§ 3.2.3) |
| Les 3 hooks sans appelant | cohésion **accidentelle** ✘ | 10 implémentations, zéro site d'appel (point d'attention 22) |
```

**Chaque ligne cite un fait déjà documenté ailleurs.** Cette table rassemble sous le critère, elle ne redécouvre pas. Si le fait est introuvable ailleurs, soit il manque, soit la qualification est faible — dans les deux cas, ne pas l'inventer.

C'est un excellent catalyseur de revue : un lead technique la parcourt en trente secondes pour arbitrer une passe de nettoyage.

## Section 9 — appels externes

Une ligne par contrat : `Code | Barreau | Artefact:version | Interface | Méthode | Contexte | Comportement d'échec`.

Un contrat au barreau 3 se présente comme tel. Un contrat non résolu porte son placeholder et figure dans les points d'attention.

## Section « limites de l'analyse » — obligatoire

Profondeur de traversée, frontières atteintes, dispatchs non résolus, absence de traces runtime, modules hors périmètre. C'est ce qui distingue une documentation professionnelle d'une génération automatique.

## Table de correspondance

En tête : quelle SFD couvre ce point d'entrée, et sur quels niveaux. Le lecteur doit pouvoir passer d'une unité documentaire à l'autre.

## Quand il manque quelque chose

Une `gap_request`, jamais un comblement. `blocking` relance la cartographie ou la résolution des contrats sur ce point ; `degrades` devient une question ouverte et le document sort avec son trou visible.
