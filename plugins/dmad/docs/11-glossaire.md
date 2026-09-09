# DMAD — Glossaire de la méthode

Le vocabulaire propre à DMAD. Utile pour lire les documents, et pour éviter que « claim », « capacité » ou « preuve » ne dérivent d'un usage à l'autre.

## Les objets

**Claim** — Une affirmation produite par DMAD, avec ses preuves, son niveau de confiance et sa traçabilité. L'unité atomique de la méthode : tout ce qui est publié est une claim rendue. Une phrase sans claim source n'existe pas.

**Evidence (preuve)** — Ce qui fonde une claim : lignes de code, test, contrainte de schéma, migration, commit, ticket, trace runtime, configuration. Peut être **négative** (`kind: absence`) : « aucun test associé » est une information qui pèse.

**Intent (intention)** — Le *pourquoi* d'une règle. Champ séparé du `statement`, avec son propre niveau de confiance, plafonné à `H` tant qu'un humain ne l'a pas validé. Le code ne dit jamais pourquoi.

**Capacité** — Un regroupement métier cohérent (Facturation, Recouvrement, Gestion des droits). Proposé par le Carver, validé par un humain au gate 3. **L'unité d'organisation de toute la documentation.**

**Business object** — Un nœud d'orchestration qui conjugue plusieurs feuilles externes ou plusieurs sous-objets. Nommé par son **sens fonctionnel**, jamais par la méthode dont il est issu, et porteur de deux étiquettes : sa profondeur récursive dans l'arbre et sa couche métier. C'est l'ossature de la SFD.

**Contrat sortant** — Un appel vers un service tiers, identifié par un code lu dans l'artefact de la dépendance. Feuille du graphe au même titre qu'un accès base ou un événement. Porte obligatoirement la **version de l'artefact** où il a été lu : le contrat décrit ce que le module consomme, pas ce que le module appelé publie aujourd'hui.

**Barreau de résolution** — Le niveau de fiabilité de la source d'où vient un code de contrat, de 1 (l'annotation, qui fait foi) à 4 (le placeholder). Un code faux ressemble exactement à un code vrai : écrire le barreau est ce qui rend la différence visible.

**Cascade** — La chaîne STD → SFD → SFG, où chaque document est l'abstraction du précédent et **aveugle à l'étage n−2**. Ce n'est pas trois rendus du même graphe : c'est une suite.

**Cycle** — L'unité de production d'un document : enquête, challenge, rédaction, puis revue humaine qui fige. Trois cycles, plus le cadrage. Le budget épuisé s'arrête sur un cycle terminé.

**Longueur et profondeur** — Les deux leviers de décomposition. La longueur est la séquence d'opérations d'un niveau ; la profondeur est l'empilement des niveaux. Ils ne se substituent pas : ils s'ajustent en tension, et c'est la contrainte de lisibilité qui arbitre.

**Seam** — Un point où le comportement peut être modifié sans réécrire le code autour. Terme repris de Michael Feathers. C'est la sortie actionnable de DMAD : documenter pour rendre l'évolution possible.

**Hotspot** — Un fichier à fort `churn × complexité`. Terme repris d'Adam Tornhill. Détermine l'ordre de travail : on documente d'abord ce qui bouge et fait mal.

**Question ouverte** — Ce que le code ne peut pas trancher, formulé comme une question à un humain. Livrable de première classe, pas un aveu d'échec.

**Frontière (boundary)** — Un point où la traversée s'est arrêtée : limite de profondeur, infrastructure, bibliothèque tierce, budget, dispatch non résolu. Journalisée systématiquement. *Une carte qui dessine ses propres bords.*

## Les niveaux de confiance

| | Nom | Ce qui le justifie |
|---|---|---|
| **V** | Vérifié | fait mécanique (analyse syntaxique, schéma) ou test exécuté ou observation runtime |
| **C** | Corroboré | ≥ 2 preuves indépendantes convergentes |
| **I** | Inféré | lecture du code par le modèle, source unique |
| **H** | Hypothèse | intention métier, non prouvable par le code |

**Plafond (ceiling)** — Niveau maximum atteignable. Imposé soit par l'agent producteur (l'Archaeologist plafonne à `H`), soit par une capability dégradée (naviguer au `grep` plafonne à `I`).

**Promotion** — Montée d'un niveau. **Seul le Test Forger peut promouvoir**, et uniquement sur test vert. Pour une intention, seule une validation humaine tracée le peut.

**Dégradation** — Descente d'un niveau, prononcée par le Challenger ou le Curator. Toujours motivée et journalisée.

## Les mécanismes

**Capability** — Un contrat d'outillage (`code-intelligence`, `repo-history`…) avec plusieurs implémentations interchangeables. Les agents consomment des capabilities, jamais des outils.

**Gate** — Un point de validation humaine bloquant. Trois en `full-scan`, quatre en `feature-scan`. Un gate n'est pas une revue : c'est **une décision précise demandée à la bonne personne**.

**Challenge** — L'attaque adversariale d'une claim selon 9 angles. Ne produit jamais de documentation, uniquement des réfutations.

**Test de caractérisation** — Un test qui capture le comportement actuel, y compris absurde. Dans DMAD, c'est la **preuve exécutable** de la documentation : le seul mécanisme atteignant le niveau `V`.

**Sonde** — L'un des cinq moyens indépendants de localiser une fonctionnalité (vocabulaire, données, historique, tests, surface externe). C'est leur convergence qui fait le signal.

**Fraîcheur (freshness)** — L'état d'une claim vis-à-vis du code actuel : `fresh`, `shifted`, `stale`, `broken`. Ce qui empêche la documentation d'être une photo qui jaunit.

**Couverture** — La fraction du code réellement atteinte par l'analyse. La seule métrique honnête et calculable de la méthode — par opposition à un pourcentage de confiance, qui serait une opinion déguisée en chiffre.

## Les trois documents

**STD** — Spécification technique détaillée. Un document **par point d'entrée**. Lit le graphe et les claims. Porte des références au code, jamais de code.

**SFD** — Spécification fonctionnelle détaillée. Un document **par arbre de business objects**, en vue récursive. Lit la STD figée et les claims.

**SFG** — Spécification fonctionnelle générale. Un document **par domaine, découpé par cas d'usage**. Lit la SFD figée, et rien d'autre. Son apport propre est l'**intention** — la seule information du corpus qu'aucune relecture de code ne produira.

## Les modes

**`full-scan`** — Tout le périmètre. Défaut en dessous de ~150 kLOC.

**`feature-scan`** — Une fonctionnalité, localisée depuis un vocabulaire métier. Défaut au-delà, ou dès que l'objectif nomme un domaine. Ajoute un gate de localisation.

## Faux amis

**Capability** a deux sens dans le projet, et c'est le seul homonyme assumé :
- une **capacité métier** (`Capability` dans le graphe, Facturation, Recouvrement)
- une **capability d'outillage** (`code-intelligence`, contrat technique)

Le contexte lève l'ambiguïté sans peine, mais mieux vaut le savoir. En français, on dit « capacité » pour le métier et « capability » pour l'outillage.

**Claim** n'est pas « affirmation vraie ». C'est « affirmation avec son niveau de preuve ». Une claim en `I` est publiée, au conditionnel.

**Preuve** n'est pas « démonstration ». Une `evidence` de type `code` est un pointeur vers ce qui fonde l'affirmation, pas une garantie de vérité — c'est précisément pour cela que le Challenger existe.
