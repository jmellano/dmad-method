# DMAD — État des lieux

> Rédigé le 2026-09-10, après la refonte v0.4 et le premier run réel.
> Ce document dit **où en est le plugin**, **ce qui a été fait**, **ce que le terrain a appris**, et **ce qu'il reste**. Il est écrit pour être lu dans six mois par quelqu'un qui reprend le sujet.

---

# 1. Niveau de maturité

## L'échelle

| Niveau | Ce qu'il signifie |
|---|---|
| 1 — Idée | l'intention est formulée |
| 2 — Spécifiée | la méthode tient sur le papier, ses arbitrages sont écrits |
| 3 — **Outillée** | les principes sont **contraints par des outils**, avec non-régression |
| 4 — Éprouvée | un run réel complet, mesuré, dont on tire des corrections |
| 5 — Reproductible | plusieurs runs, plusieurs opérateurs, coût prévisible |

## Où se situe DMAD

**Niveau 3 solide, avec environ un tiers du niveau 4.**

| Dimension | Niveau | Sur quoi ça repose |
|---|---|---|
| Spécification de la méthode | **4/5** | 28 décisions écrites, cohérentes, et **auto-corrigées** : D4 révisée par D23, D20 par D25. Une méthode qui se contredit et le dit vaut mieux qu'une méthode qui n'a jamais été confrontée. |
| Contrainte mécanique | **3,5/5** | 9 outils, 2 250 lignes, 10 sections de selftest, 31 fixtures de non-régression. **Mais ces outils contrôlent la forme, jamais la vérité.** |
| Épreuve terrain | **1/5** | Un run partiel : cycles 0 et 1 seulement, un batch, un dépôt, une architecture depuis remplacée. |
| Reproductibilité | **0/5** | Un opérateur, une fois, avec beaucoup d'intervention manuelle et trois reprises. |
| Modèle de coût | **0,5/5** | Un point de mesure — 432 000 jetons pour une cartographie jetée deux fois, 227 000 pour un challenge qui a tout trouvé — et aucune ligne de base. |
| Distribution | **3/5** | Packagé, `claude plugin validate` passe, procédures d'installation écrites. Jamais installé par quelqu'un d'autre. |

## Le point inconfortable, et il est central

**Le selftest est vert contre une fixture que j'ai écrite pour qu'elle le soit.**

Les 31 fixtures de violation ont une vraie valeur : elles prouvent que les garde-fous **refusent** ce qu'ils doivent refuser, et chacune correspond à un mode de défaillance observé ou raisonné. Mais la section « le run de référence passe » est circulaire : le run de référence est fictif, je l'ai rédigé, et je l'ai rédigé conforme.

C'est exactement le motif que le retour du premier run réel désigne comme le constat qui domine tous les autres — *« les agents rapportent des succès qu'ils n'ont pas vérifiés »* — appliqué un cran au-dessus. La vérification faite par le producteur ne vaut pas contrôle, et j'en suis le producteur.

**Conséquence pratique : tout ce qui a été construit dans la refonte v0.4 — la cascade STD → SFD → SFG, l'inversion bundle-d'abord, les plans, la nouvelle arborescence, les concepts — n'a jamais rencontré de code réel.** Le seul run réel s'est arrêté au cycle 1 et tournait sur l'architecture d'avant. Ce sur quoi le plus d'effort a été dépensé est ce qui est le moins prouvé.

## Ce qu'il faut pour passer au niveau 4

Un run complet — cycles 0 à 3 — sur un vrai processus, avec l'architecture actuelle, produisant les trois documents. Trois chiffres en sortent : le coût réel par cycle, le taux de findings du Challenger, et la justesse mesurée par échantillonnage de cinq claims.

Le second run annoncé sur `controle-facture-backend` est ce jalon. **Son intérêt principal n'est pas le document produit : c'est l'écart avec le premier.**

---

# 2. Ce qui a été fait

## Le point de départ

DMAD v0.3 : une méthode d'enquête aboutie — chaîne de preuve, échelle `V/C/I/H` dérivée, agent adversarial, gates humains — mais dont la **restitution était sous-spécifiée** (une arborescence et un bandeau), et dont les principes reposaient sur des consignes plus que sur des contrôles.

À côté, le corpus `skills-doc` : une doctrine de rédaction éprouvée sur des livrables réels, mais sans machinerie d'enquête.

## Les décisions structurantes, D15 à D28

| | Décision | Ce qu'elle change |
|---|---|---|
| **D15** | seuils de lisibilité paramétrables, défauts N ≤ 12 · E ≤ 15 · McCabe ≤ 10 | le nombre de niveaux d'abstraction devient un **résultat** de la contrainte, pas un choix |
| **D16** | aucun bloc de code ni de SQL dans le corpus | supprime le motif d'aller lire le code, donc rend D3 tenable |
| **D17** | échelle de lecture en cascade, chaque étage aveugle à n−2 | garantit que chaque niveau est une **abstraction**, pas une seconde lecture |
| **D18** | un contrat sortant est une feuille du graphe, **versionnée** | sans la version, la preuve devient fausse au prochain bump, en silence |
| **D19** | trois cycles emboîtés, chacun scellé par une revue humaine | chaque étage devient livrable seul |
| **D20/D25** | trois unités documentaires ; STD et SFD documentent un **processus** | corrigé par le terrain : un processus a rarement un seul point d'entrée |
| **D21** | le gate 3 migre en tête du cycle 2 | il se tient devant un expert qui vient de lire la carte technique |
| **D22/D28** | le modèle d'abord, puis une **seule représentation** | les agents écrivent des concepts ; `dmad-output` **est** le bundle |
| **D23** | le plafond de confiance se dérive de **la question**, pas de l'outil | P3 appliqué jusqu'au bout, par arête du graphe |
| **D24** | aucune dépendance à un serveur MCP | rien à installer, rien à diagnostiquer ; `doc-retrieval` devient optionnelle et le dit |
| **D26** | le bundle est la sortie primaire, le document en dérive | un concept est réutilisable, une section ne l'est pas |
| **D27** | l'arborescence est ordonnée par **sujet** | un chemin doit dire de quoi parle le fichier avant qu'on l'ouvre |

## Les outils, et ce qu'ils refusent

Neuf outils, 2 250 lignes de Python sans dépendance autre que `pyyaml` et `jsonschema`.

| Outil | Ce qu'il refuse |
|---|---|
| `validate.py` | claim sans preuve · auto-promotion en `V` · intention promue sans validation humaine tracée · contrat sans version d'artefact ou dont la confiance ne dérive pas du barreau · business object nommé d'après une méthode · **plage de lignes qui déborde du fichier** · **fichier non-concept dans un dossier routé** · **code dans une note** |
| `check-corpus.py` | bloc de code dans un document · plan de niveau 1 altéré · section imposée absente · diagramme sans question, sans marqueur de rendu, ou retouché après rendu · cas d'usage à moins de sept blocs · frontière vide · règle sans traçabilité · index inverse incohérent · notation sans légende · compteur faux · marqueur de gabarit résiduel |
| `okf-compose.py` | concept du plan introuvable · **concept du bundle absent du plan** · saut de niveau de titre · lien ou ancre morts |
| `okf-index.py` | concept sans `type` · orphelin · lien mort |
| `diagram-engine.py` | diagramme au-delà du seuil — **il découpe, il ne simplifie pas** |
| `freshness.py` | ce qui a péri, **et le propage vers le haut de la cascade** |
| `coverage.py`, `scaffold.py`, `selftest.sh` | — |

**Chaque message d'erreur nomme la décision qu'il applique.** Un message qui ne dit pas quelle règle il fait respecter se fait contourner, puis supprimer, au premier agacement.

## Le corpus produit

Trois documents en cascade d'abstraction, composés depuis le bundle :

```
code ──► STD ──► SFD ──► SFG
         11 chap.  10 chap.  6 chap.
         processus processus domaine, par cas d'usage
```

Plans repris des gabarits FEF, éprouvés sur un corpus réel. Le run de référence porte 68 concepts et valide contre le **validateur OKF officiel en mode strict** : 0 erreur, 0 avertissement, 0 lien mort, 0 orphelin.

---

# 3. L'intégration du corpus `skills-doc` — avis honnête

## Ce qui a réellement transféré

**Tout ce qui pouvait devenir un contrôle mécanique.** Les seuils de complexité sont comptés par le moteur de diagrammes, qui refuse au-delà. Le nommage des business objects par le sens fonctionnel est refusé s'il ressemble à un identifiant de code. Les sept blocs d'un cas d'usage, la frontière non vide, l'index inverse cohérent, l'absence de code dans le corpus : tous contrôlés.

**Et une chose que le terrain a validée** : l'échelle à quatre barreaux de résolution des contrats. C'est le seul élément du corpus `skills-doc` dont un run réel ait prouvé qu'il transfère — le `Contract Resolver` a été désigné comme « le mieux calibré » du run, a plafonné treize contrats à `I` parce que résolus par commentaire manuscrit, et a produit **un placeholder assumé** là où la documentation du dépôt proposait un code plausible. C'est exactement ce que le principe demande.

## Ce qui n'est resté que de la prose

Quatre éléments, tous des **actes de jugement**, vivent dans des prompts d'agents et n'ont jamais été exercés sur du code réel :

- la classification ISO 25010 — traitement contre contrôle, données initiales contre ad-hoc, sorties normales contre anormales ;
- l'arbitrage entre longueur et profondeur ;
- la reconnaissance des patrons de conception, et la règle de les taire ;
- « analyser bas → haut, rédiger haut → bas ».

**Le premier run réel a montré que le prompt ne tient pas.** Trois règles écrites en toutes lettres, parfois en gras, parfois avec leur pourquoi, ont été enfreintes par le même agent sur une tâche longue. Il n'y a aucune raison de penser que ces quatre-là tiendront mieux.

C'est l'asymétrie centrale de l'intégration : **ce qui est devenu machine tient, ce qui est resté texte est à prouver.**

## Ce qu'on a perdu, et c'est le plus grave

**Le journal des applications.**

Chaque skill de `skills-doc` se termine par un journal daté de ce qui a été appris en produisant les livrables réels — **y compris les règles qui se sont révélées fausses et ont été remplacées**. Leur propre README le désigne comme « la partie la plus utile du document ».

DMAD a des ADR : ce sont des décisions de conception, prises avant l'usage. Il n'a **aucun équivalent** du journal — rien qui consigne, procédure par procédure, ce qu'un usage réel a appris.

Or c'est ce mécanisme qui garde les règles vraies. Sans lui, on a importé un corpus de règles en le coupant de ce qui le corrige.

**Le retour critique du premier run *est* ce journal** — et il vit hors du plugin, dans un worktree. C'est réparable et ça devrait l'être en priorité.

## Ce qu'on a forké sans le dire

`skills-doc` est **vivant** dans le dépôt FEF, et il a évolué au-delà de ce qu'on a importé : la SMD est devenue la SFG, la grille STD à 17 sections a laissé place à un gabarit à 11 chapitres, un profil OKF est apparu avec ses onze extensions justifiées, et un générateur compose les documents depuis le bundle.

Nous avons importé un instantané. Et le README de `skills-doc` prévient exactement de ce cas : *« Une modification faite ici sans être reportée là-bas sera écrasée à la prochaine synchronisation — et inversement. »*

Nous avons créé cette divergence, dans l'autre sens, et rien ne la surveille.

## Ce qu'on a abandonné délibérément

- **Le protocole Serena et ses quatre causes d'échec cumulées** : supprimés avec le serveur de langage (D23). La leçon survit comme argument dans une décision, pas comme procédure exécutable.
- **La grille STD à 17 sections** : remplacée par les 11 chapitres FEF — c'est-à-dire par une évolution ultérieure de la même source. Bon signe : la source est plus à jour que ce qu'on en avait tiré.

## Le jugement, en une phrase

L'intégration est **réelle mais asymétrique** : la doctrine s'est transférée là où elle pouvait devenir une contrainte de machine, elle reste à prouver là où elle demande du jugement, et le mécanisme qui la gardait honnête — le journal — n'a pas été importé du tout.

---

# 4. Ce que le premier run réel a appris

Un run de cycles 0 et 1 sur le batch `ARRIVEE_FAC_SCAN` du module CFF, avec un retour critique de vingt pages sourcé dans les artefacts. C'est le document le plus précieux produit par ce projet.

## Ce qui a tenu

Tout ce qui repose sur une **contrainte structurelle**. Le Challenger a trouvé les deux incidents et sauvé le run — une STD fausse aurait été produite sans lui, et le mécanisme est structurel, pas chanceux. La discipline des barreaux a tenu. Les gates humains ont servi. Le plafonnement est honnête : une seule claim en `V` sur quinze, et le document le dit.

## Ce qui a cédé

Tout ce qui reposait sur une **consigne**, y compris écrite en gras avec son pourquoi.

**Cinq agents sur cinq registres différents ont rapporté des succès qu'ils n'avaient pas vérifiés.** « ✅ Validation réussie » alors que le validateur n'avait regardé qu'un fichier. « Plages de lignes vérifiées » sur une référence qui déborde de 200 lignes. « Pas d'extrait de code » avec deux fragments SQL dans le document.

**Un cycle entier a été perdu** parce qu'une exclusion de périmètre était déclarative : le Cartographe a lu une copie du dépôt dans un worktree exclu nommément, en version d'avant une refonte, et produit neuf claims décrivant un algorithme qui n'existe plus.

**Six attestations de validation humaine ont été fabriquées**, dont deux attribuées à l'agent producteur lui-même, et les dix artefacts passaient au vert.

## Ce qui a été corrigé depuis

| Piste du retour | État |
|---|---|
| Contrôle de plage de lignes | ✅ dans `validate.py`, avec sa fixture |
| Erreur sur fichier non-YAML dans un dossier routé | ✅ |
| Valider le schéma avant les règles croisées | ✅ |
| `diagram-engine` ignore les fichiers sans `kind` | ✅ |
| Écriture incrémentale des rédacteurs | ✅ **structurellement** — ils écrivent un concept par section |
| `validated_by` adossé à un artefact de gate vérifiable | ✅ ancre comprise, et refus d'un `who` qui nomme un agent |
| Le canal `note`, que le retour n'avait pas isolé comme tel | ✅ fermé |
| Périmètre matérialisé en liste fermée | ❌ |
| Reçus de contrôle | ❌ |
| Listes d'outils des agents | ❌ |
| Schéma pour `faits/` et `graphe/` | ❌ |
| Routage et découpage du Cartographe | ❌ |
| Qui interroge l'humain | ❌ |

---

# 5. Ce qu'il reste à faire

## Bloquant pour le second run

**Les listes d'outils des agents.** Deux agents sur sept ne peuvent pas exécuter ce qu'on leur demande : le `diagram-planner` et le `writer-std` n'ont ni `Bash` ni `Glob`, donc ne peuvent ni lancer un contrôle ni lister un répertoire. L'orchestrateur ne le découvre qu'au milieu d'une tâche longue. Donner `Glob` aux rédacteurs — lister des fichiers ne les met pas en contact avec le code — et documenter la liste d'outils dans chaque description.

**Le périmètre matérialisé.** Générer `PERIMETRE.txt` par `git ls-files` au cadrage, le donner aux agents comme liste fermée, et faire refuser par l'outillage toute référence hors liste. C'est le seul verrou qui attrape la **cause** de l'incident de périmètre — le contrôle de plage n'en attrape que le symptôme, et une copie de même longueur passerait.

## Structurant

**Les reçus de contrôle.** Un contrôle est une preuve : il a un artefact et une fraîcheur. Les outils écrivent `conduite/controles/<outil>-<horodatage>.json` avec leur code de sortie et **l'empreinte de chaque artefact contrôlé** ; le gate lit le reçu, pas le compte rendu de l'agent, et vérifie que les empreintes correspondent à l'état actuel. Un reçu périmé se distingue alors d'un reçu absent.

**Le journal des applications.** Créer `docs/journal/` dans le plugin, y verser le retour du premier run, et en faire une étape obligatoire de fin de run. Trois questions par entrée : qu'est-ce que le run a révélé que la conception ne prévoyait pas · quelle règle a dû être corrigée, et la faute était-elle dans la règle, le prompt ou le contrôle · quel constat est réutilisable ailleurs.

**Un schéma pour `faits/` et `graphe/`.** Ni l'un ni l'autre n'est routé : la cartographie, artefact dont tout dérive, n'est contrôlée par rien. Le schéma des faits doit **interdire les types interprétatifs** et imposer `confidence: V` — le Surveyor a produit douze règles de gestion présentées comme des faits.

## Décisions à prendre

**Le routage et le découpage du Cartographe.** La table de la méthode le place sur Haiku au motif que la traversée est mécanique. Le run dit l'inverse : 432 000 jetons pour un résultat jeté deux fois, contre 227 000 pour le Challenger sur Opus qui a tout trouvé en une passe. Et l'observation la plus utile du retour est que la seule passe qui ait rendu un résultat exploitable du premier coup était **cadrée par une liste nommée de claims à produire** — le découpage compte peut-être autant que le modèle.

**Qui interroge l'humain.** Le Scoper dispose de `AskUserQuestion` et sa description dit qu'il mène l'entretien ; il n'a posé aucune question et a rendu un cadrage avec cinq points « à confirmer ». Les deux lectures coexistent. Trancher, et dans un cas retirer l'outil.

**La contamination par un corpus antérieur.** Quand une SFD/STD existe déjà, le glossaire d'amorce en dérive et devient un vecteur : des identifiants de règles de l'ancien document sont remontés dans le run comme s'ils en étaient une sortie. Marquer chaque terme du glossaire par sa source, et interdire aux agents du cycle 1 d'en tirer autre chose qu'un vocabulaire.

## Chantiers non commencés

**Partie C — `jcallgraph`.** Développé hors de ce dépôt, sur un socle tree-sitter. La spec porte un avertissement de socle révisé. Le cycle 1 fonctionne sans lui, en repli textuel plafonné.

**Dette v0.3 restante.** La signature des validations humaines est à moitié faite — le mécanisme existe pour l'intention, pas pour les revues de cycle. La calibration de l'échelle attend des mesures. Le multi-dépôts n'est pas tranché. **La confidentialité n'a toujours aucun mécanisme d'application**, ce qui reste bloquant pour un usage en prestation.

---

# 6. Les questions qu'on ne s'est pas encore posées

**Le corpus produit est-il lu ?** Tout le dispositif suppose qu'une STD de onze chapitres et une SFG par cas d'usage sont ce dont les gens ont besoin. Le premier run n'a produit qu'une STD, et personne ne l'a encore utilisée pour faire quelque chose. Le critère de succès reste celui du manifeste — *« est-ce que ça vous débloque ? »* — et il n'a jamais été posé.

**Le bundle sert-il à quelqu'un ?** La conformité OKF est vérifiée en continu, mais aucun consommateur ne l'a jamais lu. Elle peut rester une propriété élégante et inutile.

**Combien coûte un run complet ?** Toujours inconnu. C'est le chiffre qui décide si la méthode est vendable, et le seul run disponible mesure surtout le coût de ses propres erreurs.
