# Gate 0 — Cadrage

**Qui valide :** le commanditaire (celui qui paie le run et lira le résultat).
**Durée cible :** 15 minutes.
**Ce qui se passe si on saute ce gate :** un run qui coûte cher et ne répond à aucune question posée. C'est le mode d'échec le plus fréquent et le plus coûteux de DMAD.

## Bloquants — le run ne démarre pas

- [ ] **L'objectif est formulé en termes de capacité d'action**, pas de livrable.
      ✅ « pouvoir changer le barème sans casser la compta »
      ❌ « avoir une documentation à jour »
- [ ] **Le périmètre est borné**, avec des exclusions écrites et justifiées.
- [ ] En `feature-scan` : **au moins 3 termes de vocabulaire métier** fournis par le commanditaire lui-même.
- [ ] **La confidentialité est tranchée** : ce qui peut sortir de la machine, ce qui reste local. Avant le premier appel d'outil, jamais après.
- [ ] **Le budget est accepté** en ordre de grandeur (temps, coût).
- [ ] `run.yaml` valide contre `scope.schema.json`.

## Avertissements — le run peut démarrer, mais le commanditaire doit avoir entendu

- [ ] **Historique git tronqué ?** → l'intention métier sera largement inaccessible : beaucoup de `H`, peu de réponses au *pourquoi*.
- [ ] **Aucun humain joignable sur le domaine ?** → les hypothèses resteront des hypothèses. DMAD produira les bonnes questions, personne ne pourra y répondre.
- [ ] **`code-intelligence` en mode dégradé ?** → annoncer maintenant le plafond de confiance du run. Une doc plafonnée à `I` est utile, mais il faut le savoir avant, pas à la livraison.
- [ ] **Aucune couverture ni trace runtime ?** → on documentera des chemins *possibles*, pas des chemins *empruntés*.
- [ ] **Objectif `audit` ou réglementaire ?** → prévenir que DMAD produit des hypothèses traçables, pas des conclusions d'audit.

## La question de contrôle

> **« Si le run se termine et produit exactement ce qui est décrit ici, est-ce que ça vous débloque ? »**

Un « oui, mais il faudrait aussi… » est le signal qu'il faut re-cadrer maintenant. Un « je ne sais pas » signifie que l'objectif n'est pas formulé.
