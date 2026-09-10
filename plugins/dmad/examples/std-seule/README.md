# Cadrage type — un point d'entrée, la STD seule

Le plus petit run DMAD qui produise un livrable défendable : **un point d'entrée, un document, une revue humaine**.

## Pourquoi commencer par là

Trois raisons, dans l'ordre où elles comptent.

**Le cycle 1 est le seul entièrement mécanique.** Inventaire, graphe d'appels, contrats sortants : tout y est outillé, donc peu coûteux en modèle fort et peu exposé à l'hallucination. C'est le cycle où le rapport valeur/risque est le meilleur.

**La STD est le socle de tout le reste.** La cascade veut que la SFD lise la STD figée, et la SFG la SFD figée. Une STD non revue empoisonne les deux étages au-dessus, en gagnant en abstraction — donc en devenant plus difficile à réfuter à chaque étage.

**C'est ce qui permet de mesurer avant de s'engager.** Un point d'entrée donne le coût réel par cycle, le taux de findings du Challenger et le résultat du contrôle par échantillonnage. Ces trois chiffres décident s'il faut lancer le corpus complet — et ils n'existent pas tant qu'un run réel n'a pas eu lieu.

## Ce que le cadrage a de particulier

**`corpus: [std]`** — on ne demande qu'un document. Enchaîner sur la SFD exigera que la STD soit figée par une revue.

**`known_entrypoints` renseigné** — l'étape de localisation et son gate sont sautés. On sait déjà où regarder ; les cinq sondes ne servent qu'à trouver ce qu'on cherche.

**`profile.contract_convention` renseigné** — c'est le seul bloc dont l'absence dégrade silencieusement le résultat. Sans lui, la résolution des contrats sortants retombe au barreau 3, le commentaire manuscrit, qui survit aux refactorings et ment alors sans le dire.

## Avant de lancer

```bash
java -version                                  # renseigne profile.jdk_version
mvn -q -DskipTests dependency:go-offline       # optionnel : résout les contrats au barreau 1
python3 <plugin>/tools/validate.py .           # le cadrage est-il conforme
```

Un projet dont les dépendances ne résolvent pas n'est pas un échec : c'est un run plafonné à `I`, à condition que le plafond soit écrit dans `capabilities_available` et affiché dans le bandeau du document.

## L'arborescence que le run produira

```
dmad-output/
├── run.yaml · PERIMETRE.txt · index.md
├── conduite/          gates, contrôles, incidents, quarantaine, couverture
├── socle/             ce qui survivrait à ce processus
├── processus/<p>/     preuves/, diagrammes/, std/, plan-std.yaml
└── documents/         STD-<processus>.md
```

Le sujet vient avant la nature (D27) : `processus/<p>/preuves/claims/`, pas `claims/`. Sur un run mono-processus c'est un niveau de plus ; c'est ce qui rend le deuxième processus lisible.

## Ce qu'on obtient

Une STD : onze chapitres, aucun omis, aucun bloc de code — des références `fichier:lignes`, des signatures, des noms de tables. Plus le graphe, les contrats résolus avec leur barreau, les questions ouvertes et le rapport de couverture.

## Ce qu'on n'obtient pas

Aucune règle métier, aucun cas d'usage, aucune intention. Ce sont les cycles 2 et 3, et ils demandent un expert métier — pas seulement un développeur.
