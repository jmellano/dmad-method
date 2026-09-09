<!-- TEMPLATE SFD — spécification fonctionnelle détaillée, vue récursive par business object.
     Un document par arbre de business objects (un processus, pas un point d'entrée).
     Dérive de la STD figée et des claims. D16/D17 — ni code, ni graphe brut,
     ni nom de classe, ni nom de patron de conception. -->

---
title: "{{processus}} — spécification fonctionnelle détaillée"
type: SFD
status: "{{status}}"
module: {{module}}
processus: "{{processus}}"
audience: "{{audience}}"
cas_usage_cible: {{RUN|BUILD-EVOLUTION}}
version: "{{app_version}}"
generated_at: "{{date}}"
generated_by: "{{model}} — {{ce_qui_a_ete_fait}}"
derives_from: ["std/{{point_entree}}.md", claims]
feeds: ["sfg/{{domaine}}.md"]
last_code_sync: "{{commit_sha}}"
confidence: {{level}}
validated_by:
validated_at:
---

{{> doc-header}}

## Correspondance avec le reste du corpus

| Niveau | Couvert par la STD | Repris en SFG |
|---|---|---|
| N{{n}} — {{bo}} | [{{std}}]({{lien}}) § {{section}} | {{cas_usage}} |

---

## 1. Principe et cadre

<!-- Deux phrases. Le cadre retenu (opérations nominales et en erreur, sources et
     puits de données) et la lecture par niveaux. Pas plus : la doctrine
     s'applique, elle ne se commente pas. -->

## 2. Le processus vu comme une seule opération

{{diagramme_3_a_5_noeuds}}

## 3. Arbre de composition

{{la_decomposition_complete_sans_detail}}

<!-- C'est la carte : le lecteur voit l'empilement des niveaux d'un seul coup. -->

## 4. N{{max}} — {{nom_fonctionnel_du_business_object}}

> **{{question_a_laquelle_le_diagramme_repond}}**
> **Confiance : {{niveau}}** · {{caveats}}

{{diagramme_nomme_par_ce_quil_montre}}

### Opérations de traitement
### Opérations de contrôle
### Données de traitement — initiales
### Données de traitement — ad-hoc
<!-- Signaler les boucles qui font un appel par itération, avec leur cardinalité
     si elle est connue. C'est le signal le plus rentable du document. -->
### Données de contrôle
### Sorties normales et anormales

<!-- Les six blocs, dans cet ordre, à chaque section de niveau.
     Un bloc vide porte son constat d'absence, il ne se supprime pas. -->

## {{n}}. N0 — business objects atomiques

{{table_condensee_ou_diagramme_dedie_selon_la_logique}}

## Synthèse

| Business object | Feuilles propres | Sous-objets | Profondeur | Couche métier |
|---|---|---|---|---|

## À confirmer par le métier
<!-- Obligatoire, même vide : afficher « aucune ». -->

## Ce qui n'a pas été analysé
<!-- Obligatoire, même vide. -->
