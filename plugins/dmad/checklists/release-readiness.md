# Definition of Done — livraison d'un run

## Bloquants

- [ ] `validate.py` passe sur tous les artefacts du run.
- [ ] **Le bandeau obligatoire** figure en tête de chaque document (périmètre, couverture, confiance globale, avertissement sur les niveaux).
- [ ] **Le rapport de couverture est publié**, même — et surtout — s'il est bas.
- [ ] **Aucun renvoi mort** : toutes les références `fichier:lignes` résolvent sur le commit de référence.
- [ ] **Les questions ouvertes sont priorisées** (P1–P4) et adressées à un public identifié.
- [ ] **Au moins un diagramme par capacité documentée**, et chacun compile réellement
      (cf. `diagram-quality.md`). La phase 6 est facile à sauter sans que rien ne le
      signale : le résultat reste cohérent et bien sourcé, simplement dépourvu de toute
      représentation. Sur un legacy, un schéma vaut trente pages — son absence est une
      non-livraison, pas un manque de finition.
- [ ] **Le registre d'intention est non vide** — REX, décisions structurantes, contraintes
      externes. L'Archaeologist est l'autre phase qu'on saute sans s'en apercevoir. Repère
      du premier run réel : le mot « pourquoi » apparaissait dans 18 fichiers de la
      documentation d'origine contre 3 dans la production initiale, REX et leçons à zéro.
      Un run sur un projet de plusieurs années qui ne produit aucun REX n'a pas terminé —
      il a documenté le *quoi* en laissant le *pourquoi* dans les sources non lues.
- [ ] **Chaque capacité a sa section « à confirmer »** et sa section « ce qui n'a pas été analysé », même vides — auquel cas elles affichent « aucune » explicitement.
- [ ] **Le glossaire est unifié** : aucun terme employé dans deux sens.
- [ ] **Les contradictions inter-capacités sont résolues** ou consignées.

## Contrôles de bon sens

- [ ] **Le commanditaire peut répondre à sa question initiale** en lisant le document. C'est le seul critère qui compte vraiment : relire `scope.objective.statement` et vérifier.
- [ ] **La doc fonctionnelle ne contient aucun nom de classe ou de table.** Recherche automatique sur `.java`, `.php`, `Service`, `Impl`, `Repository`.
- [ ] **La doc technique ne contient aucune affirmation métier non sourcée.**
- [ ] **Un développeur qui ne connaît pas le projet trouve un point d'entrée en moins de 5 minutes.** Se teste réellement, avec un vrai développeur.
- [ ] **Le contrôle par échantillonnage a été fait** (5 claims tirées au hasard, preuves vérifiées, cf. `claim-quality.md`).

## Ce qu'il faut dire à la livraison

Un run DMAD ne se livre pas comme une documentation terminée. Il se livre comme **un état des connaissances daté, avec ses limites et sa liste de questions** :

> « Voici ce qu'on a établi, avec quel niveau de preuve, sur 22 % du code —
> mais 90 % des zones à risque. Voici les 6 questions P1 dont les réponses
> feront monter 14 affirmations d'hypothèse à fait établi. Voici ce qu'on
> n'a pas regardé, et pourquoi. »

Présenter un run DMAD comme une documentation complète annule le bénéfice de toute la chaîne de preuve.
