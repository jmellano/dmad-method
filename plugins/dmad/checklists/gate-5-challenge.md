# Gate 5 — Arbitrage des contradictions

**Qui valide :** un développeur qui connaît le code **et** un référent métier.
**Durée cible :** variable — proportionnelle au nombre de contradictions non résolues.
**Ce qui se passe si on saute ce gate :** des affirmations contradictoires sont publiées côte à côte, et le lecteur découvre l'incohérence avant vous.

## Bloquants

- [ ] **Toute claim `contradicted` est traitée** : retirée de la doc et convertie en question ouverte. Aucune ne reste en attente.
- [ ] **Les tests de caractérisation rouges sont arbitrés.** Un rouge signifie *la règle est fausse*, *le test est faux*, ou *l'environnement ne reproduit pas les conditions réelles* — les trois sont plausibles et il faut trancher.
- [ ] **Les claims `split`** (une claim en cachait deux, typiquement les deux branches d'un flag) ont bien donné lieu à deux claims distinctes.
- [ ] **Aucune claim `V` sans preuve exécutée ou déclarative.** Vérifié mécaniquement par `validate.py`.

## Contrôle anti-complaisance

Le risque le plus insidieux de cette phase : un Challenger qui confirme tout. Un LLM à qui on demande de vérifier confirme, sauf si on l'en empêche par construction.

- [ ] **Le taux de findings est plausible.** Zéro finding sur 40 claims n'est pas le signe d'une documentation parfaite : c'est le signe d'un Challenger complaisant. Sur un legacy réel, un taux de 15 à 30 % de claims dégradées ou reformulées est attendu.
- [ ] **Les 9 angles ont été examinés** sur chaque claim, ou l'angle écarté est justifié (`angles_skipped`).
- [ ] **Le quota de doute est rempli** : si une capacité entière ressort sans finding, le Challenger a produit ses 3 claims les plus fragiles avec l'argument de fragilité.
- [ ] **L'angle 1 (preuve trahie) a produit au moins quelques findings** sur l'ensemble du run. C'est l'erreur dominante des LLM : citer du vrai code en lui faisant dire autre chose. N'en trouver aucune sur des centaines de claims est improbable.

## Répartition attendue

Une répartition saine sur un legacy réel, à titre de repère :

| Niveau | Ordre de grandeur | Lecture |
|---|---|---|
| `V` | 20 – 40 % | dépend fortement du nombre de tests forgés |
| `C` | 30 – 45 % | le gros du corpus |
| `I` | 15 – 30 % | normal, à condition que ce soit affiché |
| `H` | 5 – 15 % | uniquement des intentions |

*Les intentions comptent dans cette répartition mais **pas** dans le badge d'un chapitre : celui-ci est le minimum des seuls énoncés de fait (cf. manifeste §4.1).*

**Signaux d'alerte :**
- `V` > 60 % → soit le projet est exceptionnellement testé, soit des promotions ont été accordées à tort.
- `H` > 25 % → l'historique manque : le run répond au *quoi* mais pas au *pourquoi*. À dire au commanditaire.
- `I` > 50 % → l'outillage est probablement dégradé. Vérifier les plafonds de capability.
