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

**Pourquoi.** Faire d'un serveur de langage un prérequis dur exclurait COBOL, PL/SQL, VB6, 4GL propriétaires — c'est-à-dire exactement les projets qui ont le plus besoin de DMAD. Le compromis rend la dégradation **visible dans la doc produite** au lieu d'être silencieuse : un projet analysé au grep produit une doc plafonnée à `I`, et le lecteur le sait.

> **Révisée par D23 en v0.4.** Le principe tient — le contrat est obligatoire, l'implémentation libre, la dégradation visible — mais le plafond ne s'attache plus à l'implémentation : il s'attache à **la question posée**. Et le serveur de langage a été abandonné au profit d'un analyseur tree-sitter.

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

---

# v0.4 — Le corpus à trois documents

Les décisions D15 à D22 introduisent la cascade STD → SFD → SFG. Elles ne
remplacent aucune décision antérieure : elles en resserrent plusieurs, D3 en
particulier, qui passe d'une contrainte sur deux rédacteurs à une échelle de
lecture sur trois.

---

## D15 — Les seuils de lisibilité sont paramétrables
**Décision.** Les seuils qui déclenchent le découpage d'un diagramme sont déclarés dans `scope.yaml`. Valeurs par défaut : **N ≤ 12 nœuds, E ≤ 15 arêtes, McCabe ≤ 10**, et ~12 participants pour une séquence.

**Pourquoi.** La v0.3 posait ~20 nœuds, le corpus `skills-doc` pose 10-12 avec deux indicateurs supplémentaires. Aucun des deux chiffres n'est mesuré : ce sont des conventions de lisibilité, et une convention se paramètre. Les valeurs `skills-doc` deviennent le défaut parce qu'elles sont les seules à avoir été éprouvées sur des livrables réels, et parce qu'un seuil trop bas coûte un titre de section tandis qu'un seuil trop haut coûte un diagramme que personne ne rouvre.

**Ce qui ne change pas.** La règle R2 : au-delà du seuil **on découpe, on ne simplifie pas**. Un diagramme illisible reste une non-livraison.

---

## D16 — Aucun bloc de code ni de SQL dans le corpus
**Décision.** Les trois documents portent des **références** — `fichier:lignes`, signatures de méthodes, noms de tables et de colonnes — jamais un bloc de code source, de requête SQL ou de configuration XML. La SFD et la SFG sont en outre agnostiques de l'existence même du code.

**Pourquoi.** Deux raisons qui convergent. La première est la conformité ISO 25010 déjà posée par le corpus `skills-doc` pour la SFD : le code est dans le dépôt, pas dans la spécification. La seconde est structurelle : tant qu'un document peut contenir un extrait, un rédacteur a une raison légitime d'aller lire le code, et **D3 devient poreuse**. En supprimant l'extrait, on supprime le motif — la chaîne de preuve n'a plus de canal détourné.

**Coût assumé.** Un lecteur de STD qui veut voir la requête doit ouvrir le dépôt. C'est le prix d'une documentation dont chaque phrase a franchi la chaîne de preuve, et c'est aussi ce qui empêche la STD de vieillir à la première reformulation de la requête.

**Surcharge assumée du corpus `skills-doc`**, dont le skill STD demande aujourd'hui « extraits de code réels » (§ 4 section 4) et « blocs SQL exacts » (§ 3.5). Les sections concernées deviennent des sections de références. À reporter dans le skill plutôt qu'à laisser les deux versions coexister.

---

## D17 — Échelle de lecture en cascade
**Décision.** La STD lit le graphe et les claims. La SFD lit la STD et les claims. La SFG lit la SFD. **Chaque étage est aveugle à l'étage n−2.**

**Pourquoi.** C'est D3 généralisée. La contrainte « les rédacteurs ne lisent pas le code » garantissait que toute phrase publiée avait franchi la chaîne de preuve ; l'échelle garantit en plus que **chaque niveau d'abstraction est réellement une abstraction du précédent**, et non une seconde lecture indépendante du même matériau. Deux lectures indépendantes divergent ; une abstraction, non.

**Effet secondaire recherché.** Une information absente de la STD ne peut pas apparaître dans la SFD. Le trou se propage visiblement au lieu d'être comblé silencieusement à l'étage supérieur — où il serait précisément le plus difficile à détecter, puisque le lecteur métier n'a aucun moyen de vérifier.

**Ce qui rend la contrainte tenable.** La boucle de retour de D13, étendue : une `gap_request` d'un rédacteur remonte au cycle précédent, pas au code.

---

## D18 — Un contrat sortant est une feuille du graphe, et il est versionné
**Décision.** Un appel sortant vers un service tiers identifié par un contrat — annotation `@Cusi` et assimilés — est un nœud `ExternalContract`, feuille de l'arbre d'appels au même titre qu'un accès base de données ou un événement. Il porte obligatoirement l'**artefact et la version** où le contrat a été lu, et le **barreau de résolution** utilisé.

**Pourquoi la feuille.** Un contrat sortant est une frontière du système : ce qui se passe derrière n'est pas documenté par ce run. Le traiter comme une feuille typée le fait apparaître dans les mêmes tables de synthèse que les autres entrées-sorties, ce qui est exactement ce qu'un lecteur cherche.

**Pourquoi la version, impérativement.** Le contrat est lu dans un artefact Maven figé à la version que le module étudié consomme, qui n'est pas celle que le module appelé publie aujourd'hui. Sans le champ, la preuve reste plausible et devient fausse au premier bump de version, **sans que rien ne le signale**. Un `ExternalContract` sans `artifact_version` est refusé à l'écriture.

**Pourquoi le barreau.** Les quatre sources d'un code de contrat n'ont pas la même valeur : l'annotation générée fait foi, la Javadoc est fiable en pratique, le commentaire manuscrit survit aux refactorings et ment alors sans le dire, le placeholder n'affirme rien. Écrire le barreau, c'est écrire la confiance — elle en est dérivée mécaniquement.

---

## D19 — Trois cycles emboîtés, trois revues humaines
**Décision.** Chaque document est un cycle complet — enquête, challenge, rédaction — scellé par une **revue humaine** qui peut demander corrections et compléments avant de figer le document. Le cycle suivant ne démarre pas sur un document non figé.

**Pourquoi.** Trois raisons. D'abord, chaque niveau d'abstraction appelle des angles de réfutation différents : on n'attaque pas une affirmation mécanique comme on attaque une promesse faite à un utilisateur. Ensuite, l'échelle de lecture (D17) n'a de valeur que si l'étage inférieur est stable — bâtir une SFD sur une STD encore mouvante propage les corrections deux fois. Enfin, chaque étage devient **livrable seul**, ce qui donne un critère d'arrêt défendable devant un commanditaire.

**Écarté.** Une cascade cantonnée à la restitution, avec une enquête et un challenge uniques. Moins de machinerie, mais la SFD et la SFG n'auraient eu aucune passe de réfutation propre, et on n'aurait pas pu s'arrêter après la STD.

---

## D20 — Trois unités documentaires distinctes
**Décision.** Une STD documente **un point d'entrée**. Une SFD documente **un arbre de business objects**. Une SFG se découpe **par cas d'usage**.

**Pourquoi.** Ce sont les unités que chaque lecteur cherche. Le développeur ouvre la STD parce qu'il doit modifier un batch ou une route ; l'analyste ouvre la SFD pour comprendre un processus ; l'utilisateur ouvre la SFG au cas d'usage qui le concerne. Forcer les trois dans un découpage unique — par capacité, par exemple — plierait deux documents sur trois à un axe qui ne leur appartient pas, et ajouterait un niveau de titre sans rien clarifier.

**Conséquence.** Les tables de correspondance croisées ne sont pas un ornement : ce sont elles qui permettent de passer d'une unité à l'autre. Chaque document en porte une en tête.

---

## D21 — Le gate 3 migre en tête du cycle 2
**Décision.** Le gate de découpage en capacités, le plus important de la méthode, devient la porte d'entrée du cycle 2 au lieu de suivre la cartographie.

**Pourquoi.** Une STD par point d'entrée se produit sans savoir quelles capacités métier existent : la cartographie et la résolution des contrats suffisent. Le découpage en capacités est une question métier dont dépend l'organisation de la SFD et de la SFG, pas celle de la STD. Le placer au début du cycle 2, c'est le placer là où sa réponse est effectivement consommée — et c'est aussi le poser après une revue humaine de la STD, donc devant un expert qui vient de lire la carte technique.

---

## D22 — Le modèle est spécifié, sa sérialisation ne l'est pas encore
**Décision.** La v0.4 nomme les types de nœuds, leurs champs et leurs invariants. Le **format de stockage** relève du chantier suivant, qui portera le corpus sur un bundle Open Knowledge Format.

**Pourquoi.** Les deux sont séparables et leur couplage coûterait cher : écrire aujourd'hui du YAML DMAD pour le convertir demain en concepts OKF serait une réécriture, alors que définir le modèle sans son format en fait une sérialisation. Le recouvrement entre les deux vocabulaires est d'ailleurs presque champ pour champ — `evidence` et `sources`, `confidence` et les niveaux de confiance dérivés, `freshness` et `status`/`stale_after` — ce qui rend la conversion mécanique dès lors que le modèle est propre.

---

## D23 — Le plafond de confiance se dérive de la question, pas de l'implémentation
**Décision.** La capability `code-intelligence` est servie par **un analyseur tree-sitter** (`jcallgraph`), et le plafond de confiance n'est plus attaché à l'implémentation : il est attaché à **ce qui est demandé**. Une hiérarchie de types est `V` ; un appel virtuel rend des candidats en `C` ; une réflexion est `I` et ouvre une question.

**Pourquoi abandonner le serveur de langage.** Il promettait `V` sur tout, et il coûtait quatre modes de panne cumulés, dont trois n'apparaissaient qu'après avoir résolu le précédent : un magasin de certificats propre à son environnement d'exécution embarqué, des marqueurs d'échec de résolution qui bloquent les tentatives suivantes, un cache de symboles qui persiste des résultats vides comme s'ils étaient valides, et des processus orphelins qui épuisent la mémoire. À quoi s'ajoutait un démarrage paresseux qui faisait conclure à la panne au premier appel. Un outil dont le mode nominal demande un protocole de diagnostic à quatre étages n'est pas un prérequis raisonnable pour une méthode qui vise les legacy les plus abandonnés.

**Pourquoi le plafond par question est plus juste que le plafond par outil.** Parce que c'est le principe P3 appliqué jusqu'au bout : la confiance se dérive de **la nature de la preuve**. Un plafond unique par implémentation traitait « je sais lire la hiérarchie de types de ce fichier » et « je ne sais pas quelle implémentation est injectée ici » comme la même chose. Elles ne le sont pas, et les confondre pénalisait tout un run pour un dispatch non résolu — ou, pire dans l'autre sens, laissait passer en `V` une exhaustivité que rien ne fondait.

**Ce que ça change concrètement.** Le plafond s'applique **par arête du graphe** et non plus globalement au run. `scope.yaml` déclare donc un plafond maximal *et* le détail par type de question.

**Ce que ça ne change pas.** La règle qui fait tenir l'édifice : une réponse dégradée plafonne les affirmations qui en dépendent, et la dégradation reste **visible dans le document produit**.

---

## D24 — Aucune dépendance à un serveur MCP
**Décision.** Le plugin n'embarque aucun serveur MCP. Les huit capabilities sont servies par des outils déjà présents chez l'hôte, un exécutable local, ou le modèle lui-même.

**Pourquoi.** Un serveur est une dépendance à installer, à lancer, à diagnostiquer quand il ne répond pas, et qui consomme du contexte à chaque appel. Sur les projets que DMAD vise — des legacy dont personne ne maîtrise plus l'environnement — chaque prérequis d'installation est une raison de ne pas commencer. La v0.3 en demandait trois ; la v0.4 n'en demande aucun.

**Ce que ça coûte, et qui doit être dit.** `doc-retrieval` devient **optionnelle**. Comprendre du Struts 1.2 ou du Spring 2.5 sans sa doc d'époque produit des contresens, et la version compte autant que le nom. Quand la capability est absente, ce n'est pas un run dégradé : c'est un risque nommé — toute affirmation qui repose sur le comportement supposé d'un framework ancien, plutôt que sur le code effectivement lu, est plafonnée à `I` et porte sa question ouverte.

**Ce que ça ne coûte pas.** `reasoning` était déjà servi par le modèle ; le serveur n'ajoutait qu'une trace. Et `code-intelligence` a changé d'implémentation pour une autre raison, indépendante (D23).

---

## D25 — L'unité de la STD et de la SFD est le processus, pas le point d'entrée
**Décision.** Une STD et une SFD documentent **un processus**, et cataloguent ses points d'entrée dans leur premier chapitre. La SFG documente un domaine, découpée par cas d'usage. D20 est révisée sur ses deux premières lignes.

**Pourquoi.** **Un processus a rarement un seul point d'entrée.** Le corpus de référence FEF l'a établi par l'échec : sur son document témoin, `entry_point_type: BATCH` était faux alors qu'une section décrivait déjà un sous-processus événementiel. Le périmètre déclaré dans le frontmatter doit se vérifier contre le sommaire du document lui-même, et c'est ce que le chapitre 1 permet.

**Ce que ça simplifie.** STD et SFD partagent désormais l'unité et le périmètre, et ne diffèrent que par l'audience et le registre. La cascade s'en trouve plus nette : une STD, une SFD, même processus, deux lectures.

**Ce que ça coûte.** Rien de ce que D20 protégeait : l'unité reste déclarée, vérifiée mécaniquement, et un document plié dans le découpage d'un autre reste refusé.

---

## D26 — Le bundle est la sortie primaire, le document en est dérivé
**Décision.** Les rédacteurs écrivent des **concepts** dans le bundle OKF. Un **plan** — donnée du run, pas code — dit quel concept occupe quel numéro de section. `tools/okf-compose.py` assemble. **Une correction se fait dans le concept, jamais dans le fichier composé** : une édition faite là est perdue à la régénération.

**Pourquoi cet ordre-là.** Un concept est réutilisable entre documents et entre audiences ; une section de document ne l'est pas. Écrire le document d'abord oblige à le redécouper ensuite — et un concept partagé finit par exister en deux versions, une par document, qui divergent. C'est le test de duplication : *si deux documents décrivent le même concept avec deux définitions, ce n'est pas une divergence à arbitrer plus tard, c'est un concept qui aurait dû être partagé.*

**Ce que le plan porte, et pourquoi il est une donnée.** Le plan de niveau 1 est **imposé par le gabarit** — onze chapitres en STD, dix en SFD, six en SFG. Les sous-sections sont un **résultat de l'analyse**, pas une décision de mise en page : le nombre de niveaux d'une vue récursive, le nombre de cas d'usage d'une SFG. Coder le plan dans le générateur, comme le fait le corpus dont celui-ci s'inspire, oblige à éditer l'outil pour chaque nouveau processus — inacceptable pour une méthode qui doit tourner sur n'importe quel legacy.

**Le composeur refuse plutôt que d'approximer** : un concept du plan introuvable, un concept du bundle absent du plan — du contenu écrit que personne ne lira —, une section imposée sans concept ni sous-section, un saut de niveau de titre, un lien ou une ancre morts.

**Le niveau de titre se déduit du numéro** — profondeur + 1. Le § 3.2.1 est un `h4` des deux côtés, et l'export a le même sommaire que son plan sans avoir à le retranscrire.

---

## Questions encore ouvertes

1. **Calibration.** L'échelle `V/C/I/H` et le mapping en pourcentage doivent être éprouvés sur un vrai legacy. Tant que ce n'est pas fait, ce sont des conventions, pas des mesures.
2. **Coût réel d'un run.** Inconnu. À mesurer sur un cas de référence, en tokens et en temps, par phase — c'est ce chiffre qui décidera si la méthode est vendable.
3. **Validation humaine des `H`.** Le mécanisme de signature (qui valide, comment c'est tracé, que se passe-t-il quand le code change ensuite) reste à spécifier.
4. **Multi-dépôts.** Un legacy est rarement un seul repo. Le graphe doit-il être unique ou fédéré ?
5. **Confidentialité.** Analyser du code client avec des agents implique des règles explicites (ce qui sort, ce qui reste local). À trancher avant tout usage réel.
6. **Nom.** « DMAD » se lit *mad* en anglais et évoque une parodie de BMAD. Assumé comme clin d'œil, ou à retravailler si la méthode est publiée ?
