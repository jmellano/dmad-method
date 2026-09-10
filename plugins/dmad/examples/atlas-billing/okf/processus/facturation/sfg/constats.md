---
type: "Findings"
title: "Ce que la rédaction a révélé"
description: "Constats de méthode et arbitrages attendus, chacun avec ses options."
tags: ["atlas", "facturation", "SFG"]
generated:
  by: "dmad-writer-sfg/0.4.0"
  at: "2026-09-08T17:00:00Z"
status: "draft"
# — extensions du profil DMAD : voir docs/14-okf.md
module: "billing"
audience: "Utilisateurs métier"
confidence: "medium"
unite_evolution: "cas d'usage"
last_code_sync: "a1b2c3d"
renders: []
---

**De méthode.** Le découpage initial suivait les deux points d'entrée techniques. Il a fallu écrire les deux sections en entier pour voir que la vraie ligne de partage n'est pas là : ce qui distingue CU-01 de CU-02 n'est pas le déclencheur mais **le jeu de règles appliqué**. Un cas d'usage se découpe par ce qui évolue ensemble.

**Arbitrage attendu — RG-003 et RG-004.** Deux chemins produisent des résultats différents pour la même facture. Trois options : aligner la refacturation sur la campagne, documenter l'échappatoire comme volontaire, ou supprimer la règle des deux côtés si l'incident de 2019 n'a plus lieu d'être. La réponse à `OQ-012` décide des trois.

**Arbitrage attendu — RG-002.** L'intention n'a pas pu être validée : personne dans l'équipe actuelle ne sait pourquoi la précision est passée à quatre décimales en 2017. Le commit existe, son auteur est parti. Soit on l'accepte comme une contrainte héritée, soit on la requestionne avant le changement de barème.

# Liens

- section de : [DOC-SFG-FACT-001](../../../documents/doc-sfg-fact-001.md)
