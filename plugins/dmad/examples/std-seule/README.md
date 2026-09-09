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
java -version                                  # doit correspondre au projet
mvn -q -DskipTests dependency:go-offline       # décide du plafond de confiance
python3 <plugin>/tools/validate.py .           # le scope est-il conforme
```

Un projet dont les dépendances ne résolvent pas n'est pas un échec : c'est un run plafonné à `I`, à condition que le plafond soit écrit dans `capabilities_available` et affiché dans le bandeau du document.

## Ce qu'on obtient

Une STD : dix-sept sections, aucune omise, aucun bloc de code — des références `fichier:lignes`, des signatures, des noms de tables. Plus le graphe, les contrats résolus avec leur barreau, les questions ouvertes et le rapport de couverture.

## Ce qu'on n'obtient pas

Aucune règle métier, aucun cas d'usage, aucune intention. Ce sont les cycles 2 et 3, et ils demandent un expert métier — pas seulement un développeur.
