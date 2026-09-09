# DMAD — Anti-patterns de la rétro-documentation

Chaque garde-fou de DMAD existe contre une défaillance précise et observable. Ce document les nomme. Il se lit comme le *pourquoi* de la méthode — et il est aussi le meilleur argumentaire pour défendre les contraintes qui, prises isolément, paraissent excessives.

---

## A1 — La documentation plausible et fausse

**Le symptôme.** On demande à un LLM de documenter un legacy. En quelques minutes on obtient un document fluide, structuré, avec des diagrammes cohérents et un vocabulaire crédible. Quelques affirmations sont fausses. **On ne sait pas lesquelles.**

**Pourquoi c'est le pire des cas.** Une absence de documentation est un problème connu : chacun sait qu'il doit vérifier. Une documentation fausse est un problème invisible : l'équipe suivante la croit, décide sur cette base, et découvre l'erreur en production. La documentation legacy fausse est **plus nuisible que l'absence de documentation**.

**La parade DMAD.** Chaîne de preuve obligatoire (`evidence` minItems 1), agent adversarial dédié, rédacteurs sans accès au code, contrôle par échantillonnage.

---

## A2 — La preuve trahie

**Le symptôme.** La claim cite `InvoiceService.java:212-228`. Les lignes existent. Le code est réel. **Mais il ne dit pas ce que la claim lui fait dire.**

**Pourquoi c'est le mode d'erreur dominant.** L'intuition commune veut qu'un LLM « invente du code ». En pratique, c'est rare et facilement détecté. Ce qui se produit vraiment, c'est un **glissement d'interprétation** : le modèle lit un vrai fragment et en tire une généralisation légèrement fausse. Et la citation exacte, avec ses numéros de ligne, **produit une impression de rigueur qui désarme la vérification**.

**La parade.** Angle 1 du Challenger, examiné en premier. Contrôle humain par échantillonnage (5 claims au hasard, ouvrir le code) — dix minutes qui valent plus qu'une relecture intégrale, laquelle ne détecte rien sur un texte crédible.

---

## A3 — La documentation vraie en recette et fausse en production

**Le symptôme.** La règle documentée est exacte… dans l'environnement observé. Un feature flag, une variable d'environnement, un profil de build ou un paramètre en base la change ailleurs.

**Pourquoi c'est difficile à détecter.** Rien ne cloche dans la phrase. Elle est bien écrite, bien sourcée, et vérifiable — dans un seul environnement. Un relecteur qui connaît la production la validera ; un développeur qui teste en local constatera l'inverse et conclura que toute la documentation est douteuse.

**La parade.** Le champ `conditional_on` (obligatoirement reflété dans l'énoncé, contrôlé par `validate.py`), et l'angle 3 du Challenger qui compare systématiquement valeur par défaut et valeur observée.

---

## A4 — L'exhaustivité non prouvée

**Le symptôme.** « Une facture annulée n'est **jamais** transmise. » Vrai sur le chemin lu. Faux sur le troisième appelant, que personne n'a ouvert.

**Pourquoi ça passe.** Les quantificateurs universels sont naturels à l'écrit et coûteux à vérifier. Ils rendent une documentation plus affirmative et plus agréable à lire — donc plus dangereuse.

**La parade.** Angle 7 du Challenger. Et surtout : le **plafond de capability** — une navigation au `grep` interdit mécaniquement toute affirmation d'exhaustivité, parce qu'elle ne peut pas être établie.

---

## A5 — L'automate imaginaire

**Le symptôme.** Un diagramme d'états élégant, cohérent, avec des transitions nommées. Le champ d'état correspondant n'existe pas dans le code : le modèle a reconstruit une machine plausible à partir de bouts de logique.

**Pourquoi c'est particulièrement pernicieux.** Un diagramme est **plus persuasif qu'un paragraphe**. Un lecteur discute une phrase ; il regarde un schéma et l'intègre. Un automate inventé devient la représentation mentale de référence d'une équipe entière.

**La parade.** Machine à états générée **uniquement** si un champ d'état réel existe et que ses transitions sont repérables. Sinon : question ouverte. Et un seuil de 12 états qui déclenche une re-vérification, parce qu'un automate à 20 états dans un legacy signale presque toujours une fusion de plusieurs automates distincts.

---

## A6 — Le hairball

**Le symptôme.** Un diagramme de classes de 400 nœuds. Techniquement exact. Ouvert une fois, jamais deux.

**Pourquoi ça se produit.** Parce que c'est facile à générer et que ça donne l'impression d'exhaustivité. C'est une capture d'écran de la complexité présentée comme sa maîtrise.

**La parade.** Un diagramme = une question affichée. Seuils de lisibilité qui déclenchent un découpage, jamais une simplification. Diagramme de classes borné à une capacité, jamais global.

---

## A7 — Le pourcentage de confiance inventé

**Le symptôme.** « Confiance : 87 %. » Le nombre vient du modèle. Il n'est calibré sur rien, il change d'un run à l'autre, et il **rassure à tort**.

**Pourquoi c'est tentant.** Afficher la fiabilité est une excellente intuition. Demander un pourcentage au modèle est la façon la plus simple de le faire — et la seule qui ne mesure rien.

**La parade.** Échelle discrète `V/C/I/H` dérivée mécaniquement de la nature de la preuve. Confiance d'un chapitre = **minimum** de ses affirmations, jamais moyenne (une moyenne dilue le mensonge). Seul un test exécuté fait monter au niveau maximal.

---

## A8 — Le Challenger complaisant

**Le symptôme.** L'agent de vérification confirme 40 claims sur 40. Le run paraît excellent.

**Pourquoi c'est prévisible.** Un LLM à qui on demande « vérifie ceci » confirme : c'est la complétion la plus probable. La vérification n'est pas un comportement par défaut, c'est une contrainte à imposer.

**La parade.** Trois mesures, aucune suffisante seule :
1. **Consigne inversée** — pas « vérifie » mais « trouve le chemin de code qui rend ceci faux »
2. **Contexte séparé** — le Challenger ne voit pas le raisonnement de l'Elucidator, donc n'hérite pas de ses angles morts
3. **Quota de doute** — aucun finding sur une capacité ⇒ produire les 3 claims les plus fragiles

Repère : **15 à 30 % de claims dégradées** est le taux attendu sur un legacy réel.

---

## A9 — Le rédacteur qui comble

**Le symptôme.** Le graphe a un trou. Le rédacteur a le code sous les yeux. Il lit, comprend, et écrit un paragraphe fluide — **qui n'a traversé ni le Challenger ni les tests**.

**Pourquoi c'est invisible.** Le paragraphe est bon. Il est peut-être même juste. Mais il est indiscernable, dans le document final, des paragraphes qui ont franchi la chaîne de preuve. Un trou comblé silencieusement est pire qu'un trou : il supprime le signal.

**La parade.** Les rédacteurs **n'ont pas accès au code**. C'est la contrainte la plus contre-intuitive de DMAD, et probablement la plus importante. Elle coûte en fluidité ; elle garantit que toute phrase publiée est prouvée.

---

## A10 — La documentation parfaite du mauvais périmètre

**Le symptôme.** Le run se déroule bien, produit une documentation cohérente et bien sourcée… d'un ensemble de code qui n'est pas celui que le commanditaire avait en tête.

**Pourquoi c'est le pire mode d'échec.** **Il ne se voit pas dans le résultat.** Tous les indicateurs de qualité interne sont au vert. L'erreur ne se découvre qu'à la lecture, par un humain qui connaît le domaine — parfois des semaines plus tard.

**La parade.** Le gate de localisation du `feature-scan` : cinq sondes indépendantes, candidats classés, **confirmation humaine obligatoire** avant toute traversée. Dix minutes d'un humain contre des heures de travail dans la mauvaise direction.

---

## A11 — La photo qui jaunit

**Le symptôme.** Une documentation excellente le jour de sa livraison. Six mois plus tard, le code a bougé, la documentation non. Elle est désormais **fausse avec l'autorité d'un document officiel**.

**Pourquoi c'est fatal.** C'est ce qui a produit le legacy qu'on documente. Reproduire le mécanisme en le croyant résolu par des agents serait ironique.

**La parade.** Phase 7. Chaque claim pointe des lignes et un commit ; le rejeu distingue `fresh` / `shifted` / `stale` / `broken`. Intégrable en CI avec un seuil — réglé assez haut pour ne pas produire du bruit, sans quoi il sera désactivé en trois semaines.

---

## A12 — Le run qui ne finit jamais

**Le symptôme.** Périmètre non borné, budget non suivi. Le run consomme, produit des fragments, et s'arrête faute de moyens avec six capacités à moitié documentées.

**Pourquoi ça arrive.** Parce que « documenter le projet » est un objectif sans critère d'arrêt. Il n'y a pas de moment où c'est fini.

**La parade.** Gate 0 bloquant sur un objectif formulé en capacité d'action. Priorisation par hotspots (le critère d'arrêt défendable : « on a couvert les zones à risque »). Et la règle de budget : **on s'arrête sur une capacité terminée** plutôt que d'en laisser six en chantier.

---

## A13 — La confusion analyse / prescription

**Le symptôme.** La documentation se met à recommander : « ce module devrait être refactoré », « cette architecture est inadaptée ». Le lecteur ne sait plus ce qui est constaté et ce qui est jugé.

**Pourquoi c'est un problème.** Un constat se vérifie contre le code ; une recommandation dépend d'un contexte (budget, roadmap, équipe, appétence au risque) que DMAD ne connaît pas. Les mélanger fait perdre la valeur du premier sans donner la légitimité de la seconde.

**La parade.** DMAD documente ce qui **est**, y compris ce qui est laid. Les seams sont **décrits** avec leur coût ; la décision appartient à l'équipe. Le Test Forger ne modifie jamais le code de production, même pour le rendre testable.

---

## A14 — Le contrat périmé par un bump de version

**Le symptôme.** La documentation cite le code d'un appel sortant — la clé d'entrée de son exploitation. Six mois plus tard, la dépendance a changé de version, le contrat a bougé, et le document affirme toujours l'ancien. Rien ne s'est cassé, rien n'a alerté : **le code cité reste plausible**.

**Pourquoi c'est vicieux.** L'artefact lu est figé à la version que le module **consomme**, pas à ce que le module appelé publie aujourd'hui. Un lecteur qui appelle la supervision avec un code périmé tombe sur un service qui n'existe plus, ou pire, sur un autre.

**La parade.** `artifact_version` obligatoire sur tout nœud `ExternalContract`, refusé à l'écriture sinon, et comparé à la version résolue par le build à chaque passe de fraîcheur.

---

## A15 — La cascade percée

**Le symptôme.** Un rédacteur de SFD, bloqué par un trou de la STD, va lire le code. Un rédacteur de SFG, bloqué par une SFD imprécise, va lire la STD. Le document produit est correct, personne ne remarque rien.

**Pourquoi c'est un problème.** Le document cesse d'être une **abstraction** du précédent et redevient une **lecture indépendante** du même matériau. Or deux lectures indépendantes divergent — c'est mécanique — et la divergence apparaîtra plus tard, entre deux documents qu'on croyait cohérents par construction. Pire : la lecture faite en contrebande n'a traversé ni le Challenger ni le Test Forger, alors que le document, lui, porte les badges de confiance de la chaîne.

**La parade.** Trois niveaux : `disallowedTools` sur les rédacteurs, règles `deny` sur les chemins, et surtout la `gap_request` qui **remonte d'un cycle** — un rédacteur bloqué a un recours, sinon il contourne.

---

## A16 — Le faux barreau

**Le symptôme.** Un code de contrat lu dans un commentaire manuscrit, présenté dans la documentation comme s'il venait du contrat lui-même.

**Pourquoi c'est indétectable.** **Un code faux ressemble exactement à un code vrai.** Rien dans sa forme ne trahit sa source, et le commentaire manuscrit a une propriété redoutable : il survit à un refactoring qui a changé la méthode appelée. Il ment alors sans le dire, et il ment avec l'apparence de la précision.

**La parade.** `resolution_rung` obligatoire, et la confiance **dérivée** du barreau plutôt que choisie : 1 pour l'annotation qui fait foi, 2 pour la Javadoc générée, 3 pour le commentaire, rien pour le placeholder. Un placeholder visible se corrige ; un code plausible se propage.

---

## Tableau de correspondance

| Anti-pattern | Garde-fou principal | Où |
|---|---|---|
| A1 plausible et faux | chaîne de preuve complète | tout le manifeste |
| A2 preuve trahie | angle 1 + échantillonnage | `50-challenge-claim`, `claim-quality` |
| A3 vrai en recette | `conditional_on` + angle 3 | `claim.schema.json` |
| A4 exhaustivité | angle 7 + plafond de capability | `04-capabilities` |
| A5 automate imaginaire | champ d'état réel obligatoire | `06-diagrammes` |
| A6 hairball | une question + seuils | `diagram-quality` |
| A7 pourcentage inventé | échelle V/C/I/H dérivée | `01-manifeste` §4 |
| A8 challenger complaisant | consigne inversée, contexte séparé, quota | `gate-5-challenge` |
| A9 rédacteur qui comble | pas d'accès au code | `03-agents`, D3 |
| A10 mauvais périmètre | gate de localisation | `12-locate-feature` |
| A11 photo qui jaunit | phase 7, freshness | `71-check-freshness` |
| A12 run sans fin | gate 0 + hotspots + règle de budget | `workflows/` |
| A13 analyse/prescription | documenter ce qui est | `03-agents` |
| A14 contrat périmé | `artifact_version` obligatoire + fraîcheur | `external-contract.schema.json`, D18 |
| A15 cascade percée | échelle de lecture + `gap_request` d'un cycle | `03-agents`, D17, `check-corpus.py` |
| A16 faux barreau | `resolution_rung` + confiance dérivée | `13-resolve-outbound-contracts`, D18 |
