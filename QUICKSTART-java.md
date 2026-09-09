# Premier run — projet Java

Le chemin le plus court entre « j'ai un legacy Java » et « j'ai une documentation dont je peux me servir ». Compter **30 minutes de préparation** et une demi-journée pour le run lui-même.

## 1. Installer

```
/plugin marketplace add jmellano/dmad-method
/plugin install dmad@dmad-method
```

Aucun serveur de langage à installer : `jcallgraph` est un analyseur tree-sitter, et il n'a pas besoin que le projet compile — c'est sa principale vertu sur un legacy, où la compilation est souvent le premier obstacle et parfois un obstacle définitif.

## 2. Ce qui aide, et ce qui ne bloque pas

**Le projet n'a pas besoin de compiler.** C'est la principale vertu d'un analyseur syntaxique sur un legacy, où la compilation est souvent le premier obstacle et parfois un obstacle définitif. Un projet qui ne compile pas donne un run normal.

Deux choses restent utiles quand elles sont là :

```bash
cd /chemin/vers/le/legacy
java -version                                  # renseigne profile.jdk_version
mvn -q -DskipTests dependency:go-offline       # optionnel, pour les contrats sortants
```

| Situation | Conséquence |
|---|---|
| ✅ les dépendances résolvent | les contrats sortants se résolvent au barreau 1 — le contrat qui fait foi |
| ⚠️ résolution partielle | certains contrats retombent au barreau 3, le commentaire manuscrit, **qui ment sans le dire** |
| ❌ rien ne résout | les contrats non résolus portent un placeholder visible, et une question ouverte |

**Ce n'est pas un plafond global qui se joue ici.** Depuis la v0.4, le plafond se dérive de la question posée : une hiérarchie de types reste `V` même sans dépendances résolues, un appel virtuel reste `C` même avec. Ce qui se joue, c'est la qualité des sources des contrats — et elle se mesure, ligne « contrats par barreau » du rapport de couverture.

## 3. Rassembler avant de commencer

Trois choses ne sont **pas dans le dépôt** et bloquent la qualité du run si elles manquent :

- [ ] **La configuration de production** (profils Spring, feature flags, `application-prod.yml`). Sans elle, l'anti-pattern A3 est garanti : une documentation vraie en local et fausse en production.
- [ ] **Le DDL réel ou un accès base.** Les entités JPA disent ce que le code *croit* ; la base dit ce qui *est*. Les écarts entre les deux sont de l'information de première qualité.
- [ ] **La configuration de l'ordonnanceur externe** (Control-M, $U, Rundeck) s'il y en a un. Un job qui appelle un `main()` n'apparaît nulle part dans le code.

Et une quatrième, la plus importante :

- [ ] **Le vocabulaire métier**, collecté auprès d'un humain — pas déduit du code. Cinq à vingt termes tels qu'ils sont employés en réunion. C'est le levier principal de la localisation.

Et une cinquième, propre à la v0.4 :

- [ ] **La convention de contrat d'API du dépôt** — à quoi reconnaît-on, ici, le contrat d'un appel sortant ? Quelle annotation, quel suffixe d'interface exposée, quel groupe d'artefacts. Sans elle, la résolution des contrats retombe au barreau du commentaire manuscrit, celui qui survit aux refactorings et **ment alors sans le dire**.

## 4. Lancer

```
/dmad-run
```

Le Scoper mène l'entretien de cadrage. Sa première question :
> « Dans trois semaines, qu'est-ce que vous devez pouvoir faire que vous ne pouvez pas faire aujourd'hui ? »

Réponds sérieusement : cette réponse oriente tout le run. « Faire évoluer la facturation » et « reprendre la maintenance » ne produisent pas la même documentation.

## 5. Ce qui va t'être demandé

Un arrêt par cycle, plus les gates. Ce ne sont pas des validations de politesse : ce sont les moments où dix minutes d'un humain économisent des heures d'agents.

| Arrêt | Ce qu'on te demande | Qui | Compter |
|---|---|---|---|
| **Gate 0 — Cadrage** | objectif, périmètre, vocabulaire, budget, **jusqu'où va le corpus** | commanditaire | 15 min |
| **Localisation** *(feature-scan)* | quels points d'entrée appartiennent vraiment à la fonctionnalité | commanditaire | 10 min |
| **Revue de cycle 1** | la STD est-elle juste ? | développeur | 30–45 min par document |
| **Gate 3 — Découpage** | valider ou corriger les capacités et les business objects | **expert métier** | 30–45 min |
| **Revue de cycle 2** | la SFD se contredit-elle quelque part ? | analyste + métier | 45–60 min |
| **Revue de cycle 3** | ces intentions sont-elles les bonnes ? | utilisateur métier | 45 min |

Le **gate 3 reste le plus important** : tout le fonctionnel est organisé selon ce découpage. Depuis la v0.4 il se tient **après** la revue de la STD, donc devant un expert qui vient de lire la carte technique.

**Une revue qui ne demande aucune correction est un signal d'alarme**, pas un succès : elle signifie que le relecteur n'a pas cherché, ou que le document est trop vague pour être contesté.

### Le contrôle de dix minutes, à chaque revue

Tire **cinq affirmations au hasard**, ouvre le code aux lignes citées, vérifie que la phrase correspond. C'est le seul contrôle qui détecte l'erreur dominante des modèles — citer du vrai code en lui faisant dire autre chose — parce qu'un texte crédible et bien sourcé ne déclenche aucune alarme à la lecture.

## 5bis. Choisir jusqu'où aller

DMAD produit **trois documents en cascade** : la STD par point d'entrée, la SFD par arbre de business objects, la SFG par cas d'usage. Chacun est l'abstraction du précédent, et le suivant ne démarre pas tant que le précédent n'est pas figé par sa revue.

| Corpus | Ce qu'on obtient | Qui doit être disponible |
|---|---|---|
| `[std]` | la carte technique d'un point d'entrée | un développeur |
| `[std, sfd]` | + les règles, les données, les niveaux d'abstraction | + un analyste et un référent métier |
| `[std, sfd, sfg]` | + l'intention et les cas d'usage | + un utilisateur métier |

**Pour un premier run, prends `[std]` sur un seul point d'entrée.** Le cadrage type est dans [`examples/std-seule/`](plugins/dmad/examples/std-seule/) : c'est le plus petit run qui produise un livrable défendable, et le moins cher pour mesurer le coût réel avant de s'engager.

## 6. Choisir le mode

| | Quand |
|---|---|
| `full-scan` | < 150 kLOC, ou objectif de reprise de maintenance |
| `feature-scan` | > 150 kLOC, ou l'objectif nomme un domaine (« la facturation ») |

**En cas de doute, `feature-scan`.** Une capacité documentée en entier vaut mieux que six ébauches, et c'est plus facile à défendre : « on a couvert 90 % des zones à risque de la facturation » est un résultat ; « on a survolé tout le projet » n'en est pas un.

## 7. Avant de considérer que c'est fini

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/tools/validate.py     dmad-output/
python3 ${CLAUDE_PLUGIN_ROOT}/tools/check-corpus.py dmad-output/
```

Puis **le contrôle qui compte** — dix minutes, et c'est le seul qui détecte l'erreur dominante des LLM :

> Tire 5 affirmations au hasard. Ouvre le code aux lignes citées. Vérifie que la phrase correspond.

Plus d'une erreur sur cinq condamne le run : il faut repasser le Challenger avec des consignes durcies. Une relecture intégrale ne remplace pas ce test — un texte crédible et bien sourcé ne déclenche aucune alarme à la lecture.

## Ce que tu dois obtenir

- une **STD** par point d'entrée : dix-sept sections dont aucune omise, des renvois `fichier:lignes`, une section « limites de l'analyse » — et **aucun bloc de code**
- si tu es allé plus loin, une **SFD** sans un seul nom de classe, et une **SFG** sans une seule trace de technique
- des **tests de caractérisation** qui prouvent les règles critiques — et te servent de filet pour la suite
- un **registre de questions** priorisé, prêt pour l'atelier métier
- un **rapport de couverture** honnête

## Ce que tu ne dois pas obtenir

- Une documentation qui affirme tout avec la même assurance. Si tous les chapitres sont au même niveau de confiance, quelque chose ne va pas.
- Zéro question ouverte. Sur un vrai legacy, c'est impossible — et le signe que les agents ont comblé les trous.
- Zéro finding du Challenger. Attendu : **15 à 30 %** de claims dégradées ou reformulées. Beaucoup moins signale un Challenger complaisant, pas une documentation parfaite.

---

**Note pour ce premier run :** DMAD n'a encore jamais tourné sur un vrai projet. Trois chiffres méritent d'être notés au passage — le coût réel par phase, le taux de findings du Challenger, et le résultat du contrôle par échantillonnage. Ce sont eux qui diront si la méthode tient. Détails dans [la roadmap](plugins/dmad/docs/12-roadmap.md).
