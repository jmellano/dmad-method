<!-- TEMPLATE : un cas d'usage. Structure attaquable étape par étape par le
     Challenger, et rendable sans relire le code. -->

### {{label}}   {{badge}}

**Déclencheur** — {{trigger}}
**Acteur** — {{actor}}

{{#if preconditions}}
**Pour que ça démarre**
{{#each preconditions}}
- {{this}}
{{/each}}
{{/if}}

**Déroulement**
{{#each nominal_flow}}
{{step_number}}. {{step}}
   {{#if rules}}*Règles appliquées : {{rules}}*{{/if}}
{{/each}}

{{#if alternate_flows}}
**Cas particuliers**
{{#each alternate_flows}}
- **{{condition}}** → {{outcome}} {{badge}}
{{/each}}
{{/if}}

**À la fin**
{{#each postconditions}}
- {{this}}
{{/each}}

{{#if side_effects}}
**Effets de bord**
{{#each side_effects}}
- {{this}}
{{/each}}
{{/if}}

{{#if open_questions}}
> ⚠️ **À confirmer :** {{open_questions_prose}}
{{/if}}

<!-- Test de qualité : un lecteur métier doit pouvoir lire ce cas d'usage
     sans jamais rencontrer un nom de classe. -->
