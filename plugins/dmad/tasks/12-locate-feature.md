# Task 12 — Localiser une fonctionnalité

**Agent :** `surveyor` · **Phase :** 1b (feature-scan) · **Sortie :** `feature-candidates.yaml`

## Le problème
Un legacy de 900 kLOC ne tient dans aucun contexte. Il faut trouver les points d'entrée de « la facturation » **sans lire le projet** — en partant d'un vocabulaire métier, pas d'une arborescence.

C'est le point le plus délicat de DMAD : une mauvaise localisation produit une documentation cohérente et complète… du mauvais périmètre. C'est le seul mode d'échec de la méthode qui ne se voit pas dans le résultat.

## Les cinq sondes

Chaque sonde est **indépendante** et produit des candidats avec un score. La convergence fait la force du signal.

### Sonde 1 — Vocabulaire (coût : très faible)
Rechercher chaque terme du glossaire d'amorce **et ses variantes** dans :
noms de fichiers · noms de classes et de méthodes · noms de tables et de colonnes · chemins de routes · libellés d'IHM · messages d'erreur · clés de traduction.

Les **messages d'erreur et les clés de traduction** sont sous-estimés : ils sont rédigés en langue métier par des humains, et souvent les seuls endroits du code où le vocabulaire réel apparaît intact.

### Sonde 2 — Données (coût : faible, signal souvent le plus fiable)
Quelles tables portent le vocabulaire ? Puis : qui les lit, qui les écrit ?

Dans un legacy mal nommé côté code, **le schéma reste le document métier le plus fiable du projet** : il a été modélisé, il est versionné par les migrations, et il ment moins que le code.

### Sonde 3 — Historique (coût : faible)
```
git log --grep="<terme>" --oneline
git log --grep="<clé de ticket>" --name-only
```
Les commits d'une même fonctionnalité touchent les mêmes fichiers. Un cluster de co-modification autour d'un terme métier est un signal fort — et il capte les fichiers que le nommage ne trahit pas.

### Sonde 4 — Tests (coût : très faible)
Les **noms de tests** contiennent le vocabulaire métier survivant. Un `devrait_refuser_une_facture_sans_echeance` localise mieux qu'une recherche sur `Invoice`.

### Sonde 5 — Surface externe (coût : faible)
Routes, écrans, exports, jobs, rapports mentionnant le domaine. C'est la vue qu'a le métier du système : elle recoupe rarement le découpage du code, et cet écart est lui-même informatif.

## Agrégation

```yaml
candidate:
  entrypoint: "JOB nightly-billing"
  handler: "src/billing/BillingRun.java#L44"
  signals:
    vocabulary: 0.9      # "facture", "barème" dans le nom et le corps
    data: 1.0            # écrit invoices, invoice_lines
    history: 0.8         # 34 commits mentionnant "factur*"
    tests: 0.6           # 4 tests au vocabulaire métier
    surface: 1.0         # job connu du métier
  score: 0.86
  confidence: strong
```

Classement par score, puis **⛔ confirmation humaine obligatoire**.

## Le gate de localisation

> « Voici 12 points d'entrée candidats classés. Les 6 premiers ont un signal fort.
> Les 6 suivants sont douteux — notamment `ReportingExport` qui écrit dans
> `invoices` mais n'a jamais été modifié avec le reste depuis 2020.
> **Lesquels font partie de la facturation pour vous ?** »

Dix minutes ici évitent des heures de traversée dans la mauvaise direction. **C'est le meilleur rapport coût/valeur de toute la méthode.**

## Les deux pièges

**Le faux positif transverse.** Une classe utilitaire (`DateUtils`, `AuditLogger`) touchée par tout le monde ressort sur toutes les sondes. Filtrer par **spécificité** : un fichier qui apparaît dans les candidats de trois features différentes n'appartient à aucune.

**Le faux négatif du nommage.** La fonctionnalité « facturation » implémentée dans un module `TransactionProcessor` sans aucun terme métier. Seules les sondes 2 (données) et 3 (historique) le rattrapent — d'où l'importance de ne jamais se contenter de la recherche textuelle.

## Sortie de secours
Si aucune sonde ne converge, **ne pas deviner**. Remonter au commanditaire :
> « Le vocabulaire fourni n'apparaît nulle part dans le code. Trois hypothèses :
> le domaine porte un autre nom en interne, il est implémenté dans un autre
> dépôt, ou il n'est pas informatisé. Pouvez-vous nous montrer un écran ou un
> document produit par cette fonctionnalité ? »

Un artefact concret (un écran, un export, un PDF de facture) permet de repartir de la sortie et de remonter le code à l'envers — c'est presque toujours efficace.
