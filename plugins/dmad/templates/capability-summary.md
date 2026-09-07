<!-- TEMPLATE : chapitre fonctionnel d'une capacité -->

<!-- {{level}} = MINIMUM des `statement` du chapitre.
     Les `intent` sont exclus du calcul : ils sont tous en H par construction,
     les inclure badgerait tout chapitre en H et rendrait l'échelle inutile.
     Chaque intention porte son marquage H au fil du texte. -->
# {{label}}   [{{level}} · {{level_name}} · {{claims_count}} affirmations · {{to_confirm}} à confirmer]

## En une phrase
{{one_liner}}

## Ce que fait le système

{{#each use_cases}}
### {{label}}
**Déclencheur** — {{trigger}}
**Qui** — {{actor}}

{{nominal_flow_prose}}

{{#if alternate_flows}}
**Cas particuliers**
{{#each alternate_flows}}
- {{condition}} → {{outcome}} {{badge}}
{{/each}}
{{/if}}
{{/each}}

## Les règles appliquées

{{#each rules}}
**{{statement}}** {{badge}}
{{#if conditional_on}}
> ⚠️ Ce comportement dépend du paramètre `{{conditional_on.key}}` : {{conditional_on.observed_prose}}
{{/if}}
{{#if intent}}
> *Raisonnement supposé : {{intent.statement}}* **[H — à confirmer]**
{{/if}}
{{/each}}

## Le parcours

{{#each diagrams}}
> **Question :** {{question}}
> **Confiance : {{level}}** {{#if caveats}}· {{caveats}}{{/if}}

{{rendered}}
{{/each}}

## Les données manipulées
{{data_prose}}

## ⚠️ À confirmer par le métier
{{#each open_questions}}
{{index}}. **{{short_title}}** — {{question}}
   → *impact si on se trompe : {{impact}}* · `{{related_claims}}` · `{{id}}`
{{else}}
Aucune. Toutes les règles de cette capacité sont établies ou corroborées.
{{/each}}

## Ce qui n'a pas été analysé
{{#each boundaries}}
- {{description}} ({{reason}})
{{else}}
Aucune frontière de traversée atteinte sur cette capacité.
{{/each}}

<!-- Les deux dernières sections ne sont JAMAIS omises, même vides.
     Une section absente se lit "rien à signaler".
     Une section vide et assumée se lit "on a regardé". -->
