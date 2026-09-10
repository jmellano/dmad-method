# Task 63 — Écrire la strate STD du bundle

**Agent :** `writer-std` · **Cycle :** 1 · **Sorties :** concepts `<bundle>/processus/<p>/std/`, `plan-std.yaml`, puis `STD-<processus>.md` composée

## Tu écris des concepts, pas un document

Le bundle est la sortie primaire ; le fichier est composé (D26).

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/tools/scaffold.py <plan> --bundle <bundle> --prefix processus/<processus>
# … rédaction, un concept à la fois …
python3 ${CLAUDE_PLUGIN_ROOT}/tools/okf-compose.py <bundle> --all <run>
```

`scaffold.py` matérialise un concept vide par section du plan, chacun portant **sa consigne en bloc `[gabarit]`**. Tu la supprimes au fur et à mesure : `check-corpus.py` refuse un document qui en porte encore.

Il **n'écrase jamais** un concept existant. Le rejouer après une passe sert à créer les sections que l'analyse a fait apparaître.

## Le plan

Le **plan de niveau 1 est imposé** — le gabarit le fixe. Les **sous-sections sont un résultat de l'analyse**, pas une décision de mise en page : tu les ajoutes au plan à mesure que tu les découvres, et `scaffold.py` les matérialise.

Une section imposée dont le sujet n'existe pas **ne se supprime pas** : elle porte son constat d'absence **et son périmètre**. Le plus grand gain est le **piège d'attribution** — signaler les artefacts voisins qui ressemblent à ce que le lecteur cherche mais n'appartiennent pas au périmètre.

## Ce que le composeur refuse

Un concept du plan introuvable · **un concept du bundle absent du plan** — écrit, et que personne ne lira · une section imposée sans concept ni sous-section · un saut de niveau de titre · un lien ou une ancre morts.

Il ne produit pas un document approximatif : il refuse.

## Les deux contraintes du contenu

**Pas d'accès au code.** Le graphe et les claims, rien d'autre.

**Aucun bloc de code, aucune requête, aucune configuration** (D16). Des **références** : `fichier:lignes`, signatures, noms de tables et de colonnes. C'est ce qui rend la première contrainte tenable — tant qu'un extrait est permis, aller lire le code a un motif légitime.

## L'unité est le processus

Une STD documente **un processus**, pas un point d'entrée (D25) : un processus en a rarement un seul. Le chapitre 1 les catalogue, et le périmètre déclaré dans le frontmatter **se vérifie contre ce chapitre** — pas l'inverse.

## Les onze chapitres

Le plan les fixe : cartographie · modèle de données · traitement de données · gestion des erreurs · appels externes · dépendances · points d'attention · cas de test · références · historique · annexes.

**Chapitre 1**, la cartographie se clôt par la cohésion et le couplage : chaque ligne **cite un fait documenté ailleurs**. Cette table rassemble sous le critère, elle ne redécouvre pas. Si le fait est introuvable ailleurs, soit il manque, soit la qualification est faible.

**Chapitre 4**, sépare le **site de levée** et l'**effet observable**. Ce ne sont pas le même fait, et les confondre crée des contradictions qui deviendront des promesses fausses en SFG.

**Chapitre 5**, une ligne par contrat avec son **barreau** et sa **version d'artefact**. Un contrat non résolu porte un placeholder visible et une ligne au chapitre 7 — jamais un code plausible.

## Quand il manque quelque chose

Une `gap_request`, jamais un comblement. `blocking` relance la cartographie ou la résolution des contrats ; `degrades` devient une question ouverte, et le document sort avec son trou visible.
