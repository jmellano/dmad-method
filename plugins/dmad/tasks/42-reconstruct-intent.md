# Task 42 — Reconstituer l'intention

**Agent :** `archaeologist` · **Phase :** 4 · **Sortie :** blocs `intent` (plafond `H`)

## Principe
Le code dit *quoi*, jamais *pourquoi*. L'intention se reconstruit à partir de traces, et reste une hypothèse jusqu'à validation humaine — **sans exception**.

## Procédure pour une règle donnée

```bash
git log -L <début>,<fin>:<fichier>      # histoire des lignes exactes
git log --grep="<mot-clé métier>"
git log -S "<constante ou seuil>"       # quand la valeur magique est apparue
git blame -w -C -C <fichier>            # en ignorant reformatages et déplacements
```

Les options `-w -C -C` du blame comptent : sans elles, un reformatage massif de 2018 s'attribue tout le code et l'histoire réelle disparaît.

## Le motif « incident »

Signature à repérer :
- correction rapide, souvent hors des heures ouvrées
- message mentionnant un incident, un ticket urgent, un client nommé
- **aucun test associé**
- code jamais retouché depuis

```
9f3e2a1  vendredi 18h47  "fix(billing): skip zero-amount invoices - cf INC-4471"
                ↓
   une garde ajoutée sans test, jamais retirée, devenue règle métier de fait
```

Remonté comme :
> **Hypothèse `H` :** probablement un contournement d'incident (2019) devenu permanent par inertie, plutôt qu'une décision métier délibérée.
> **Question :** doit-elle être conservée ?

**C'est souvent la découverte la plus utile d'un run DMAD.** Une équipe qui apprend que sa « règle de gestion » est un patch jamais validé prend une décision différente.

## Le code supprimé
```bash
git log --diff-filter=D --name-only      # fichiers supprimés
git log -S "<terme>" --all               # apparition et disparition d'un concept
```
Ce qu'on a retiré dit ce qu'on a cessé de vouloir. Une fonctionnalité supprimée puis partiellement réintroduite raconte un changement de doctrine métier.

## Hypothèses concurrentes
Quand l'histoire est ambiguë, **exposer les lectures concurrentes** dans `competing_hypotheses` plutôt que choisir la plus élégante. La plus élégante est précisément celle qu'un modèle produit par défaut, et elle n'est pas plus probable pour autant.

## Interdits
- Écrire une intention sans preuve documentaire. Un silence de l'histoire reste un silence : il devient une question ouverte.
- Faire monter au-dessus de `H`. Seule une validation humaine tracée (`validated_by`) le peut — contrôlé mécaniquement par `validate.py`.
- Traiter une absence de preuve comme une preuve d'absence. Utiliser `evidence.kind: absence` pour enregistrer ce qui a été cherché sans être trouvé.
