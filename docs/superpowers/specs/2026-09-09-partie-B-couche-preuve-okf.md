# Partie B — La couche de preuve OKF

> Spec détaillée. Vue d'ensemble : [reste à faire](2026-09-09-dmad-reste-a-faire.md)
> **Dépend de** : A2 (les types doivent être nommés avant d'être sérialisés). **Bloque** : rien.

## L'objet

Le Knowledge Graph — `claims/`, `graph/`, `contracts/`, `business-objects/`, `capabilities/`, `open-questions/`, `challenges/` — devient un **bundle Open Knowledge Format conformant**.

Les trois documents du corpus **restent des documents humains**, projetés depuis le bundle. C'est la garde posée par OKF lui-même : *un bundle est fait pour la connaissance qu'un agent lit, pas pour de la prose humaine ; un README, un billet, un document de conception destiné à des personnes n'est pas un bundle.* Une STD à dix-sept sections est lue par un développeur.

## Pourquoi ça vaut le coup

**Le recouvrement est presque champ pour champ.** DMAD a inventé, isolément, à peu près ce qu'OKF normalise :

| DMAD | OKF |
|---|---|
| `evidence[]` | `sources[]` |
| `evidence.tool` | `sources[].author` en `process:<id>` |
| `produced_by` | `generated.by` en `<producteur>/<version>` |
| promotion par test forgé | `verified: [{by: "process:characterization-test", at}]` |
| `intent.validated_by` | `verified: [{by: "human:<id>", at}]` |
| `freshness` | `status` + `stale_after` |
| `relates_to`, `contradicts` | liens Markdown relatifs, la relation nommée dans la prose |

**Ce qu'on y gagne concrètement**, au-delà de l'interopérabilité :

- `okf-validate --strict` échoue sur les **concepts orphelins** et les **liens morts**. Traduit en DMAD : *une preuve qu'aucun chemin n'atteint est une preuve absente*, et un renvoi mort est un défaut bloquant — deux règles que le Curator applique aujourd'hui à la main.
- La convention d'acteurs (`human:` / `process:` / `<outil>/<version>`) rend **mécanique** la distinction que DMAD tient par discipline : ce qu'un humain a validé contre ce qu'un agent a produit. OKF calcule son niveau de confiance sur le préfixe `human:`. C'est exactement la règle « seul un humain promeut une intention ».
- Un bundle est lisible par n'importe quel agent, sans SDK. Une SFD n'a besoin de personne pour être lue ; un graphe de preuves, si.

---

## B1 — La table de correspondance des champs

Le document qui décide de tout le reste. Il doit trancher les cas où le recouvrement **n'est pas** exact.

### Ce qui se traduit directement

```yaml
# DMAD v0.4                          # OKF v0.2
id: BR-FACT-014                      → chemin du fichier : claims/BR-FACT-014.md
type: BusinessRule                   → type: BusinessRule          (OKF : chaîne libre descriptive)
statement: >                         → corps du document
  Une facture dont le montant…
produced_by: dmad-elucidator         → generated: {by: "dmad-elucidator/0.4.0", at: …}
evidence:
  - kind: code                       → sources:
    ref: src/…#L212-L228               - id: ev-code-1
    commit: a1b2c3d                      resource: "src/…#L212-L228@a1b2c3d"
    tool: lsp.find_definition            author: "process:lsp.find_definition"
```

Chaque `evidence` devient une entrée de `sources` avec un `id`, et le corps **cite cet id en note de bas de page** — `…n'est pas transmise.[^ev-code-1]`. C'est la forme OKF de l'attribution d'une affirmation à sa preuve, et elle est plus fine que le bloc `evidence` actuel : elle rattache **une phrase** à **une preuve**, au lieu de rattacher un paquet de preuves à une claim entière.

C'est un gain réel de la migration, pas un effet de bord : l'anti-pattern A2, la preuve trahie, se loge précisément dans l'écart entre « cette claim a des preuves » et « cette phrase a cette preuve ».

### Ce qui n'a pas d'équivalent, et reste en clé d'extension

OKF autorise explicitement les producteurs à ajouter leurs clés, et exige des consommateurs qu'ils les préservent. On garde donc, tels quels :

`confidence` · `confidence_reason` · `confidence_ceiling_applied` · `conditional_on` · `challenged_by` · `challenge_outcome` · `freshness` (voir B6) · `resolution_rung` · `artifact_version`.

**`confidence_reason` mérite d'être défendu** : OKF n'a rien de tel, et c'est le champ le plus utile de DMAD — celui qui force un agent à écrire *ce qui manque pour monter d'un niveau*. Le supprimer au nom de la conformité serait perdre le meilleur pour gagner l'interopérable.

### Le cas qui demande une décision de conception

**L'intention.** Une claim porte un `statement` prouvable et un bloc `intent` non prouvable, chacun avec sa confiance — c'est la décision D6, l'une des plus structurantes de la méthode.

Or `verified` en OKF vouche pour **le concept entier**. Écrire `verified: [{by: "human:jdupont"}]` sur une claim dont seule l'intention a été validée ferait mentir le niveau de confiance calculé : un lecteur comprendrait que le fait a été vérifié.

Deux options :

| Option | Ce qu'elle donne | Ce qu'elle coûte |
|---|---|---|
| **L'intention devient un concept propre**, lié à la claim | `verified` dit la vérité ; la séparation fait/intention devient structurelle au lieu d'être conventionnelle | un concept de plus par règle, et une navigation en deux sauts |
| **`verified` reste réservé au fait**, l'intention garde `intent.validated_by` en clé d'extension | migration plus légère | un consommateur OKF générique ne voit pas la validation de l'intention |

**Recommandation : le concept propre.** D6 dit que la séparation existe parce qu'un modèle produirait sinon « la facture nulle n'est pas transmise *pour éviter les rejets* » — une phrase dont la moitié est prouvée et l'autre inventée. Faire de l'intention un concept distinct, c'est rendre cette séparation impossible à effacer.

---

## B2 — Types de concepts et arborescence

```
dmad-evidence/                    ← le bundle
├── index.md                      okf_version: "0.2"
├── log.md                        append-only, plus récent en tête
├── capabilities/     index.md + un concept par capacité
├── entrypoints/      index.md + un concept par point d'entrée
├── business-objects/ index.md + un concept par BO
├── contracts/        index.md + un concept par contrat sortant
├── claims/           index.md + un concept par règle, cas d'usage, invariant…
├── intents/          index.md + un concept par intention           (cf. B1)
├── open-questions/   index.md + un concept par question
├── challenges/       index.md + un concept par réfutation
├── diagrams/         index.md + un concept par diagramme planifié
└── documents/        index.md + un concept par document du corpus  (métadonnées seules)
```

`documents/` ne contient **pas** les documents : il contient leur carte d'identité — `kind`, `unit`, `derives_from`, `frozen_at` — et les liens vers les claims qu'ils rendent. C'est ce qui permet à `--strict` de vérifier la cascade sans avaler la prose.

**Les `type` à définir** : `Capability`, `Entrypoint`, `BusinessObject`, `ExternalContract`, `BusinessRule`, `UseCase`, `Invariant`, `StateMachine`, `Actor`, `Term`, `Risk`, `Intent`, `OpenQuestion`, `Challenge`, `Diagram`, `Document`.

**Liens relatifs, jamais absolus.** OKF admet les deux, mais la forme absolue est résolue contre la racine du dépôt par GitHub, qui sert alors un 404, et les visualiseurs n'en construisent aucune arête. Google a converti ses propres bundles pour cette raison. Corollaire : après tout déplacement, rejouer le validateur.

---

## B3 — La migration

Un convertisseur **ponctuel**, pas un pont permanent. On ne maintient pas deux formats : le jour où le bundle est la source, les schémas YAML d'A2 disparaissent.

À migrer : les artefacts du run de référence, les six fixtures de violation, et les schémas qui deviennent des contrôles du validateur OKF.

**Le point de vigilance** : les fixtures de violation doivent continuer d'être refusées **après** migration. Si une violation devient acceptable parce que le format a changé, c'est le format qui a perdu une garantie — et il faut le dire, pas le découvrir plus tard.

---

## B4 — La validation

`okf-validate.mjs --strict` intégré à `validate.py` et posé en gate de fin de cycle.

Ce que `--strict` apporte que DMAD n'a pas aujourd'hui :

- **orphelins** — un concept qu'aucun lien n'atteint. Un agent qui traverse le bundle ne le trouvera jamais : il est absent par construction.
- **liens morts** — dont les liens vers un `index.md`, que la spec réserve.
- **`--drift`** — compare chaque entrée d'index à la `description` du concept lié. Attrape l'index qui annonce encore une affirmation corrigée depuis.

À ajouter côté DMAD, en règles croisées sur le bundle : la dérivation confiance ↔ barreau, la propagation de péremption, et les contrôles de cascade d'A1 qui portent sur `documents/`.

---

## B5 — `index.md` et `log.md`

**Générés, jamais édités à la main.** Un index désynchronisé est pire qu'absent : il annonce ce qui n'est plus là.

`log.md` est append-only, une ligne par entrée, plus récent en tête, jamais de réécriture d'une entrée passée — une correction supersède. Cette contrainte se marie exactement avec le versionnement git déjà retenu, et avec la règle DMAD que l'historique des corrections est lui-même une source de connaissance.

**Ce qui déclenche une entrée de log** : la création d'un concept, une modification de sens, une dépréciation. Pas une transformation mécanique — une conversion de forme de lien, une passe de ponctuation — qui met à jour le log sans toucher `generated`.

---

## B6 — La fraîcheur

`status` (`draft` / `stable` / `deprecated`) et `stale_after` remplacent le bloc `freshness`.

La correspondance n'est **pas** directe et doit être décidée :

| DMAD | Proposition OKF |
|---|---|
| claim en cours de cycle | `status: draft` |
| claim d'un document figé | `status: stable` |
| claim retirée | `status: deprecated` |
| `fresh` / `shifted` / `stale` / `broken` | reste en clé d'extension `freshness` — OKF n'a pas ces nuances, et elles sont utiles |
| péremption prévisible | `stale_after: YYYY-MM-DD` |

**B6 et A6 implémentent la même chose.** Si B est priorisé, A6 devient sans objet ; si A6 est fait d'abord, B6 le réécrit. À arbitrer explicitement plutôt qu'à découvrir en cours de route.

Un point qu'OKF impose et qui sert DMAD : *si l'on modifie matériellement un concept qui portait un `verified`, cette vérification ne couvre plus ce que le concept dit maintenant — on la retire plutôt que de la laisser cautionner un texte que personne n'a relu.* C'est la règle qui manquait à la question ouverte D1 sur les validations humaines.

---

## La question laissée ouverte

**Faut-il mettre les trois documents dans le bundle ?**

La décision actuelle les laisse dehors — c'est la garde d'OKF, et c'est le confort de lecture.

L'alternative : chaque section de STD, chaque business object de SFD, chaque cas d'usage de SFG devient un concept lié. La cascade deviendrait alors **vérifiable par le validateur de liens** : une section de SFD sans lien vers son ancrage STD serait un orphelin, détecté par `--strict` sans écrire une ligne de contrôle spécifique.

C'est séduisant, et c'est exactement le contrôle n° 4 d'A1 obtenu gratuitement. Ça se paie en lisibilité : une STD éclatée en cinquante fichiers n'est plus un document qu'on ouvre lundi matin.

**À trancher au début de B, pas maintenant** — et le facteur décisif sera ce qu'aura montré le premier run réel sur la façon dont les gens lisent réellement ces documents.

---

## Fin de partie

Le bundle passe `okf-validate --strict`, les fixtures de violation sont toujours refusées, le run de référence est migré, et aucun agent n'écrit plus de YAML DMAD.
