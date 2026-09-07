# Task 60 — Planifier les diagrammes

**Agent :** `diagram-planner` · **Phase :** 6 · **Sortie :** `diagram-plan.yaml`

## Procédure

1. **Lister les questions** auxquelles un lecteur voudra répondre, par public (métier / technique).
2. **Associer un type** de diagramme à chaque question (catalogue : `docs/06-diagrammes.md`).
3. **Extraire le sous-graphe** minimal qui y répond.
4. **Vérifier le seuil** de lisibilité. Au-dessus : découper en plusieurs questions, ne pas simplifier.
5. **Hériter la confiance** du niveau le plus bas du sous-graphe.
6. **Déléguer le rendu** au `diagram-engine`. Le planner n'écrit jamais de syntaxe.

## Les questions par défaut

**Fonctionnel** — À quoi sert le système, pour qui ? · Comment se déroule ce cas d'usage ? · Que se passe-t-il quand ça se passe mal ? · Quel est le cycle de vie de cet objet ? · Quelles données manipule-t-on ?

**Technique** — De quoi dépend-on ? · Comment est-ce structuré ? · Qu'est-ce qui appelle quoi depuis cette entrée ? · Où sont les ports et adaptateurs ? · Quelles API externes ? · Où est le risque ?

## Seuils

| Type | Seuil | Au-delà |
|---|---|---|
| Classes | 15 nœuds | découper par sous-domaine |
| Séquence | 12 participants / 25 messages | découper par phase |
| C4 composants | 20 | monter d'un niveau ou découper |
| ERD | 20 tables | découper par capacité |
| Call graph | profondeur 3 / 25 nœuds | borner ou changer de racine |
| États | 12 états | **re-vérifier le modèle** |

Le dernier cas n'est pas un problème de mise en page : une machine à 20 états dans un legacy signale presque toujours que **plusieurs automates distincts ont été fusionnés** (l'état de la facture et l'état de son export, par exemple). Le dépassement déclenche une re-vérification.

## Journal des refus

```yaml
refused:
  - kind: class_diagram
    scope: global
    reason: "412 classes — hairball. Découpé en 6 diagrammes par capacité."
  - kind: state_machine
    scope: Order
    reason: "aucun champ d'état détecté ; transitions non repérables → OQ-024"
```

Le second cas est le plus important : **un diagramme refusé faute de preuve devient une question ouverte**, pas un blanc silencieux dans le document.
