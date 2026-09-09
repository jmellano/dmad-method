# DMAD — État et suite

## Où en est le projet

**v0.4 — le corpus à trois documents est spécifié.** Ce qui existe :

| Brique | État |
|---|---|
| Manifeste, principes, échelle de confiance | ✅ |
| Méthode : 8 phases, 3–4 gates, 2 modes | ✅ |
| 15 agents avec périmètre de lecture et plafond | ✅ |
| Corpus STD → SFD → SFG, trois cycles, trois revues | ✅ |
| Résolution des contrats sortants, échelle à quatre barreaux | ✅ |
| 8 capabilities contractualisées | ✅ |
| 16 tâches opérationnelles | ✅ |
| Schémas JSON Schema + validateur + selftest | ✅ |
| Templates de sortie | ✅ |
| Run de référence rendu de bout en bout | ✅ (fictif) |
| Catalogue d'anti-patterns | ✅ |
| **Run sur un legacy réel** | ❌ **c'est ce qui manque** |

## Le seul jalon qui compte maintenant

**Un run complet sur un vrai legacy.** Tant qu'il n'a pas eu lieu, DMAD est une spécification cohérente — ce qui ne prouve rien. Trois chiffres en sortiront, et ce sont eux qui décideront de la suite :

1. **Le coût réel d'un run**, en tokens et en heures, phase par phase. C'est ce chiffre qui rend la méthode vendable ou non. L'hypothèse implicite du design (le modèle fort n'est payé qu'en phases 3 et 5) doit être vérifiée.
2. **Le taux de findings du Challenger.** Le repère de 15–30 % est une estimation. S'il ressort à 3 %, le Challenger est complaisant et tout l'édifice de confiance s'effondre. S'il ressort à 70 %, l'Elucidator est inutilisable en l'état.
3. **La justesse mesurée par échantillonnage.** Tirer 20 claims au hasard, les vérifier à la main, compter les erreurs. C'est la seule mesure externe de la valeur de la méthode.

**Critère de succès du premier run :** le commanditaire répond « oui » à *« est-ce que ça vous débloque ? »*, et le taux d'erreur à l'échantillonnage est inférieur à 1 sur 20.

## Ce qui reste à construire

### Fait en v0.4

- **Invariants contraints** — D16, D17, D18, D19, D20 et R1/R3 sont vérifiés par `validate.py` et `check-corpus.py`, avec vingt-huit fixtures de non-régression. Chaque message nomme la décision qu'il applique.
- **Schémas des nouveaux types** — `ExternalContract`, `BusinessObject`, `Document`.
- **Corpus du run de référence** — `examples/atlas-billing` produit STD, SFD et SFG.
- **`diagram-engine`** — les diagrammes sont rendus depuis un plan, comptés, et refusés au-delà du seuil. Un diagramme retouché à la main est détecté.
- **`freshness.py`** — avec la propagation de la péremption vers le haut.
- **Calcul de la couverture** — les chiffres calculés, l'interprétation écrite.

### Prioritaire (nécessaire au premier run réel)
- **Adaptateurs `code-intelligence`** — au minimum Serena/LSP et le mode dégradé tree-sitter

### Ensuite
- **Calibration de l'échelle.** Les seuils (3 signaux sur 4, 15–30 % de findings, mapping en pourcentage) sont des conventions raisonnées, pas des mesures. À éprouver puis ajuster.
- **Mécanisme de validation humaine des `H`.** Qui signe, comment c'est tracé, et surtout : que devient une validation quand le code change ensuite ?
- **Multi-dépôts.** Un legacy est rarement un seul repo. Graphe unique ou fédéré ? La question n'est pas tranchée.
- **Distribution.** Expansion pack BMAD, pack d'agents autonome, ou les deux.

## Questions ouvertes de conception

**Le nom.** « DMAD » se lit *mad* en anglais et sonne comme une parodie de BMAD. Assumé comme clin d'œil, ou à retravailler avant publication ? À trancher avant, pas après.

**La confidentialité.** Analyser du code client avec des agents implique des règles explicites : ce qui sort de la machine, ce qui reste local, ce qui est caviardé. Le champ existe dans `scope.yaml`, mais **le mécanisme d'application n'est pas spécifié**. C'est bloquant pour tout usage en prestation.

**Les capacités sans code.** Une procédure manuelle, un Excel parallèle, un traitement chez un prestataire : invisibles pour DMAD, souvent critiques. Le gate 3 pose la question à l'expert (« il en manque une ? »), mais la méthode n'a aucun moyen de les détecter seule. C'est une limite structurelle à assumer, pas un défaut à corriger.

**Le rapport à l'humain qui n'existe plus.** DMAD est conçu pour produire les bonnes questions. Sur un legacy dont plus personne ne connaît le domaine, il n'y a personne pour y répondre. Les `H` restent des `H`. La méthode reste utile (le *quoi* est établi), mais il faut le dire au gate 0 plutôt qu'à la livraison.

## Ce que DMAD ne deviendra pas

Pour cadrer les évolutions futures :

- **Pas un outil de refactoring.** Le Test Forger ne modifie jamais le code de production. Franchir cette ligne changerait le profil de risque de tout le produit, et retirerait au commanditaire la garantie qu'un run est sans effet de bord.
- **Pas un générateur de wiki.** L'objectif n'est pas le volume de pages.
- **Pas un remplaçant du métier.** DMAD prépare les questions ; il ne décide pas ce que le métier voulait.
- **Pas un outil qui affirme sans preuve.** Si une évolution future impose de relâcher la chaîne de preuve pour gagner en fluidité ou en couverture, c'est l'évolution qu'il faut abandonner, pas la contrainte.
