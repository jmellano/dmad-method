# Task 65 — Écrire la strate SFG du bundle

**Agent :** `writer-sfg` · **Cycle :** 3 · **Sorties :** concepts `<bundle>/processus/<p>/sfg/`, `plan-sfg.yaml`, puis `SFG-<domaine>.md` composée

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

**La SFD figée. Rien d'autre** (D17). Ni le code, ni le graphe, ni la STD.

## Prérequis bloquant

Le `Curator` a vérifié que la SFD ne se contredit pas. Si une contradiction apparaît malgré tout en cours de rédaction : **arrête et remonte**. Ne choisis pas la version la plus plausible, n'écris pas une formulation qui concilie — les deux sections peuvent être vraies à deux moments différents du traitement, et c'est cette distinction qui est l'information.

## L'unité est le cas d'usage

Ce qui se demande, s'arbitre et se livre d'un bloc. Le **nombre de cas d'usage est un résultat** : le plan n'en impose ni trois ni cinq. Une variation qui ne change ni les acteurs, ni le déclencheur, ni le résultat attendu **n'est pas un cas d'usage** mais une règle à l'intérieur d'un cas.

## Les six chapitres, et les sept blocs

Ce que le domaine résout · invariants · les cas d'usage · index inverse · ce que la rédaction a révélé · historique.

Chaque cas d'usage porte **sept blocs, sans numéro et sans exception** : Situation · Acteurs et rôles métier · Déclencheur et cadence (**avec le fuseau horaire**) · Règles applicables · Ce que l'utilisateur voit (**succès et échec**) · Ce qui n'est pas couvert · Traçabilité.

> **« Ce qui n'est pas couvert » conditionne tout le reste.** Un cas d'usage dont la frontière n'est pas écrite ne peut être l'unité d'évolution de rien.

L'**index inverse** se génère, il ne s'édite pas : un écart entre le corps et l'index est un défaut, pas un arrondi.

## Interdit d'audience — le frontmatter compris

Aucun nom de composant, d'application, de table, de code technique, hors du bloc traçabilité. **Le frontmatter est du contenu** : une SFG ne porte ni `entry_point_type` ni `entry_point_name` — un lecteur métier n'a pas à lire un nom de job sur son premier écran.
