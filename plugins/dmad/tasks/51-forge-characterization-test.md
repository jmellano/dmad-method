# Task 51 — Forger un test de caractérisation

**Agent :** `test-forger` · **Phase :** 5 · **Sortie :** `tests/characterization/`, promotions vers `V`

## Principe
Un test de caractérisation ne vérifie pas que le code est **correct**. Il documente ce qu'il **fait**, tel quel, y compris quand c'est absurde.

Dans DMAD il a une seconde fonction, plus importante : **c'est une preuve exécutable de la documentation.** Si le test qui encode la règle passe, la règle est vraie — mécaniquement, sans avoir à faire confiance à un modèle.

## Priorisation

On ne forge pas un test par claim : c'est le poste le plus coûteux de la méthode.

1. Règles à **impact réglementaire ou financier** (calculs, montants, droits, conformité)
2. Règles dans un **hotspot** — elles vont bouger, le filet servira
3. Règles **dégradées ou contestées** par le Challenger — le test tranche le débat
4. **Invariants** de capacité
5. Règles portant sur un **seam** identifié — elles sécurisent la future découpe

Le reste reste en `C` ou `I`, et c'est acceptable **à condition que ce soit affiché**.

## Écriture

```java
// BR-FACT-021
@Test
void le_montant_de_ligne_est_arrondi_au_demi_superieur_a_4_decimales() {
    OrderLine line = aLine().withUnitPrice("10.00005").withQuantity(1).build();

    BigDecimal amount = calculator.compute(line);

    assertThat(amount).isEqualByComparingTo("10.0001");
}
```

**Le nom du test est la règle métier, en français, lisible par un non-développeur.** Un métier qui lit la liste des noms de tests lit la documentation fonctionnelle exécutable du système.

Un test = une règle = une assertion. Un test qui vérifie trois choses ne prouve aucune des trois clairement.

## Arbitrage des résultats

| Résultat | Interprétation | Action |
|---|---|---|
| **Vert** | la règle est prouvée | promotion en `V`, `promoted_by: test-forger` |
| **Rouge** | trois causes possibles | **ne dégrade pas automatiquement** → question ouverte + second passage du Challenger |
| **Non exécutable** | le code résiste au test | question ouverte + entrée dans `70-seams.md` |

Un rouge signifie : la règle est fausse, **ou** le test est faux, **ou** l'environnement ne reproduit pas les conditions réelles. Les trois sont plausibles — condamner la claim automatiquement serait une erreur symétrique de celle qu'on cherche à éviter.

Le cas « non exécutable » est un **résultat précieux** : il identifie exactement où le code résiste au test, ce qui est la définition d'un seam manquant. Ces points alimentent la page des seams et deviennent des recommandations concrètes.

## Garde-fou absolu

Le Test Forger **ne modifie jamais le code de production**, même pour le rendre testable. Il décrit le seam nécessaire et le laisse à l'équipe.

DMAD documente ; il ne refactore pas. Franchir cette ligne transformerait un outil de documentation en outil de modification, avec un profil de risque radicalement différent — et retirerait au commanditaire la garantie qu'un run est sans effet de bord sur son système.
