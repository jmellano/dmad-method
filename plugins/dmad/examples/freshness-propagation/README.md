# Fixture — la péremption remonte la cascade

Le contrôle que la v0.4 ajoute à la fraîcheur, isolé pour être vérifiable.

Une seule claim a bougé : `BR-PROP-001`, publiée par la STD. Rien d'autre n'a
changé. Pourtant **les trois documents doivent ressortir périmés**, parce que la
SFD dérive de la STD et la SFG de la SFD.

Sans cette propagation, la SFG resterait marquée fraîche alors que son socle a
bougé — et c'est le pire cas possible : **le document le plus cru est le plus
périmé**, et son lecteur est celui qui a le moins de moyens de s'en apercevoir.
Il n'a ni le code, ni le graphe, ni la STD.

```bash
python3 ../../tools/freshness.py .          # trois documents périmés, deux par héritage
python3 ../../tools/freshness.py . --strict # sort en erreur
```
