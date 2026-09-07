<!-- TEMPLATE : registre consolidé. C'est l'ordre du jour de l'atelier métier,
     souvent le livrable le plus immédiatement rentable d'un run DMAD. -->

# Questions ouvertes — {{run_id}}

{{total}} questions · **{{p1_count}} prioritaires**
Répondre aux P1 ferait passer {{promotable_count}} affirmations d'hypothèse à fait établi.

---

## P1 — À trancher en priorité
*Impact réglementaire ou financier, et confiance actuelle faible.*

{{#each p1}}
### {{id}} — {{short_title}}
**Public :** {{audience}} · **Capacité :** {{capability}}

{{question}}

**Ce que fait le système aujourd'hui**
{{context}}

**Pourquoi ça compte**
{{why_it_matters}}

**Réponses possibles**
{{#each options}}
- {{this}}
{{/each}}

*Concerne :* {{related_claims}}

---
{{/each}}

## P2 — Bloque la compréhension d'une capacité
{{#each p2}}
- **{{id}}** — {{question}} *({{audience}})*
{{/each}}

## P3 — Règle isolée
{{#each p3}}
- **{{id}}** — {{question}}
{{/each}}

## P4 — Curiosité historique
*Sans effet sur les décisions. Listées pour mémoire.*
{{#each p4}}
- **{{id}}** — {{question}}
{{/each}}

---

## Comment utiliser ce document

Ce registre est fait pour être **traité en atelier**, pas lu. Les questions sont
fermées (avec des options) parce qu'une question ouverte obtient un silence et
une question fermée obtient une réponse.

Chaque réponse enregistrée dans `answer` fait remonter le niveau de confiance
des claims associées — c'est le seul mécanisme qui fait sortir une intention
du niveau `H`.
