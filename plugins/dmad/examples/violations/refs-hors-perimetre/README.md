# Fixture — une preuve qui déborde de son fichier

Le contrôle de plage ne s'exécute qu'avec `--code`, parce qu'il a besoin de la racine du
code analysé. Il vit donc dans son propre dossier : passer `--code` sur les autres
fixtures ferait échouer toutes leurs références, qui pointent un code fictif.

```bash
python3 ../../../tools/validate.py . --code .
```

`src/Fixture.java` fait dix lignes ; la preuve cite `L300-L400`. C'est exactement la
forme qu'avait la cartographie faite dans une copie hors périmètre lors du premier run
réel : le fichier existait, le nom de classe était le bon, et seules les lignes
trahissaient qu'on lisait une autre arborescence.

**Le contrôle attrape le symptôme, pas la cause.** Une copie de la même longueur
passerait. C'est la liste fermée du périmètre qui ferme la porte.
