# Partie D — La dette ouverte

> Spec détaillée. Vue d'ensemble : [reste à faire](2026-09-09-dmad-reste-a-faire.md)
> **Nature** : cinq décisions à prendre, pas du code à écrire. Trois sont aggravées par la cascade v0.4.

Cette partie ne se « livre » pas : elle se tranche. Chaque point est présenté avec ses options et une recommandation, pour que l'arbitrage tienne en une séance plutôt qu'en une enquête.

---

## D1 — La signature des validations humaines

**Question ouverte n° 3 de la v0.3. La v0.4 l'aggrave nettement.**

La v0.3 avait un endroit où un humain validait quelque chose de traçable : `intent.validated_by`. La v0.4 en a **quatre** : trois revues de fin de cycle, plus le gate 3. Et la revue de cycle 3 est le **seul endroit de toute la méthode où une intention peut monter de `H` à `C`** — c'est-à-dire la seule promotion qu'un humain puisse prononcer.

Aujourd'hui, aucune de ces quatre signatures n'a de forme définie. `gate_0.approved_by` existe dans le schéma de scope, et c'est tout.

### Ce qu'il faut décider

**Qui signe.** Un nom ? Un rôle ? Les deux ? Un rôle seul (« l'expert métier ») ne permet pas de retrouver qui interroger six mois plus tard. Un nom seul vieillit mal — les gens partent, et c'est le problème même que DMAD adresse.

**Ce que la signature couvre.** Une revue de cycle valide-t-elle *le document* ou *chacune de ses claims* ? La différence est considérable : la première est tenable en quarante-cinq minutes, la seconde ne l'est pas — mais la première ne dit rien de précis, et une signature qui ne dit rien de précis n'est pas une preuve.

**Ce qu'elle devient quand le code change.** C'est la question difficile, et OKF y apporte une réponse nette que DMAD peut reprendre : *si un concept qui portait une validation est matériellement modifié, cette validation ne couvre plus ce qu'il dit maintenant — on la retire plutôt que de la laisser cautionner un texte que personne n'a relu.* C'est brutal et c'est juste.

### Recommandation

Trois niveaux de granularité, un par nature de décision :

| Objet | Granularité | Forme |
|---|---|---|
| Gate de cadrage et de découpage | le document entier | `{who, role, when, corrections[]}` |
| Revue de fin de cycle | le document, **plus** la liste des claims explicitement contestées | `{who, role, when, disputed[]}` |
| Promotion d'une intention | **la claim** | `intent.validated_by: {who, role, when, note}` |

Et la règle de péremption d'OKF, appliquée telle quelle : **une validation ne survit pas à une modification matérielle de ce qu'elle validait.** Elle est retirée, et le fait qu'elle ait existé reste dans le journal.

**Pourquoi c'est pressant** : sans cette décision, la seule promotion qu'un humain puisse prononcer n'est pas traçable, et le cycle 3 produit des intentions validées oralement — c'est-à-dire pas validées.

---

## D2 — La calibration de l'échelle

`V/C/I/H`, le seuil de trois signaux convergents sur quatre, la fourchette de 15 à 30 % de findings du Challenger, la conversion `V=100 / C=85 / I=60 / H=30` : ce sont des **conventions raisonnées, pas des mesures**. La v0.3 le disait déjà ; la v0.4 n'a rien mesuré de plus, et a ajouté une échelle — la dérivation confiance ↔ barreau de résolution — qui est dans le même cas.

### Ce qui ne peut pas être décidé en séance

Rien. **C'est la partie E qui tranche**, et elle seule. Une calibration décidée en réunion serait exactement ce que la décision D2 originelle refuse : un chiffre qui rassure sans mesurer.

### Ce qui peut être décidé maintenant

**Le protocole de mesure**, pour que le premier run produise des chiffres exploitables plutôt que des impressions. Il est spécifié en partie E.

Et une décision de présentation : **la conversion en pourcentage devrait-elle exister ?** Elle est aujourd'hui optionnelle et documentée comme une convention de lecture. Le risque est connu — un lecteur pressé retient « 85 % » et oublie que c'est une correspondance arbitraire. La supprimer coûterait peu et fermerait la porte à l'anti-pattern A7, dont elle est la version domestiquée.

---

## D3 — Le multi-dépôts

Un legacy est rarement un seul dépôt. Le schéma de scope accepte déjà `repositories` au pluriel, mais **rien dans la méthode ne dit ce que devient le graphe** : unique ou fédéré, et comment une claim d'un dépôt cite une preuve d'un autre.

La partie C attaque un cas particulier — lire une dépendance **figée**, dont on connaît la version — et ce cas est le plus fréquent. Il ne résout pas le cas général : plusieurs dépôts **vivants**, qui évoluent chacun de leur côté, et dont la fraîcheur se calcule sur des commits différents.

### Les options

| Option | Ce qu'elle donne | Ce qu'elle coûte |
|---|---|---|
| **Un graphe par dépôt**, liens inter-dépôts par référence externe | fraîcheur calculable par dépôt, run indépendant | la cascade se casse aux frontières : une SFD ne peut pas ancrer une STD d'un autre dépôt sans convention |
| **Un graphe fédéré**, un run couvrant plusieurs dépôts | la cascade tient | la fraîcheur devient multi-commits, et le périmètre explose |
| **Hors périmètre, déclaré** | honnête, coûte zéro | ferme la porte aux systèmes les plus concernés |

### Recommandation

**Un graphe par dépôt, avec une convention de référence externe** — un ancrage inter-dépôts porte le dépôt, le commit et le chemin. C'est cohérent avec le traitement des dépendances figées de la partie C, où un `ExternalContract` porte déjà sa version d'artefact : dans les deux cas, on cite quelque chose d'extérieur en disant **à quelle version** on le cite.

À trancher avant le premier run multi-dépôts, pas avant le premier run.

---

## D4 — La confidentialité

Le champ existe dans `scope.yaml` — `level`, `local_only`, `forbidden_egress`, `redaction_rules`. **Le mécanisme d'application n'est pas spécifié.** Inchangé depuis la v0.3, et bloquant pour tout usage en prestation.

### Ce qu'il faut spécifier

**`local_only: true` doit désactiver les serveurs MCP distants.** Context7 sort du réseau ; le déclarer sans le couper est une clause de style.

**Les règles `redaction_rules` doivent s'appliquer avant écriture**, pas après. Une donnée sensible écrite puis caviardée reste dans l'historique git — et l'historique git est justement ce que DMAD versionne et conserve.

**`forbidden_egress` doit être appliqué par des règles `deny`**, au même titre que la coupure du code pour les rédacteurs. Le mécanisme existe déjà et sert déjà à ça : il est disponible.

**Un point que la v0.4 ajoute** : les `evidence.excerpt` étaient le principal vecteur de fuite de code dans un document. La décision D16 les a supprimés du chemin de rédaction. La surface de risque a donc diminué — mais le graphe, lui, continue de contenir des références précises, et le bundle de la partie B les rendra plus lisibles encore.

### Recommandation

Spécifier D4 **avant** la partie B, pas après : un bundle est fait pour être lu et partagé, et il est plus facile de décider ce qu'il ne doit pas contenir avant de le construire.

---

## D5 — Le nom

« DMAD » se lit *mad* en anglais et sonne comme une parodie de BMAD. Assumé comme clin d'œil, ou à retravailler ?

La v0.4 déplace légèrement l'enjeu : la méthode ne produit plus « une documentation fonctionnelle et technique » mais un **corpus normé à trois documents**, dans un vocabulaire — STD, SFD, SFG — qui a cours dans des organisations où le clin d'œil ne se lira pas.

**À trancher avant publication, pas après.** Un renommage après diffusion coûte les liens, le marketplace, et la mémoire des gens.

---

## Ordre

| Décision | Quand | Pourquoi |
|---|---|---|
| **D1** | avant le premier cycle 3 | sinon les intentions sont validées oralement, donc pas validées |
| **D4** | avant la partie B | on décide ce qu'un bundle ne contient pas avant de le construire |
| **D2** | après le premier run | c'est lui qui mesure |
| **D3** | avant le premier run multi-dépôts | pas avant |
| **D5** | avant publication | après, c'est trop tard |

Aucune de ces cinq décisions ne bloque un premier run sur un point d'entrée unique, en `corpus: [std]` — ce qui est une raison de plus de commencer par là.
