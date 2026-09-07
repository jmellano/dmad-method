<!-- TEMPLATE : bandeau obligatoire en tête de CHAQUE document généré.
     Ce n'est pas une clause de style : c'est ce qui empêche la doc de devenir,
     dans six mois, une source de vérité qu'on cite sans la questionner. -->

> **Documentation générée par DMAD** · run `{{run_id}}` · `{{timestamp}}` · commit `{{commit}}`
> **Périmètre :** {{mode}} « {{feature_label}} » — {{coverage_files}} % du code atteint, {{coverage_hotspots}} % des zones à risque
> **Confiance globale : {{level}}** (minimum des chapitres) · {{open_questions_count}} questions ouvertes
>
> ⚠️ Cette documentation est **reconstruite depuis le code**. Chaque affirmation porte
> son niveau de preuve : **V** vérifié · **C** corroboré · **I** inféré · **H** hypothèse
> à valider. Ne prenez pas une affirmation `I` ou `H` pour une décision métier établie.
>
> {{#if degraded_capabilities}}
> ⚠️ **Outillage dégradé :** {{degraded_list}} — la confiance de ce run est plafonnée à `{{ceiling}}`.
> {{/if}}
