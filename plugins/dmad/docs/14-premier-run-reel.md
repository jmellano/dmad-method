# DMAD — Premier run sur un projet réel

> **Run `lcdn-backend-2026-09-09`** · Spring Boot 3.4.1 / Java 21 · 88 174 LOC · 678 fichiers
> Plugin v0.3.0 · Mode `full-scan` · Commanditaire = auteur unique du code, joignable
>
> Ce document répond au jalon de la roadmap : *« un run complet sur un vrai legacy ».*
> Les trois chiffres demandés y sont, ainsi que six frictions rencontrées.

## Le contexte, et ce qu'il ne prouve pas

| Facteur | Valeur | Conséquence |
|---|---|---|
| Compilation | ✅ 41 s, 0 erreur | LSP nominal, **plafond `V`** — le mode dégradé n'a **pas** été testé |
| Historique git | complet, 20 mois, 889 commits | l'Archaeologist n'est pas plafonné |
| Auteur du code | **commanditaire lui-même** | gate 3 arbitré en minutes, pas en atelier |
| Documentation existante | 43 000 lignes, partiellement fausse | exclue des sources au gate 0 |

⚠️ **Ce run est un cas favorable.** Un legacy dont les auteurs sont partis et qui ne compile
pas donnerait des chiffres différents. Ce qui suit vaut pour ce contexte, pas en général.

## Les trois chiffres demandés

### 1. Coût réel

| Phase | Agents | Tokens |
|---|---|---|
| 1 — reconnaissance | 3 | ~285 k |
| 3 — découpage | 1 | ~100 k |
| 4 — élucidation | 6 | ~1 130 k |
| 5 — challenge | 2 | ~240 k |
| 6 — diagrammes | 2 | ~200 k |
| 4bis — archéologie | 1 | ~170 k |
| Refonte au format livrable | 3 | ~490 k |
| **Total** | **18** | **~2,6 M** |

Pour **13 capacités**, 361 règles, 47 diagrammes, sur 88 kLOC.
Ordre de grandeur : **~30 k tokens / kLOC** en couverture complète.

**L'hypothèse de design est vérifiée** : les phases 1 et 2 sont peu coûteuses et produisent
du `V` sans interprétation. La phase 4 concentre 43 % du coût — c'est aussi la moins fiable,
ce qui justifie le Challenger.

### 2. Taux de findings du Challenger

| Capacité | Règles | Taux |
|---|---|---|
| gestion-leads | 27 | **37 %** |
| ingestion-promoteurs | 33 | **50 %** |
| diffusion-evenements | 25 | **48 %** |

**Au-dessus du repère de 15-30 %.** Deux lectures, honnêtement :
- les Elucidators ont pu être trop affirmatifs ;
- ou le code contient réellement beaucoup de pièges.

L'indice qui tranche partiellement : **les findings se concentrent sur peu de causes racines**
(une auto-invocation à une seule ligne en explique 3 à elle seule ; un consumer non migré en
explique 2). Un taux brut de 50 % réparti sur 4 causes n'a pas le même sens que 50 % sur
25 causes indépendantes.

→ **Proposition de métrique complémentaire : `findings / causes racines distinctes`.**
Le taux brut seul ne permet pas de distinguer « Elucidator bavard » de « code piégeux ».

### 3. Justesse par échantillonnage

Protocole : 5 règles tirées au sort (seed fixe, reproductible) sur 85, code ouvert aux lignes
citées, phrase comparée.

**Résultat : 5/5 exactes, 0 erreur.** Seuil d'échec (>1/5) non atteint.

Réserve : 5 tirages, pas 20 comme le suggère la roadmap. Le tirage a de plus sur-représenté
une capacité (3/5). À refaire à plus grande échelle.

### Critère de succès : « est-ce que ça vous débloque ? »

**Oui.** Le run a produit 6 bugs réels vérifiés qu'une relecture complète de la documentation
existante, faite le matin même, n'avait pas produits :
1. un consumer d'événements qui **écrase son propre marquage d'erreur** (event `CONSOMME` au
   lieu de `EN_ERREUR`, sans retry ni trace) ;
2. un `@Transactional(timeout=600)` **inopérant** sur le chemin planifié (auto-invocation) ;
3. un endpoint exposant **email/nom/téléphone** de tous les contacts à tout compte authentifié ;
4. un garde-fou de sécurité en **code mort** (teste `"REAL"`, la valeur réelle est `"HTTP"`) ;
5. un baromètre publiant des **pourcentages sur un dénominateur plus large que son stock** ;
6. une exception dont le constructeur **jette son message** (`"Erreur technique: null"`).

## Le résultat le plus inattendu

**Trois affirmations de la mémoire de l'agent — toutes héritées de la documentation
existante — se sont révélées fausses.**

| Ce qui était cru | La réalité vérifiée |
|---|---|
| events bloqués en `A_CONSOMMER` si un consumer est absent | `IllegalStateException` ⇒ `EN_ERREUR` ⇒ 3 retries ⇒ `ABANDONNE` |
| masquage couvrant nom, adresse, code postal | **email et téléphone uniquement** |
| un validateur bloquant l'envoi réel en non-prod | **code mort**, jamais déclenché |

C'est la thèse centrale de DMAD vérifiée **contre l'agent lui-même** : une documentation
fausse est plus nuisible qu'une absence de documentation, parce qu'un agent la propage
ensuite avec assurance. L'anti-pattern A1 ne concerne pas que les LLM qui rédigent — il
concerne aussi les LLM qui *lisent*.

## Six frictions rencontrées

### F1 — La phase 1 se croit fiable et ne l'est pas toujours ⚠️ le plus transférable
Un hook d'optimisation de tokens (`rtk`) tronquait `git log` à **50 lignes, sans marqueur**.
Conclusion produite : « historique tronqué à 7 semaines ». Réalité : 20 mois, 889 commits.
Le faux diagnostic a été annoncé au commanditaire, qui a demandé à « débloquer » un problème
inexistant.

**Une sortie tronquée est indiscernable d'une sortie complète.** Un fait dit « mécanique »
n'est fiable que si l'outil qui le produit l'est.

→ **Proposition** : le gate 0 devrait exiger une **contre-vérification croisée** de tout fait
structurant, par deux commandes indépendantes. Exemple : l'étendue d'un historique se vérifie
par `git rev-list --max-parents=0 HEAD` **et** par `git rev-list --count HEAD`, jamais par un
`git log | tail`.

### F2 — Les diagrammes cassés ne rendent rien, et ça ne se voit pas
Sur 47 diagrammes Mermaid produits, **4 ne compilaient pas** — invisibles à la relecture,
rendus vides sur GitLab/GitHub. Causes trouvées : parenthèses dans un libellé de `flowchart`,
parenthèses et deux-points dans un `gantt`, `linkStyle` hors borne, et un **point-virgule dans
un message de `sequenceDiagram`** (trois itérations pour l'identifier).

→ **Proposition** : la checklist `diagram-quality.md` devrait porter une case
**« compile réellement »**, et le `diagram-engine` à construire devrait valider au rendu.
Un diagramme non compilé est une non-livraison, exactement comme un diagramme illisible.

### F3 — `validate.py` attend une arborescence non documentée
Le validateur route par nom de dossier **à la racine du run** (`claims/`, `open-questions/`),
alors que `07-livrables.md` les place sous `preuves/`. Les artefacts ont été silencieusement
ignorés (« 1 artefact validé » au lieu de 10) jusqu'à inspection du code.

→ **Correctif proposé** : accepter les deux emplacements, ou aligner la documentation.

### F4 — La contrainte `V` fonctionne, et c'est inconfortable (dans le bon sens)
`validate.py` a **refusé les 3 premières claims**, écrites en `V` sur la foi d'une lecture de
code. Il a fallu les dégrader en `C` et écrire, dans `confidence_reason`, ce qui manquerait
pour monter.

**C'est le mécanisme le plus précieux de la méthode.** Il transforme une intention en
contrainte. À conserver tel quel — et à mettre en avant dans le README, car c'est ce qui
distingue DMAD d'un prompt de documentation.

### F5 — Le format de sortie n'est pas spécifié, et ça se voit
`07-livrables.md` donne une arborescence mais aucun **gabarit de document**. Résultat : des
fiches de 30-150 lignes, navigables mais insuffisantes comme spécification. Le commanditaire
a fourni sa propre référence (SFD/STD de ~2 000 lignes) et il a fallu tout refondre.

Ce qui manquait et qui a fait la différence une fois ajouté :
- un **front-matter YAML** avec `last_code_sync` (SHA), `confidence`, `validated_by` ;
- un **bandeau d'audience** disant ce que le document **ne** couvre **pas** ;
- une section **« Points d'attention pour le développeur »**, qualifiée (dette / bug latent /
  code mort / nommage trompeur) — le meilleur rapport valeur/effort du modèle ;
- une section **« sorties dégradées silencieuses »** : ce que le système *tait* ;
- une section **« chemins non atteignables et pièges d'attribution »** : anticiper les faux
  diagnostics.

→ **Proposition** : ajouter un `templates/document-sfd.md` et `templates/document-std.md`.

### F6 — Deux phases sont faciles à sauter sans s'en apercevoir
Le Diagram Planner (phase 6) et l'Archaeologist (phase 4) ont été **omis** dans un premier
temps. Le résultat était cohérent, bien sourcé… et sans aucun schéma ni aucun « pourquoi ».
Il a fallu que le commanditaire le signale — deux fois.

Mesure de l'écart : le mot « pourquoi » apparaissait dans **18 fichiers** de la documentation
archivée contre **3** dans la production initiale ; REX et leçons à **zéro**.

→ **Proposition** : ajouter à `release-readiness.md` deux cases bloquantes —
**« au moins un diagramme par capacité »** et **« le registre d'intention est non vide »**.
Un workflow qui n'a pas produit de REX sur un projet de 20 mois n'a pas terminé.

## Ce que ce run ne prouve pas

- Le **mode dégradé** (projet qui ne compile pas) n'a pas été exercé.
- La **phase 7** a été implémentée pendant le run, pas éprouvée dans la durée.
- **276 des 361 règles (76 %) n'ont pas été challengées** faute de budget. Sur les 85 qui
  l'ont été, le taux était de 37-50 %. Il reste donc statistiquement des erreurs.
- L'auteur du code était joignable. Sur un legacy orphelin, les `H` restent des `H`.
