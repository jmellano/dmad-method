# Task 13 — Résoudre les contrats des appels sortants

**Agent :** `contract-resolver` · **Cycle :** 1 · **Sortie :** `preuves/contrats/`

## Principe

Un appel sortant sans son code de contrat est une frontière anonyme. Avec son code, c'est une frontière **exploitable** : on retrouve le propriétaire, la supervision et le contrat. C'est la moitié de la valeur de la section 9 de la STD.

## L'échelle à quatre barreaux

**Chercher jusqu'au barreau le plus haut atteignable, et écrire lequel a servi.**

| Barreau | Source | Confiance |
|---|---|---|
| 1 | l'annotation de contrat, dans l'artefact de la dépendance | `V` |
| 2 | la Javadoc de l'interface de dépendance | `C` |
| 3 | un commentaire dans le code appelant | `I` |
| 4 | le placeholder | — |

**Un placeholder visible vaut mieux qu'un code plausible** : le premier se corrige, le second se propage.

## Procédure par appel sortant

1. **Partir du site d'appel** posé par le Cartographer, et résoudre le type du champ injecté jusqu'à l'interface importée. C'est le point de départ, et un outil de navigation sémantique le fait bien.
2. **Remonter la chaîne générée** jusqu'à l'interface qui porte l'annotation. Le code appelant n'importe presque jamais celle-ci : il importe une interface de service applicatif, qui n'en porte aucune. Le motif de nommage de la chaîne est déclaré dans `run.yaml`.
3. **Ouvrir l'artefact de la dépendance.** Il vit hors du projet indexé : **aucun outil de navigation sémantique ne le voit**. C'est de la lecture d'archive. La recette est dans `${CLAUDE_PLUGIN_ROOT}/docs/13-profil-java.md`.
4. **Relever le bloc d'annotations complet** — il donne d'un coup le code, le verbe, la route et le nom d'opération. Quatre attributs pour une seule lecture, c'est ce qui rend le barreau 1 rentable même quand un commentaire donne déjà le code.
5. **Confirmer l'invocation depuis le chemin cible.** Une classe utilitaire peut porter un contrat annoté sans être invoquée depuis le périmètre étudié. Sans cette confirmation, on documente des appels qui n'ont pas lieu.
6. **Écrire le nœud**, avec sa version d'artefact.

## Le nœud produit

```yaml
id: CTR-<module>-<nnn>
call_site: "src/.../XxxService.java#L212"
code: "SIM_APP_ACH_022"
resolution_rung: 1
artifact: "<groupId>/<artifactId>"
artifact_version: "103.65.11"
http_verb: GET
route: "/rechercherCommandeAchatParDateLivraisonEtLieu"
operation: "rechercherCommandeAchatParDateLivraisonEtLieu"
confidence: V
```

## L'invariant

```
∀ nœud ExternalContract c : c.artifact_version ≠ ∅
```

**Refusé à l'écriture sinon.** L'artefact lu est figé à la version que le module étudié consomme, qui n'est pas celle que le module appelé publie aujourd'hui. Sans le champ, la preuve reste plausible et devient fausse au premier bump — sans que rien ne le signale.

## Deux périmètres à ne pas confondre

**Les appels sortants** ont un artefact dans le dépôt local : c'est là qu'on lit leur contrat.

**Les points d'entrée du module étudié** n'en ont pas — un module ne dépend pas de sa propre API. Pour documenter les contrats entrants, lire les sources du module lui-même. Confondre les deux fait chercher longtemps un artefact qui n'existe pas.

## Ce qui n'est pas résolu

Un placeholder, une question ouverte, et une ligne dans les points d'attention de la STD. Le rapport de couverture publie la répartition par barreau : c'est une mesure de la qualité des sources, pas seulement du nombre de contrats trouvés.
