# Premier run — projet Java

Le chemin le plus court entre « j'ai un legacy Java » et « j'ai une documentation dont je peux me servir ». Compter **30 minutes de préparation** et une demi-journée pour le run lui-même.

## 1. Installer

```
/plugin marketplace add jmellano/dmad-method
/plugin install dmad@dmad-method
```

Serena a besoin de `uv` :
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## 2. Rendre le projet analysable — l'étape qui décide de tout

`code-intelligence` a besoin que le projet **résolve ses dépendances**. C'est le premier obstacle sur un legacy, et il conditionne le plafond de confiance du run.

```bash
cd /chemin/vers/le/legacy
java -version                                  # doit correspondre au projet
mvn -q -DskipTests dependency:go-offline       # ou ./gradlew --offline compileJava
```

| Résultat | Conséquence |
|---|---|
| ✅ ça compile | run nominal, plafond `V` |
| ⚠️ dépendances partielles | `find_references` incomplet ⇒ **aucune affirmation d'exhaustivité**, plafond `I` |
| ❌ rien ne résout | mode dégradé (tree-sitter/grep), plafond `I` — utilisable, mais à annoncer |

**Un projet qui ne compile pas n'est pas un échec.** C'est un run plafonné, et le plafond doit être écrit dans le cadrage et affiché dans la documentation produite.

## 3. Rassembler avant de commencer

Trois choses ne sont **pas dans le dépôt** et bloquent la qualité du run si elles manquent :

- [ ] **La configuration de production** (profils Spring, feature flags, `application-prod.yml`). Sans elle, l'anti-pattern A3 est garanti : une documentation vraie en local et fausse en production.
- [ ] **Le DDL réel ou un accès base.** Les entités JPA disent ce que le code *croit* ; la base dit ce qui *est*. Les écarts entre les deux sont de l'information de première qualité.
- [ ] **La configuration de l'ordonnanceur externe** (Control-M, $U, Rundeck) s'il y en a un. Un job qui appelle un `main()` n'apparaît nulle part dans le code.

Et une quatrième, la plus importante :

- [ ] **Le vocabulaire métier**, collecté auprès d'un humain — pas déduit du code. Cinq à vingt termes tels qu'ils sont employés en réunion. C'est le levier principal de la localisation.

## 4. Lancer

```
/dmad-run
```

Le Scoper mène l'entretien de cadrage. Sa première question :
> « Dans trois semaines, qu'est-ce que vous devez pouvoir faire que vous ne pouvez pas faire aujourd'hui ? »

Réponds sérieusement : cette réponse oriente tout le run. « Faire évoluer la facturation » et « reprendre la maintenance » ne produisent pas la même documentation.

## 5. Ce qui va t'être demandé

Trois à quatre arrêts. Ce ne sont pas des validations de politesse : ce sont les moments où dix minutes d'un humain économisent des heures d'agents.

| Gate | Ce qu'on te demande | Compter |
|---|---|---|
| **0 — Cadrage** | objectif, périmètre, vocabulaire, budget | 15 min |
| **1b — Localisation** *(feature-scan)* | quels points d'entrée candidats appartiennent vraiment à la fonctionnalité | 10 min |
| **3 — Découpage** | valider ou corriger les capacités métier proposées | 30–45 min, **avec un expert métier** |
| **5 — Challenge** | arbitrer les contradictions et les tests rouges | variable |

Le **gate 3 est le plus important** : tout ce qui suit est organisé selon ce découpage. Un expert métier y corrige en trente minutes ce que des heures d'agents auraient mal deviné.

## 6. Choisir le mode

| | Quand |
|---|---|
| `full-scan` | < 150 kLOC, ou objectif de reprise de maintenance |
| `feature-scan` | > 150 kLOC, ou l'objectif nomme un domaine (« la facturation ») |

**En cas de doute, `feature-scan`.** Une capacité documentée en entier vaut mieux que six ébauches, et c'est plus facile à défendre : « on a couvert 90 % des zones à risque de la facturation » est un résultat ; « on a survolé tout le projet » n'en est pas un.

## 7. Avant de considérer que c'est fini

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/tools/validate.py dmad-output/
```

Puis **le contrôle qui compte** — dix minutes, et c'est le seul qui détecte l'erreur dominante des LLM :

> Tire 5 affirmations au hasard. Ouvre le code aux lignes citées. Vérifie que la phrase correspond.

Plus d'une erreur sur cinq condamne le run : il faut repasser le Challenger avec des consignes durcies. Une relecture intégrale ne remplace pas ce test — un texte crédible et bien sourcé ne déclenche aucune alarme à la lecture.

## Ce que tu dois obtenir

- une **documentation fonctionnelle** sans un seul nom de classe, avec un niveau de preuve par affirmation
- une **documentation technique** avec renvois `fichier:lignes` et une section « limites de l'analyse »
- des **tests de caractérisation** qui prouvent les règles critiques — et te servent de filet pour la suite
- un **registre de questions** priorisé, prêt pour l'atelier métier
- un **rapport de couverture** honnête

## Ce que tu ne dois pas obtenir

- Une documentation qui affirme tout avec la même assurance. Si tous les chapitres sont au même niveau de confiance, quelque chose ne va pas.
- Zéro question ouverte. Sur un vrai legacy, c'est impossible — et le signe que les agents ont comblé les trous.
- Zéro finding du Challenger. Attendu : **15 à 30 %** de claims dégradées ou reformulées. Beaucoup moins signale un Challenger complaisant, pas une documentation parfaite.

---

**Note pour ce premier run :** DMAD n'a encore jamais tourné sur un vrai projet. Trois chiffres méritent d'être notés au passage — le coût réel par phase, le taux de findings du Challenger, et le résultat du contrôle par échantillonnage. Ce sont eux qui diront si la méthode tient. Détails dans [la roadmap](plugins/dmad/docs/12-roadmap.md).
