<!-- TEMPLATE : le glossaire est le pont entre les deux documentations.
     C'est lui qui permet au rédacteur fonctionnel de ne jamais écrire un nom
     de classe, et au lecteur technique de retrouver le terme métier. -->

# Glossaire — {{run_id}}

| Terme métier | Dans le code | Dans la base | Définition | Confiance |
|---|---|---|---|---|
{{#each terms}}
| **{{business}}** | {{code}} | {{db}} | {{definition}} | {{level}} |
{{/each}}

## Homonymes détectés
*Termes employés dans deux sens différents. Chacun est un piège pour le lecteur.*

{{#each homonyms}}
### {{term}}
- Dans **{{context_a}}** : {{meaning_a}}
- Dans **{{context_b}}** : {{meaning_b}}

→ {{resolution}}
{{/each}}

## Termes du code sans équivalent métier
*Souvent le signe d'un concept technique, parfois celui d'un concept métier oublié.*

{{#each orphan_code_terms}}
- `{{term}}` — {{note}}
{{/each}}

## Termes métier absents du code
*Le métier en parle, le code ne les connaît pas. Trois causes : autre nom en
interne, autre système, ou processus non informatisé.*

{{#each orphan_business_terms}}
- **{{term}}** — {{hypothesis}} → `{{open_question}}`
{{/each}}
