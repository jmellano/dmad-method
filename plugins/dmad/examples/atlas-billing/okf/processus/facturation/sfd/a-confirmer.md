---
type: "Open Question Set"
title: "À confirmer par le métier"
description: "Les cinq points que le code ne peut pas trancher, formulés comme des questions à un humain."
tags: ["atlas", "facturation", "SFD"]
generated:
  by: "dmad-writer-sfd/0.4.0"
  at: "2026-09-08T17:00:00Z"
status: "stable"
# — extensions du profil DMAD : voir docs/14-okf.md
module: "billing"
audience: "hybride MOA/MOE"
confidence: "medium"
last_code_sync: "a1b2c3d"
renders: []
---

1. **Factures à montant nul** — règle comptable voulue, ou reliquat de l'incident d'import de 2019 ? → `BR-FACT-014` · `OQ-012`
2. **Refacturation manuelle** — doit-elle appliquer les mêmes règles ? Elle contourne aujourd'hui la garde. → `OQ-019`
3. **Précision à quatre décimales** — choix métier lié aux contrats au pourcentage, ou héritage ? → `BR-FACT-021` · `OQ-013`
4. **Clients en litige** — le report est-il indéfini ? Aucune limite trouvée. → `OQ-022`
5. **Service de tarification** — quel contrat, quelle supervision ? → `OQ-024`

# Liens

- section de : [DOC-SFD-FACT-001](../../../documents/doc-sfd-fact-001.md)
