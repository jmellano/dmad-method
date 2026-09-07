# Definition of Done — une claim

Checklist appliquée à chaque affirmation avant publication. Automatisable en grande partie via `validate.py` ; le reste relève de la relecture.

## Automatisé (`validate.py`)

- [ ] Au moins une `evidence`
- [ ] `confidence_reason` renseignée et substantielle
- [ ] `freshness.verified_at_commit` présent
- [ ] `intent` séparé du `statement`, plafonné à `H` sans validation humaine
- [ ] `V` uniquement avec preuve exécutée (test vert) ou déclarative (schéma, migration, runtime)
- [ ] `promoted_by` = `test-forger` exclusivement
- [ ] Confiance ≤ plafond de capability appliqué
- [ ] `conditional_on` reflété dans le `statement`

## Relecture humaine

- [ ] **La preuve dit ce qu'on lui fait dire.** À vérifier par échantillonnage : ouvrir 5 claims au hasard et lire les lignes citées. C'est le contrôle le plus rentable de toute la méthode.
- [ ] **Le `statement` décrit un comportement, pas une intention.** Un « pour éviter que » dans le statement est une erreur de rangement : ça va dans `intent`.
- [ ] **Aucun verbe d'opinion** : *semble*, *paraît*, *devrait*, *a l'air de*, *gère probablement*. Une incertitude s'exprime par le niveau de confiance, pas par un adverbe.
- [ ] **Portée explicite.** « Toujours » et « jamais » exigent d'avoir vérifié tous les appelants. Sinon : « sur le chemin X ».
- [ ] **Localisation précise.** `fichier#Ldébut-Lfin`, pas `fichier`. Une claim qui pointe un fichier de 800 lignes n'est pas vérifiable.
- [ ] **Formulation autonome.** La claim se comprend sans avoir lu la précédente.

## Le contrôle par échantillonnage

Le seul contrôle qui détecte réellement l'angle 1 (preuve trahie) :

> Tirer 5 claims au hasard, ouvrir le code aux lignes citées, vérifier que la phrase correspond.

**Un taux d'erreur supérieur à 1 sur 5 condamne le run** : il faut repasser le Challenger avec des consignes durcies. Ce contrôle prend dix minutes et vaut plus que n'importe quelle relecture intégrale — parce qu'une relecture intégrale d'une documentation crédible ne détecte rien.
