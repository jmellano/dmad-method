# DMAD — La couche de preuve en Open Knowledge Format

## Ce qui est dans le bundle, et ce qui reste dehors

Le **graphe** est de la connaissance destinée à un agent : claims, contrats, business objects, questions ouvertes, réfutations, intentions, cartes d'identité des documents. C'est exactement ce qu'OKF normalise, et c'est le bundle.

Les **trois documents** du corpus restent dehors. OKF pose lui-même la garde : *un bundle est fait pour la connaissance qu'un agent lit, pas pour de la prose humaine.* Une STD à dix-sept sections est lue par un développeur le lundi matin.

```bash
python3 tools/okf-export.py <run> --check --at <horodatage>
```

L'export est **reproductible** quand on fixe `--at` : sans lui, un bundle versionné change à chaque passe et son diff devient illisible.

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

L'exportateur porte ses propres contrôles : la règle dure d'OKF (tout concept porte un `type` non vide), les orphelins et les liens morts. Ils suffisent au selftest et ne demandent rien d'autre que Python.

Quand le validateur officiel est disponible, il tranche :

```bash
node okf-validate.mjs <bundle> --strict
```

Le bundle du run de référence passe les deux : *18 concepts, 0 erreur, 0 avertissement, 0 lien mort, 0 orphelin.*

## Ce qui reste ouvert

**Faut-il mettre les trois documents dans le bundle ?** La décision actuelle les laisse dehors — c'est la garde d'OKF, et c'est le confort de lecture.

L'alternative : chaque section de STD, chaque business object de SFD, chaque cas d'usage de SFG devient un concept lié. La cascade deviendrait alors **vérifiable par le validateur de liens** — une section de SFD sans lien vers son ancrage STD serait un orphelin, détecté sans écrire une ligne de contrôle spécifique. C'est exactement ce que `check-corpus.py` fait aujourd'hui à la main.

Ça se paie en lisibilité : une STD éclatée en cinquante fichiers n'est plus un document qu'on ouvre lundi matin.

**Le facteur décisif n'est pas théorique.** Il sera ce qu'aura montré le premier run réel sur la façon dont les gens lisent réellement ces documents — et cette question ne se tranche pas en réunion, elle se tranche en regardant quelqu'un ouvrir une STD pour modifier un batch.
