<!-- TEMPLATE : la sortie actionnable. La documentation n'est pas la finalité —
     pouvoir modifier le système l'est. -->

# Points de découpe (seams)

Un *seam* est un endroit où le comportement peut être modifié sans réécrire le code
autour ([Feathers](https://www.oreilly.com/library/view/working-effectively-with/0131177052/)).
Cette page liste ceux qui ont été identifiés, avec ce qu'ils permettent et ce
qu'ils coûtent.

{{#each seams}}
## {{isolates}}

**Point de coupe** — `{{at}}`
**Traversé par** — {{crossed_by}} appels {{#if callers}}({{callers}}){{/if}}
**Effort estimé** — {{estimated_effort}}
**Capacité** — {{capability}} {{#if hotspot_rank}}· hotspot rang {{hotspot_rank}}{{/if}}

**Ce que ça permet**
{{enables}}

**Ce qui traverse aujourd'hui**
{{#each crossings}}
- {{this}}
{{/each}}

**Filet nécessaire avant l'opération**
{{#each blocking_tests_needed}}
- `{{id}}` — {{statement}} {{#if forged}}✅ test forgé{{else}}⚠️ **à forger**{{/if}}
{{/each}}

{{#if risks}}
**Risques**
{{#each risks}}
- {{this}}
{{/each}}
{{/if}}

---
{{/each}}

## Ce que DMAD ne fait pas

DMAD **documente** les seams ; il ne les crée pas et ne refactore pas. Le choix
de découper, quand et comment, appartient à l'équipe. Cette page fournit la
matière de la décision : ce qui est isolable, à quel coût, et avec quel filet.
