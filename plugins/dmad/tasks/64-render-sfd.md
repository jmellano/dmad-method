# Task 64 — Écrire la strate SFD du bundle

**Agent :** `writer-sfd` · **Cycle :** 2 · **Sorties :** concepts `<bundle>/processus/<p>/sfd/`, `plan-sfd.yaml`, puis `SFD-<processus>.md` composée

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

## Ce qui est lu

**La STD figée et les claims validées.** Pas le code, pas le graphe brut (D17). Une information absente de la STD ne peut pas apparaître ici : le trou se propage visiblement plutôt que d'être comblé.

## L'unité est le processus, le même que la STD

STD et SFD partagent l'unité et le périmètre (D25). Elles ne diffèrent que par l'**audience** et le **registre** — c'est le chapeau qui fixe la frontière, et c'est pour cela qu'il n'est pas décoratif.

## Les dix chapitres

Processus métier · processus général du SI · processus détaillé du SI · services externes · gestion des erreurs · cas de test · règles de gestion · références · historique · annexes.

**Le chapitre 3 est le cœur, et il est libre.** Un § par sous-processus, puis la vue récursive par objet métier dont le **nombre de niveaux est un résultat de l'analyse**. Chaque niveau porte les six blocs : traitement · contrôle · données initiales · données ad-hoc · données de contrôle · sorties normales et anormales.

**Signale les données ad-hoc chargées en boucle**, avec leur cardinalité si elle est connue. C'est le signal le plus rentable pour un lecteur venu pour un temps de réponse.

## Interdits

Blocs de code, noms de classes, noms de méthodes, **noms de patrons de conception**. Le patron a servi au découpage ; il n'a rien à faire ici.

Un diagramme est nommé **par ce qu'il montre**, jamais par son type.
