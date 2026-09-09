# Affirmations

- [BR-FACT-014](br-fact-014.md) — Lorsque le paramètre billing.skipZeroAmount est actif, une facture dont le montant TTC est nul n'est pas transmise au SI comptable : elle est archivée avec le statut SKIPPED.
- [BR-FACT-021](br-fact-021.md) — Le montant de chaque ligne de facture est calculé avec une précision de 4 décimales et un arrondi au demi-supérieur (HALF_UP), puis stocké tel quel.
- [RISK-FACT-001](risk-fact-001.md) — Le module src/billing est le 3e hotspot du dépôt (churn x complexité) et 87 % de ses lignes sont attribuées à un unique contributeur, parti en 2023.
