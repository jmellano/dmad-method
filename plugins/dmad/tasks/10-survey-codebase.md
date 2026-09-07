# Task 10 — Recenser la codebase

**Agent :** `surveyor` · **Phase :** 1 · **Sortie :** `facts/*.json` · **Modèle :** haiku

## Objectif
Établir mécaniquement tout ce qui peut l'être. **Chaque fait établi ici est un fait qu'aucun modèle en aval n'aura l'occasion d'halluciner.**

## Procédure

### Stack et versions
Fichiers de build (`pom.xml`, `package.json`, `composer.json`, `*.csproj`, `Gemfile`…), lockfiles, images Docker, runtime cible.
**Les versions sont obligatoires** : un Spring 2.5 ne se lit pas comme un Spring 6, et le `doc-retrieval` en aval en dépend.

### Modules et dépendances internes
Arborescence, découpage par langage, graphe de dépendances entre modules, **cycles détectés**.

### Données
```
db/migrations/*, schema.sql, modèles ORM
→ tables, colonnes, types, NOT NULL, CHECK, UNIQUE, FK, index
```
Les contraintes déclaratives sont des **règles de gestion de niveau `V`** obtenues gratuitement : non contournables, non ambiguës. C'est le meilleur rendement de toute la méthode.

### Intégrations sortantes
Clients HTTP, SDK, URL en configuration, files, FTP, batchs d'échange, envois de mail.

### Tests
Fichiers, framework, nommage, couverture si un rapport existe. Extraire **la liste des noms de tests** : souvent la dernière documentation métier vivante du projet.

### Hotspots
```
git log --format=%H --name-only --since=2.years  → churn par fichier
+ complexité (cyclomatique, ou LOC en repli)
+ git shortlog -sne -- <file>                     → bus factor
→ hotspots = churn x complexité, top 20
```

## Sortie
```json
{
  "generated_at": "2026-09-07T10:12:00Z",
  "commit": "a1b2c3d",
  "stack": { "language": "java", "version": "8", "framework": "spring", "framework_version": "4.3.12" },
  "counts": { "files": 1847, "loc": 214000, "tables": 88, "entrypoints": 51 },
  "degraded_capabilities": [
    { "capability": "runtime-evidence", "status": "degraded",
      "reason": "couverture seule, aucune trace", "confidence_ceiling_applied": "C" }
  ]
}
```

## Interdits
- Aucune prose. Aucun verbe d'opinion (*semble*, *paraît*, *gère probablement*) — rejeté par `claim-quality`.
- Aucune priorisation métier : c'est le travail du Carver, avec un modèle qui en a les moyens et un gate derrière.
- **Aucun comblement** : un outil qui échoue produit une entrée `unavailable` avec sa raison et son impact, jamais une déduction.
