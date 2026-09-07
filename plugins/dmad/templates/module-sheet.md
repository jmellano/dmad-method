<!-- TEMPLATE : fiche de module. Le format le plus consulté de la doc technique.
     Une page maximum. -->

## `{{path}}`   [{{level}}]

**Rôle** — {{role}}
**Capacité** — {{capability}}{{#if hotspot_rank}} · **Hotspot** rang {{hotspot_rank}}/20 ⚠️{{/if}}
{{#if bus_factor}}**Bus factor** — {{bus_factor}} {{#if bus_factor_alert}}⚠️{{/if}}{{/if}}

**Entrées** — {{entrypoints}}
**Sorties** — {{outputs}}
**Dépend de** — {{depends_on}}
**Dépendu par** — {{depended_by}}{{#if unexpected_coupling}} ⚠️ *{{unexpected_coupling}}*{{/if}}

**Points d'attention**
{{#each attention}}
- {{description}} → `{{claim}}`
{{/each}}

**Fichiers clés**
{{#each key_files}}
- `{{path}}:{{line}}` — {{what}}
{{/each}}

**Tests** — {{existing_tests}} existants (couverture {{coverage}} %){{#if forged}} · {{forged}} tests de caractérisation forgés par DMAD{{/if}}

<!-- Un "dépendu par" inattendu est une information architecturale de premier
     ordre : le signaler explicitement avec sa question ouverte. -->
