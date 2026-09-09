<!-- TEMPLATE STD — spécification technique détaillée, un document par point d'entrée.
     Les dix-sept sections sont dans un ordre imposé et AUCUNE ne s'omet : une section
     sans objet porte son constat d'absence et son périmètre.
     D16 — aucun bloc de code, aucune requête, aucune configuration. Des références. -->

---
title: "{{entry_point_name}} — spécification technique détaillée"
type: STD
status: "{{status}}"
module: {{module}}
entry_point_type: {{entry_point_type}}      # batch | api | consumer | cli | scheduled | soap
entry_point_name: {{entry_point_name}}
tier: {{tier}}
version: "{{app_version}}"
generated_at: "{{date}}"
generated_by: "{{model}} — {{ce_qui_a_ete_fait}}"
last_code_sync: "{{commit_sha}}"
confidence: {{level}}
derives_from: [graph, claims]
feeds: ["sfd/{{processus}}.md"]
validated_by:
validated_at:
---

<!-- Guillemets doubles obligatoires sur tout champ en phrase libre, generated_by
     en premier : il s'allonge à chaque passe et finira par contenir un ": ",
     que YAML lit comme un mapping imbriqué. Le frontmatter entier devient
     alors invalide. Valider avec un parseur avant commit. -->

{{> doc-header}}

## Correspondance avec le reste du corpus

| Ce document couvre | Vu en SFD |
|---|---|
| {{entry_point_name}} | [{{sfd_titre}}]({{sfd_lien}}) — niveaux {{niveaux}} |

---

## 1. Cartographie des composants
{{cablage}}
{{un_diagramme_de_classes_par_couche_chacun_suivi_de_sa_phrase_de_lecture}}

### 1.5 Cohésion et couplage des composants

| Composant / relation | Degré | Fait qui le prouve |
|---|---|---|
| {{composant}} | cohésion **{{degre}}** {{✔/✘}} | {{fait_deja_documente}} § {{renvoi}} |

<!-- Ordonnée du plus fort (cohésion de fonction) au plus faible (accidentelle).
     Chaque ligne CITE un fait documenté ailleurs — cette table rassemble sous le
     critère, elle ne redécouvre pas. Fait introuvable ailleurs = manque ou
     qualification faible. Seconde table pour les couplages problématiques. -->

## 2. Configuration
| Propriété | Valeur |
|---|---|

## 3. Architecture du flux
## 4. Détail par étape
<!-- Par références : signatures et fichier:lignes. Jamais d'extrait. -->
## 5. Traitement unitaire
## 6. Séquence technique
## 7. Modèle de données
**Tables lues** · **Tables écrites** · colonnes manipulées
## 8. Requêtes clés
| Référence | Tables | Colonnes | Intention |
|---|---|---|---|
<!-- Jamais le SQL lui-même. -->

## 9. Appels externes
| Code | Barreau | Artefact:version | Interface | Méthode | Contexte | Comportement d'échec |
|---|---|---|---|---|---|---|

<!-- Barreau 1 annotation de contrat (V) · 2 Javadoc (C) · 3 commentaire manuscrit (I)
     · 4 placeholder. Un contrat non résolu porte SIM_XXX_XXX_XXX et une ligne en § 14. -->

## 10. Événements
## 11. Mapping et transformations
## 12. Gestion des erreurs
<!-- Hiérarchie · propagation · exceptions métier, techniques, NON DÉCLARÉES ·
     sources d'infrastructure · sémantique de la reprise · sorties dégradées ·
     chemins inatteignables et pièges d'attribution.
     Séparer systématiquement le SITE DE LEVÉE et l'EFFET OBSERVABLE : ce ne
     sont pas le même fait, et les confondre crée des contradictions qui
     deviendront des promesses fausses en SFG. -->
## 13. Dépendances
## 14. Points d'attention pour le développeur
## 15. Cas de test
## 16. Références croisées
## 17. Historique

---

## Limites de cette analyse
<!-- Obligatoire. Profondeur de traversée, frontières atteintes, dispatchs non
     résolus, absence de traces runtime, modules hors périmètre. C'est ce qui
     distingue une documentation professionnelle d'une génération automatique. -->
