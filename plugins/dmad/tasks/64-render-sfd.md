# Task 64 — Rendre la SFD

**Agent :** `writer-sfd` · **Cycle :** 2 · **Sortie :** `dmad-output/sfd/<processus>.md`

## Ce qui est lu

**La STD figée et les claims validées.** Pas le code, pas le graphe brut (D17). Une information absente de la STD ne peut pas apparaître ici — le trou se propage visiblement plutôt que d'être comblé.

## Un document par arbre de business objects

Un processus, pas un point d'entrée. Plusieurs points d'entrée peuvent alimenter le même arbre ; la table de correspondance en tête le dit.

## Analyser bas → haut, rédiger haut → bas

L'analyse est partie des feuilles. **La rédaction part du sommet.** Confondre les deux produit un document où le lecteur se noie dans le détail avant d'avoir le contexte.

1. **Principe et cadre** — deux phrases sur le cadre retenu et la lecture par niveaux.
2. **Niveau le plus haut** — le processus comme une seule opération, avec ses entrées et sorties externes. Trois à cinq nœuds.
3. **Arbre de composition** — la décomposition complète, sans détail. C'est la carte : le lecteur voit l'empilement d'un seul coup.
4. **Niveaux intermédiaires, en ordre décroissant** — un ou deux diagrammes par niveau, prose en complément.
5. **Niveau le plus bas** — les BO qui n'invoquent que des feuilles. Table condensée si la logique est triviale, diagramme dédié si elle porte du conditionnel intéressant.
6. **Synthèse** — la table à toutes les colonnes : BO, feuilles propres, sous-objets, profondeur récursive, couche métier.

## Le gabarit six blocs, par section de niveau

Traitement · contrôle · données initiales · données ad-hoc · données de contrôle · sorties normales et anormales. Un bloc vide porte son constat d'absence.

Deux distinctions à ne jamais fondre : **traitement contre contrôle** change ce qu'on documente d'une opération ; **initiale contre ad-hoc** est le signal le plus rentable pour qui cherche une optimisation. Signaler les boucles qui font un appel ad-hoc par itération.

## Diagrammes d'abord

Le texte ne sert qu'à ce qui nuirait à la lisibilité du diagramme : contraintes, notes de bord, exceptions rares, ancrages vers la STD.

Un diagramme est nommé **par ce qu'il montre**, jamais par son type. « Diagramme de séquence 3 » ne dit rien ; « Échanges du calcul avec les services amont » dit à quoi sert la figure avant qu'on la regarde.

## Interdits

Blocs de code, requêtes, noms de classes, noms de méthodes, jargon de framework, **noms de patrons de conception**. Le patron a servi à découper ; il n'a rien à faire dans le document.

## Glossaire imposé

Chaque identifiant de framework ou de table rencontré dans une claim se traduit avant d'être écrit. Constituer la table une fois par processus et la rejouer à chaque passe.

## Table de correspondance

En tête : quelle STD couvre quel niveau, et quelle SFG dérive de ce document.
