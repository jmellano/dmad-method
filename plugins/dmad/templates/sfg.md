<!-- TEMPLATE SFG — spécification fonctionnelle générale, découpée par cas d'usage.
     Dérive de la SEULE SFD figée (D17). Aucun nom de composant, d'application,
     de table ou de code technique hors du bloc traçabilité. -->

---
title: "{{domaine}} — règles métier par cas d'usage"
type: SFG
status: "{{status}}"
module: {{module}}
domaine: "{{domaine}}"
audience: "{{les_personnes_pas_un_role_projet}}"
unite_evolution: "cas d'usage"
version: "{{app_version}}"
generated_at: "{{date}}"
generated_by: "{{model}} — {{ce_qui_a_ete_fait}}"
derives_from: ["sfd/{{processus}}.md"]
last_code_sync: "{{commit_sha}}"
confidence: {{level}}
validated_by:
validated_at:
---

{{> doc-header}}

## Note d'audience

<!-- À qui s'adresse ce document, ce qu'on n'y trouvera pas et où c'est écrit,
     comment il est organisé ET POURQUOI, son statut.
     C'est le seul endroit où la doctrine du cas d'usage est expliquée au
     lecteur ; ailleurs elle est appliquée, pas commentée. -->

## Ce que le domaine résout

<!-- Le problème métier en une page, SANS le système. Un lecteur qui s'arrête
     ici doit avoir compris à quoi sert la chose. -->

## Invariants du domaine

| Invariant | Intention | Ce que l'utilisateur voit |
|---|---|---|
| INV-{{n}} — {{enonce}} | {{intention}} {{marquage_H_si_non_validee}} | {{effet}} |

---

## CU-{{nn}} — {{titre_du_cas_usage}}

### Situation
<!-- Ce que le lecteur reconnaît : qui commande, qui est livré, qui paye.
     Piège : décrire le système au lieu de la situation. -->

### Acteurs et rôles métier
<!-- Des personnes et des entités. Piège : glisser un nom d'application. -->

### Déclencheur et cadence
<!-- Ce qui lance, à quelle fréquence, AVEC LE FUSEAU HORAIRE.
     Format : HH:MM:SS <ZoneId>. « Chaque nuit » est inutilisable. -->

### Règles applicables

| Règle | Intention | Ce que l'utilisateur voit |
|---|---|---|
| RG-{{n}} — {{enonce}} | {{intention}} {{marquage_H}} | {{effet}} |

<!-- Ne pas factoriser vers un autre cas d'usage. Une règle partagée a une
     décision écrite : soit elle remonte en invariant, soit elle est
     contextualisée dans chacun. -->

### Ce que l'utilisateur voit
<!-- En succès ET en échec. L'échec est le cas le plus consulté. -->

### Ce qui n'est pas couvert
<!-- LE BLOC QU'ON OUBLIE, et le plus structurant. Un cas d'usage dont la
     frontière n'est pas écrite ne peut être l'unité d'évolution de rien :
     personne ne saura si une demande tombe dedans ou à côté.
     Ne peut pas être vide. -->

### Traçabilité

| Règle | Section SFD |
|---|---|

<!-- Le seul endroit du document où les identifiants ont droit de cité. -->

---

## Index inverse — règle → cas d'usage

<!-- GÉNÉRÉ, jamais édité. Compter les règles du corps et les entrées de
     l'index : un écart est un défaut, pas un arrondi. -->

## Constats

<!-- Distinguer ce qui relève de la méthode et ce qui attend un arbitrage.
     Chaque arbitrage énonce ses options. -->

## Historique

| Date | Version | Nature |
|---|---|---|

<!-- Y consigner explicitement les CORRECTIONS FACTUELLES, avec ce qui était
     écrit et pourquoi c'était faux : c'est la seule trace qu'un relecteur
     aura de la fiabilité du document. -->
