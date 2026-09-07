# DMAD — Décisions & arbitrages (v0)

Journal des choix structurants, avec ce qui a été retenu, écarté, et pourquoi. Format ADR allégé.

---

## D1 — DMAD n'est pas BMAD à l'envers
**Décision.** La méthode est construite autour d'une **chaîne de preuve**, pas autour d'un pipeline d'artefacts inversé.

**Pourquoi.** BMAD est génératif : il n'existe aucune vérité qui puisse le contredire. DMAD est investigatif : la vérité existe, elle tourne en production, et elle nous contredira. Inverser le sens des flèches sans ajouter de mécanisme de preuve produit un générateur de documentation crédible et fausse — le pire livrable possible sur du legacy, parce qu'il sera cru.

**Ce qu'on garde de BMAD.** Le modèle d'orchestration : agents spécialisés, artefacts qui se contraignent l'un l'autre, gates humains, conventions de fichiers.

---

## D2 — Confiance : échelle discrète dérivée, pas pourcentage estimé
**Décision.** Échelle `V / C / I / H`, calculée à partir de la nature de la preuve. Rendu en pourcentage optionnel, mais **calculé**, jamais demandé au modèle.

**Pourquoi.** L'intuition d'afficher la fiabilité est excellente et devient un principe fondateur. Mais demander « tu es sûr à combien ? » à un LLM produit un nombre non calibré : il ne mesure rien, il varie d'un run à l'autre, et il **rassure à tort** — une doc à « 87 % » se lit comme fiable alors que rien ne l'a vérifiée. Une échelle discrète adossée au type de preuve est vérifiable, reproductible, et auditable.

**Corollaires.** La confiance d'un chapitre est le **minimum** de ses affirmations (une moyenne dilue le mensonge). Seul un test de caractérisation qui passe fait monter en `V`. Le `Challenger` peut dégrader, jamais promouvoir.

**Écarté.** Un pourcentage produit par le modèle. **Ouvert.** La convention `V=100/C=85/I=60/H=30` est arbitraire et devra être calibrée sur des cas réels.

---

## D3 — Les rédacteurs n'ont pas accès au code
**Décision.** `Writer:Functional` et `Writer:Technical` lisent uniquement les claims validées et le graphe.

**Pourquoi.** C'est la contrainte la plus contre-intuitive de la méthode et probablement la plus importante. Un rédacteur qui a le code sous les yeux comblera naturellement les trous du graphe par sa propre lecture — et cette lecture n'aura traversé ni le `Challenger` ni le `Test Forger`. En coupant l'accès, **toute phrase publiée a nécessairement franchi la chaîne de preuve**, et les trous restent visibles au lieu d'être bouchés silencieusement.

**Coût assumé.** La prose sera moins fluide qu'un agent libre. C'est le prix de la vérifiabilité.

---

## D4 — Le LSP est un contrat obligatoire, pas une dépendance dure
**Décision.** `code-intelligence` est requis ; son implémentation est libre (Serena/LSP → tree-sitter → grep) et **chaque niveau plafonne la confiance**.

**Pourquoi.** Faire de Serena un prérequis dur exclurait COBOL, PL/SQL, VB6, 4GL propriétaires — c'est-à-dire exactement les projets qui ont le plus besoin de DMAD. Le compromis rend la dégradation **visible dans la doc produite** au lieu d'être silencieuse : un projet analysé au grep produit une doc plafonnée à `I`, et le lecteur le sait.

---

## D5 — Beaucoup de diagrammes, mais chacun répond à une question
**Décision.** Catalogue large (13 types), encadré par : une question explicite affichée, un seuil de ~20 nœuds, une génération depuis le graphe. Diagramme de classes borné à une capacité, jamais global.

**Pourquoi.** L'ambition « beaucoup de diagrammes » est justifiée sur du legacy. Mais un diagramme de classes global est un hairball que personne ne rouvre, et un diagramme sans question fait douter de tout le document. Les trois règles préservent la densité en éliminant le bruit.

**Cas particulier.** Machine à états générée **uniquement** si un champ d'état réel existe et que ses transitions sont détectables. Un automate inventé est l'hallucination la plus convaincante et la plus coûteuse de la rétro-documentation.

---

## D6 — Fait et intention sont deux champs séparés
**Décision.** Une claim porte un `statement` prouvable et un bloc `intent` non prouvable, chacun avec son propre niveau de confiance.

**Pourquoi.** Le code dit *quoi*, jamais *pourquoi*. Sans cette séparation, un modèle produit « la facture nulle n'est pas transmise **pour éviter les rejets comptables** » — une phrase où la moitié est prouvée et l'autre inventée, sans que rien ne le signale. La séparation force le rendu à distinguer les deux.

---

## D7 — La couverture est publiée
**Décision.** Chaque run publie la fraction de code réellement atteinte, par fichiers, fonctions, points d'entrée, hotspots et tables.

**Pourquoi.** C'est la seule métrique honnête et calculable de la méthode (contrairement à un pourcentage de confiance inventé). Elle permet de revendiquer un bon résultat partiel — 22 % du code mais 90 % des hotspots — plutôt que de laisser croire à l'exhaustivité.

---

## D8 — Priorisation par hotspots
**Décision.** Au-delà d'une certaine taille, l'élucidation est ordonnée par `churn × complexité` (Tornhill), pas par arborescence.

**Pourquoi.** Documenter tout un legacy est économiquement absurde et jamais terminé. Le code qui bouge et qui fait mal concentre le risque. Ça donne aussi à la méthode un **critère d'arrêt défendable** devant un commanditaire, ce qui manque à la plupart des démarches de ce type.

---

## D9 — Stockage en YAML plat versionné
**Décision.** Une claim = un fichier YAML dans git, plus un index généré. Pas de base graphe.

**Pourquoi.** Diffable en revue, corrigeable à la main par un expert métier (essentiel : c'est lui qui valide les `H`), aucune infrastructure à installer chez le client, et l'historique git des corrections devient lui-même une source de connaissance. Une base graphe n'apporterait rien à cette échelle.

---

## D10 — Compatibilité BMAD dans la forme, autonomie dans l'exécution
**Décision.** Conventions de fichiers BMAD (`agents/`, `tasks/`, `templates/`, `checklists/`, `workflows/`), enrichies de deux champs propres à DMAD : `reads:` (périmètre de lecture) et `confidence_ceiling:`.

**Pourquoi.** Familiarité immédiate pour les utilisateurs de BMAD, distribution possible en *expansion pack*, tout en restant exécutable en autonome. Les deux champs ajoutés sont ce qui empêcherait un portage naïf de perdre la garantie de fiabilité.

---

---

## D11 — Deux régimes de preuve pour le niveau `V`
**Décision.** Une claim **interprétative** (règle de gestion, cas d'usage, invariant, machine à états, acteur) n'atteint `V` que par une preuve exécutée ou déclarative. Une claim **structurelle** (risque, terme) l'atteint par un outil déterministe, à condition de nommer cet outil.

**Pourquoi.** La règle initiale, uniforme, rejetait les hotspots mesurés par `git churn` — des faits mécaniques que rien n'interprète. La distinction rétablit la cohérence sans ouvrir de brèche : un constat structurel reste refusé s'il ne nomme pas l'outil qui l'a produit, ce qui empêche « le modèle a trouvé que » de se déguiser en mesure.

**Détecté en relisant la méthode contre ses propres fixtures**, pas en la concevant.

---

## D12 — Le badge d'un chapitre exclut les intentions
**Décision.** La confiance d'un chapitre est le minimum de ses **énoncés de fait**. Les blocs `intent` en sont exclus et portent leur marquage `H` individuellement, au fil du texte.

**Pourquoi.** Les intentions sont toutes en `H` par construction (P5). Sous la règle initiale — minimum de *toutes* les affirmations — **tout chapitre aurait été badgé `H`**, ce qui aurait rendu l'échelle entièrement inutile. Le badge répond à « puis-je m'appuyer sur ce que fait le système » ; le *pourquoi* est marqué séparément parce qu'on ne s'y appuie jamais de la même façon.

**Défaut réel du manifeste v0.1**, corrigé après confrontation avec le run de référence, qui appliquait déjà la bonne règle sans qu'elle soit écrite.

---

## D13 — Une boucle de retour pour les rédacteurs
**Décision.** Un rédacteur qui rencontre un manque émet une `gap_request` ciblée. Une demande `blocking` relance l'Elucidator sur ce point précis puis le Challenger ; une demande `degrades` devient une question ouverte et le document sort avec son trou visible.

**Pourquoi.** La contrainte « les rédacteurs ne lisent pas le code » (D3) était incomplète : elle ne disait pas ce que fait un rédacteur bloqué. Sans issue, il contourne — il devine, ou il produit un document criblé de trous inutilisable. La boucle rend la contrainte tenable.

---

## D14 — Les quatre signaux du Carver ne sont pas indépendants
**Constat assumé, pas décision.** Cohésion d'appels, partage de données et vocabulaire se recoupent largement. Trois signaux convergents ne valent pas trois confirmations indépendantes.

**Conséquence.** Le couplage temporel git est le signal à plus forte valeur ajoutée : c'est le seul construit sur une source entièrement différente — le comportement des développeurs plutôt que la structure du code. Une capacité soutenue par les trois autres mais **contredite par l'historique** est plus fragile que son score ne le suggère, et doit être présentée comme telle au gate 3.

Le seuil de « 3 sur 4 » reste une convention de travail utile, à condition de ne pas la présenter comme une mesure statistique.

---

## Questions encore ouvertes

1. **Calibration.** L'échelle `V/C/I/H` et le mapping en pourcentage doivent être éprouvés sur un vrai legacy. Tant que ce n'est pas fait, ce sont des conventions, pas des mesures.
2. **Coût réel d'un run.** Inconnu. À mesurer sur un cas de référence, en tokens et en temps, par phase — c'est ce chiffre qui décidera si la méthode est vendable.
3. **Validation humaine des `H`.** Le mécanisme de signature (qui valide, comment c'est tracé, que se passe-t-il quand le code change ensuite) reste à spécifier.
4. **Multi-dépôts.** Un legacy est rarement un seul repo. Le graphe doit-il être unique ou fédéré ?
5. **Confidentialité.** Analyser du code client avec des agents implique des règles explicites (ce qui sort, ce qui reste local). À trancher avant tout usage réel.
6. **Nom.** « DMAD » se lit *mad* en anglais et évoque une parodie de BMAD. Assumé comme clin d'œil, ou à retravailler si la méthode est publiée ?
