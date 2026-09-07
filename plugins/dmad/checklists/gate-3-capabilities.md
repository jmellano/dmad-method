# Gate 3 — Découpage en capacités

**Qui valide :** un expert métier (pas un architecte seul — le découpage est une question métier).
**Durée cible :** 30 à 45 minutes.
**Ce qui se passe si on saute ce gate :** toute la documentation en aval est organisée selon un découpage faux. Ça ne se rattrape pas : ça se propage dans les six chapitres, les diagrammes et les tests.

## Comment le Carver doit présenter

Pas « voici le découpage, ça vous va ? » — cette formulation obtient un « oui » qui ne vaut rien.

Le Carver présente **des décisions précises et leur impact** :

> « 6 capacités. 4 solides, 2 fragiles. La seule décision dont j'ai besoin :
> **Recouvrement** est-elle une capacité à part ou une étape de **Facturation** ?
> Les données sont partagées, mais l'historique git les sépare depuis 2021.
> **40 % de la documentation à produire dépend de cette réponse.** »

## Vérifications

- [ ] Chaque capacité est nommée **dans le vocabulaire du métier**, pas dans celui des packages.
- [ ] Chaque capacité expose ses **4 signaux** et son `hypothesis_strength`.
- [ ] Les capacités `weak` (moins de 3 signaux convergents) sont **présentées comme telles**, avec leur découpage alternatif.
- [ ] Les **recouvrements** sont listés, pas masqués.
- [ ] Tous les **entrypoints recensés** sont rattachés à une capacité — ou explicitement déclarés orphelins.
- [ ] Toutes les **tables du périmètre** sont rattachées — ou déclarées non rattachables.
- [ ] `capabilities.yaml` valide contre `capability.schema.json`.

## Questions à poser à l'expert métier

1. « Ces six noms, ce sont les vôtres ? » — *un nom que le métier n'emploie pas signale un mauvais découpage*
2. « Il en manque une ? » — *les capacités sans code (procédures manuelles, Excel parallèles) sont invisibles pour DMAD et souvent critiques*
3. « Celle-ci, vous la pilotez séparément ? » — *le pilotage métier tranche les cas ambigus mieux que n'importe quelle métrique*
4. « Qui est responsable de celle-là ? » — *une capacité sans propriétaire est souvent deux capacités ou zéro*

## Enregistrement obligatoire

Les corrections de l'expert sont enregistrées dans `gate_3.corrections` **avec leur raison**.

C'est une source de connaissance à part entière : dans l'exemple de référence, le Carver avait proposé le bon découpage, mais l'expert l'a confirmé **pour une raison que le code ne pouvait pas donner** (le pilotage métier séparé). Cette raison vaut d'être conservée — elle éclairera le prochain arbitrage.
