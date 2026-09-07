# Definition of Done — livraison d'un run

## Bloquants

- [ ] `validate.py` passe sur tous les artefacts du run.
- [ ] **Le bandeau obligatoire** figure en tête de chaque document (périmètre, couverture, confiance globale, avertissement sur les niveaux).
- [ ] **Le rapport de couverture est publié**, même — et surtout — s'il est bas.
- [ ] **Aucun renvoi mort** : toutes les références `fichier:lignes` résolvent sur le commit de référence.
- [ ] **Les questions ouvertes sont priorisées** (P1–P4) et adressées à un public identifié.
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
