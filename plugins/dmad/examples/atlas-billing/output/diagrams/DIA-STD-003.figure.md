> **Question :** que devient une facture selon l'endroit où l'exécution échoue, et que le support observe-t-il ?
> **Confiance : C — corroboré** · aucune trace d'exécution pour confirmer les fréquences

<!-- diagram: DIA-STD-003 · N=7 E=4 McCabe=1 -->
```mermaid
flowchart TD
  E1["Échec de valorisation"]
  S1["Facture non créée · lot poursuivi"]
  E2["Échec de transmission"]
  S2["Statut FAILED · reprise, 5 tentatives"]
  E3["Échec de tarification"]
  S3["Exception non déclarée · lot interrompu"]
  N["Aucune notification"]
  E1 --> S1
  E2 --> S2
  E3 --> S3
  S3 --> N
```
