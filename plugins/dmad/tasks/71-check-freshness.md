# Task 71 — Vérifier la fraîcheur

**Agent :** `curator` · **Phase :** 7 · **Récurrent**

## Principe
Chaque claim porte `freshness.verified_at_commit` et des `evidence` en `fichier#Llignes`. Le code bouge ; la documentation doit savoir ce qui ne tient plus.

Sans cette boucle, DMAD produit une photo qui jaunit. Avec elle, une documentation vivante.

## Procédure

```bash
git diff <verified_at_commit>..HEAD --name-only
```

Pour chaque claim dont un fichier de preuve a changé :

```bash
git diff <commit>..HEAD -- <fichier>   # les lignes citées ont-elles bougé ?
```

| État | Condition | Action |
|---|---|---|
| `fresh` | lignes citées inchangées | — |
| `shifted` | lignes déplacées, contenu identique | mise à jour automatique des références |
| `stale` | contenu modifié | re-soumission au pipeline (phases 4–5 sur la claim) |
| `broken` | fichier supprimé ou renommé | alerte + re-cartographie du secteur |

La distinction `shifted` / `stale` évite le bruit : un ajout de 10 lignes en début de fichier ne périme pas 40 claims, il décale leurs références.

## Intégration CI

```yaml
- name: DMAD freshness
  run: python3 dmad/tools/freshness.py --fail-over 15%
```

Le job échoue quand plus de 15 % des claims d'une capacité passent en `stale`. Ce n'est pas un blocage de merge : c'est un signal que la documentation de cette capacité mérite un passage.

## Le bon réglage
Un seuil trop bas produit du bruit à chaque refactoring et sera désactivé au bout de trois semaines. Le but n'est pas de bloquer les développeurs : c'est de **rendre visible la dérive** avant qu'elle ne rende la documentation inutilisable.
