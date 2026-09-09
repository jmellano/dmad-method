# Definition of Done — un diagramme

- [ ] **Une question est formulée** et affichée au-dessus du diagramme dans la documentation.
- [ ] **Le seuil de lisibilité est respecté** (classes 15 · séquence 12 participants · C4 20 · ERD 20 · call graph profondeur 3 / 25 nœuds · états 12).
- [ ] **Généré depuis le graphe**, jamais rédigé à la main. Un diagramme écrit directement ne peut pas être vérifié contre les claims.
- [ ] **Badge de confiance présent**, hérité du niveau le plus bas de son sous-graphe.
- [ ] **Les caveats sont affichés** : chemins non explorés, frontières atteintes, dispatchs non résolus.
- [ ] **Format Mermaid** sauf nécessité justifiée (PlantUML pour l'UML fin, Graphviz pour les grands graphes).
- [ ] **Le diagramme compile réellement** — rendu vérifié par un moteur, pas relu.
      Un diagramme qui ne compile pas ne rend **rien** et l'échec est silencieux côté
      GitHub/GitLab : il est indiscernable d'un diagramme absent. Premier run réel :
      4 diagrammes sur 47 étaient cassés et invisibles à la relecture.
      Pièges rencontrés : parenthèses dans un libellé de `flowchart` · parenthèses et
      deux-points dans un `gantt` · `linkStyle N` avec N ≥ nombre d'arêtes · **point-virgule
      dans un message de `sequenceDiagram`** · même paire de relations déclarée deux fois
      dans un `erDiagram`.
- [ ] **Le vocabulaire correspond au public** : métier dans la doc fonctionnelle, noms réels dans la doc technique.

## Refus systématiques

| Cas | Raison | À la place |
|---|---|---|
| Diagramme de classes global | hairball illisible | un par capacité |
| Machine à états sans champ d'état réel | automate inventé | question ouverte |
| Séquence de plus de 25 messages | personne ne la lit | découper par phase |
| Diagramme sans question | illustration, pas documentation | supprimer |
| Call graph non borné | explose au-delà de 3 niveaux | borner ou changer de racine |

## Le cas de la machine à états à 20 états

Ce n'est pas un problème de lisibilité : c'est un **signal de qualité**. Un legacy réel a rarement un automate à 20 états cohérent. Le dépassement signifie presque toujours que l'agent a **fusionné plusieurs automates distincts** (par exemple l'état de la facture et l'état de son export).

Le dépassement déclenche donc une **re-vérification**, pas un découpage cosmétique.
