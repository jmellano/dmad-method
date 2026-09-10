# DMAD — Le run est un bundle Open Knowledge Format

## Le run EST le bundle

Il n'y a **pas d'export** (D28). Les agents écrivent des concepts — du Markdown à frontmatter — et `dmad-output` est directement un bundle conformant. `tools/okf-index.py` ne produit rien de nouveau : il **maintient** la navigation, index par répertoire et bloc de liens de chaque concept, puis contrôle.

```bash
python3 tools/okf-index.py <run> --check
```

**Deux zones sont hors bundle par convention.** `documents/` porte les fichiers composés, qui sont de la prose destinée à des humains — c'est la garde d'OKF, et une STD se lit le lundi matin. `conduite/` porte ce qui parle du run et non du système.

**Ce qui reste de la donnée reste de la donnée.** Faits, graphe, frontières, plans de diagrammes et figures rendues sont lus par des outils. Ils gardent leur format, et une figure rendue porte l'extension `.txt` — sans quoi un validateur y verrait un concept sans frontmatter, ce qui est arrivé.

## Pourquoi OKF plutôt qu'un format maison

Le recouvrement est presque champ pour champ — DMAD avait inventé, isolément, à peu près ce qu'OKF normalise :

| DMAD | OKF |
|---|---|
| `evidence[]` | `sources[]` |
| `evidence.tool` | `sources[].author`, en `process:<outil>` |
| `produced_by` | `generated.by`, en `<producteur>/<version>` |
| promotion par test de caractérisation | `verified: [{by: "process:characterization-test"}]` |
| `intent.validated_by` | `verified: [{by: "human:<id>"}]` sur le concept d'intention |
| `status` (draft / challenged / validated / retired) | `status` (draft / draft / stable / deprecated) |
| `freshness` | conservé en clé d'extension — OKF n'a pas ces nuances, et elles servent |

Ce qu'on y gagne au-delà de l'interopérabilité :

**La convention d'acteurs rend mécanique ce que DMAD tenait par discipline.** `human:` contre `process:` contre `<outil>/<version>` : OKF calcule son niveau de confiance sur le préfixe `human:`. C'est exactement la règle « seul un humain promeut une intention », et elle n'est plus une consigne mais une donnée.

**Les orphelins et les liens morts deviennent des défauts détectables.** Traduit en DMAD : *une preuve qu'aucun chemin n'atteint est une preuve absente*, et un renvoi mort est un défaut bloquant. Deux règles que le Curator appliquait à la main.

**L'attribution devient plus fine.** Une note de bas de page rattache **une phrase** à **une preuve**, là où le bloc `evidence` rattachait un paquet de preuves à une claim entière. Ce n'est pas un effet de bord : l'anti-pattern A2, la preuve trahie, se loge précisément dans l'écart entre « cette claim a des preuves » et « cette phrase a cette preuve ».

## Les deux choix de conception

### L'intention devient un concept propre

`verified` en OKF vouche pour **le concept entier**. Poser `verified: [{by: "human:…"}]` sur une claim dont seule l'intention a été validée ferait croire qu'un humain a vérifié le **fait**.

Or la séparation fait / intention est la décision D6, l'une des plus structurantes de la méthode : sans elle, un modèle produit « la facture nulle n'est pas transmise *pour éviter les rejets comptables* » — une phrase dont la moitié est prouvée et l'autre inventée, sans que rien ne le signale.

Chaque `intent` devient donc un concept `Intent`, lié à sa claim. **La séparation passe de conventionnelle à structurelle** : elle n'est plus effaçable par distraction.

### `confidence_reason` reste

OKF n'a pas d'équivalent, et c'est le champ le plus utile de DMAD : celui qui force un agent à écrire **ce qui manque pour monter d'un niveau**. OKF autorise explicitement les clés de producteur et exige des consommateurs qu'ils les préservent. Le supprimer au nom de la conformité serait perdre le meilleur pour gagner l'interopérable.

Restent aussi en clés d'extension : `confidence`, `confidence_ceiling_applied`, `conditional_on`, `challenge_outcome`, `freshness`, `resolution_rung`, `artifact_version`, `dmad_id`.

## Ce que l'export signale et ne corrige pas

Un lien vers un artefact absent du run est **signalé, jamais abandonné en silence** :

```
⚠ 5 lien(s) vers un artefact absent du run :
  br-fact-021.md → CHK-2026-09-07-034
```

Ce n'est pas forcément une faute — la cible peut être hors périmètre — mais c'est une arête du graphe qui n'existe pas dans le bundle, et le taire reviendrait à publier une carte dont on a effacé des routes.

## Vérifier

L'indexeur porte ses propres contrôles : la règle dure d'OKF (tout concept porte un `type` non vide), les orphelins et les liens morts. Ils suffisent au selftest et ne demandent rien d'autre que Python.

Quand le validateur officiel est disponible, il tranche :

```bash
node okf-validate.mjs <bundle> --strict
```

Le bundle du run de référence passe les deux : *18 concepts, 0 erreur, 0 avertissement, 0 lien mort, 0 orphelin.*

## Deux collisions de vocabulaire, et la règle qui les tranche

**Quand la spécification définit une propriété pour un besoin, elle garde son sens** — même si nos artefacts la nommaient autrement. Une extension ne se justifie que par l'absence d'équivalent officiel, jamais par une habitude de nommage.

`status` en est le cas d'école : OKF y met le cycle de vie du concept (`draft` / `stable` / `deprecated`), DMAD y mettait l'arbitrage d'une claim (`draft` / `challenged` / `validated` / `retired`) et l'état d'une question (`open` / `answered`…). Trois sens pour un nom. L'officiel garde le sien ; les nôtres deviennent `claim_status` et `answer_status`.

Le renommage est le prix de la portabilité : un consommateur OKF quelconque sait lire `status`, il ne saura jamais deviner lequel de nos trois sens il lit.

## Ce qui reste ouvert

**Faut-il mettre les trois documents dans le bundle ?** La décision actuelle les laisse dehors — c'est la garde d'OKF, et c'est le confort de lecture.

L'alternative : chaque section de STD, chaque business object de SFD, chaque cas d'usage de SFG devient un concept lié. La cascade deviendrait alors **vérifiable par le validateur de liens** — une section de SFD sans lien vers son ancrage STD serait un orphelin, détecté sans écrire une ligne de contrôle spécifique. C'est exactement ce que `check-corpus.py` fait aujourd'hui à la main.

Ça se paie en lisibilité : une STD éclatée en cinquante fichiers n'est plus un document qu'on ouvre lundi matin.

**Le facteur décisif n'est pas théorique.** Il sera ce qu'aura montré le premier run réel sur la façon dont les gens lisent réellement ces documents — et cette question ne se tranche pas en réunion, elle se tranche en regardant quelqu'un ouvrir une STD pour modifier un batch.
