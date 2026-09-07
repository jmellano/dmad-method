# Task 30 — Découper en capacités

**Agent :** `carver` · **Phase :** 3 · **Modèle :** opus · **Sortie :** `capabilities.yaml`

## Les quatre signaux

| Signal | Calcul | Faiblesse |
|---|---|---|
| Cohésion d'appels | densité d'arêtes `calls` intra-groupe / inter-groupes | god classes, utilitaires transverses |
| Partage de données | tables communes en lecture/écriture | tables fourre-tout (`params`, `audit`, `log`) |
| Couplage temporel | co-occurrence dans les commits (fenêtre glissante) | commits massifs (reformatage, montée de version) |
| Vocabulaire | lexique partagé (noms, libellés, messages) | nommage incohérent des legacy |

**Seuil : 3 signaux convergents sur 4** pour `hypothesis_strength: strong`.

> **Réserve à assumer.** Ces quatre signaux ne sont **pas indépendants**. La cohésion d'appels et le partage de données se recoupent largement (des fonctions qui s'appellent manipulent souvent les mêmes tables), et le vocabulaire corrèle avec les deux dans un code bien nommé. Trois signaux convergents ne valent donc pas trois confirmations indépendantes.
>
> Conséquence pratique : **le couplage temporel git est le signal qui apporte le plus d'information**, parce qu'il est le seul construit sur une source entièrement différente — le comportement des développeurs, pas la structure du code. Une capacité soutenue par cohésion + données + vocabulaire, mais **contredite par l'historique**, est plus fragile que ne le suggère son score. Le Carver doit la présenter comme telle.

Le couplage temporel mérite une attention particulière : dans un legacy où l'architecture a été violée pendant dix ans, **ce qui change ensemble est souvent plus vrai que ce qui est rangé ensemble**.

## Filtrage préalable obligatoire

Avant tout clustering, écarter les nœuds transverses — sinon ils agrègent tout en une capacité unique :
- fichiers présents dans > 60 % des commits (utilitaires, configuration)
- tables techniques (`audit`, `log`, `sequence`, `params`, `i18n`)
- god classes (> 50 appelants entrants)

Ces nœuds sont rangés dans une capacité `transverse` explicite, pas ignorés.

## Recherche des seams

Un *seam* est un point où le système peut être coupé sans réécriture. Les candidats :
- interfaces avec une seule implémentation (le point d'injection existe déjà)
- ports explicites (`*Gateway`, `*Port`, `*Adapter`, `*Client`)
- frontières de transaction
- frontières réseau (déjà découplées par construction)

Pour chaque seam : ce qu'il isole, combien d'appels le traversent, l'effort estimé, et **les tests de caractérisation qui sécuriseraient l'opération**.

## Préparer le gate 3

Le Carver ne présente pas un schéma. Il présente **les décisions à prendre, avec leur impact** :

> « 6 capacités. 4 solides. La seule décision dont j'ai besoin : Recouvrement
> est-elle autonome ou une étape de Facturation ? Les données sont partagées,
> l'historique git les sépare depuis 2021. **40 % de la documentation en dépend.** »

Un gate qui présente une décision précise obtient une réponse en dix minutes. Un gate qui demande « ça vous va ? » obtient un « oui » sans valeur.

## Quand le signal est ambigu
Produire `alternative_carving` plutôt que trancher. Le Carver a le droit de ne pas savoir — il n'a pas le droit de masquer qu'il ne sait pas.
