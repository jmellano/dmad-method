# Gabarits DMAD

**Le gabarit d'un document n'est pas un fichier à copier : c'est son plan.**

Les trois `plan-*.yaml` fixent le plan de niveau 1 — onze chapitres en STD, dix en SFD, six en SFG — et portent, à côté de chaque numéro, **la consigne de rédaction de la section**. La consigne vit là et nulle part ailleurs : deux copies d'une consigne divergent, et c'est la copie qu'on lit qui est la mauvaise.

| Fichier | Ce qu'il fixe |
|---|---|
| [`plan-std.yaml`](plan-std.yaml) | onze chapitres, audience MOE |
| [`plan-sfd.yaml`](plan-sfd.yaml) | dix chapitres, audience hybride MOA/MOE |
| [`plan-sfg.yaml`](plan-sfg.yaml) | six chapitres, audience métier |
| [`doc-header.md`](doc-header.md) | le bandeau obligatoire |

## S'en servir

```bash
cp <plugin>/templates/plan-std.yaml <run>/plan-std.yaml     # puis remplacer les {{…}}
python3 <plugin>/tools/scaffold.py <run>/plan-std.yaml --bundle <run>/okf --prefix processus/<p>
# … rédaction, un concept à la fois …
python3 <plugin>/tools/okf-compose.py <run>/okf --all <run>
```

`scaffold.py` crée **un concept vide par section**, chacun portant sa consigne en bloc `[gabarit]`. Le rédacteur la supprime au fur et à mesure — `check-corpus.py` refuse un document qui en porte encore.

Il **n'écrase jamais** un concept existant : le rejouer après une passe sert à matérialiser les sections que l'analyse a fait apparaître.

## Ce qui est fixe, ce qui est libre

C'est la seule question qui compte à l'usage, et la réponse n'est pas « tout est fixe ».

**Fixe** — le plan de niveau 1 · les sept blocs de chaque cas d'usage de SFG, dans leur ordre · le chapeau d'audience et de périmètre · les en-têtes des tableaux de catalogue · les champs de frontmatter.

**Libre** — tout ce dont la forme est imposée par une règle plutôt que par une liste de titres : le nombre de niveaux d'une vue récursive, le nombre de cas d'usage d'une SFG, les sous-sections propres à un traitement. Ce sont des **résultats de l'analyse**, et une section marquée `free_subsections` le déclare.

**Corollaire.** Une section dont le sujet n'existe pas dans ce traitement **ne se supprime pas** : elle se remplit avec le constat d'absence **et son périmètre**. Un résultat négatif explicite fait gagner du temps ; une section absente laisse croire à un oubli. Le plus grand gain est le **piège d'attribution** — signaler les artefacts voisins qui ressemblent à ce que le lecteur cherche mais n'appartiennent pas au périmètre.

## Un gabarit ne remplace pas la méthode

Le plan donne la structure et les invariants de forme. Ce qui remplit chaque section — comment descendre l'arbre d'appels, comment identifier les objets métier, comment prouver qu'une erreur est atteignable — relève des tâches 63, 64 et 65, et des skills prérequis.

## Ce que les outils contrôlent

| Outil | Ce qu'il refuse |
|---|---|
| `okf-compose.py` | concept du plan introuvable · **concept du bundle absent du plan** · section imposée sans constat d'absence · saut de niveau de titre · lien ou ancre morts |
| `check-corpus.py` | bloc de code (D16) · plan de niveau 1 altéré · sept blocs de SFG · règle sans traçabilité · index inverse incohérent · diagramme sans question ou écrit à la main · **notation sans légende, légende orpheline, compteur faux** · marqueur de gabarit résiduel |

Aucun ne contrôle l'exactitude factuelle : c'est le travail du Challenger et du contrôle par échantillonnage.
