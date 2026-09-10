# Revue de cycle 1 — la STD

**Qui valide :** un développeur qui connaît le point d'entrée, ou à défaut celui qui devra le modifier.
**Durée cible :** 30 à 45 minutes par document.
**Ce qui se passe si on saute cette revue :** la SFD est construite sur une carte technique non vérifiée, et la SFG sur cette SFD. Une erreur qui survit ici traverse tout le corpus, en gagnant en abstraction — donc en devenant plus difficile à réfuter à chaque étage.

Une revue n'est pas un feu vert. Elle peut demander **corrections et compléments**, et le cycle 2 ne démarre pas avant que la STD ne soit figée.

## Le contrôle qui compte le plus

**Tirer cinq affirmations au hasard, ouvrir le code aux lignes citées, vérifier que la phrase correspond.**

Dix minutes, et c'est le seul contrôle qui détecte l'erreur dominante des modèles de langage : **citer du vrai code en lui faisant dire autre chose**. La citation exacte donne une impression de rigueur qui désarme la vérification — c'est précisément pour ça qu'il faut la faire.

## Vérifications mécaniques

**Elles se lancent avant la séance, pas pendant.**

```bash
python3 <plugin>/tools/validate.py     dmad-output/ --code .
python3 <plugin>/tools/okf-index.py    dmad-output/ --check
python3 <plugin>/tools/check-corpus.py dmad-output/
```

**C'est le relecteur ou l'orchestrateur qui les lance, jamais l'agent producteur.** Un agent qui atteste son propre travail rend une affirmation d'état vérifié, pas un état vérifié.

Une revue humaine ne doit pas servir à trouver ce qu'une machine trouve. Ce qui suit est ce que les outils vérifient — la liste est là pour dire au relecteur ce qu'il n'a **pas** à faire, et donc où porter son attention.

- [ ] **Aucun bloc de code, de requête ou de configuration** dans le document (D16). Contrôlable par recherche des clôtures de bloc de langage.
- [ ] Les **dix-sept sections sont présentes**, y compris celles sans objet, qui portent leur constat d'absence **et son périmètre**.
- [ ] Chaque **référence `fichier:lignes` résout** sur le commit de référence.
- [ ] Chaque **contrat sortant porte son barreau et sa version d'artefact**. Aucun `ExternalContract` sans `artifact_version`.
- [ ] Chaque **diagramme porte sa question** et respecte les seuils de `run.yaml`.
- [ ] Chaque **diagramme est nommé par ce qu'il montre**, pas par son type.
- [ ] La section « limites de cette analyse » est présente et **chiffrée**.
- [ ] Le frontmatter est **parsable** par un parseur YAML — champs en phrase libre entre guillemets doubles.

## Vérifications de fond

- [ ] La **section 1.5** qualifie les composants réels, et chaque ligne cite un fait documenté ailleurs dans le document. Une ligne dont le fait est introuvable signale un manque ou une qualification faible.
- [ ] Les **pièges d'attribution** sont signalés : les artefacts voisins qui ressemblent à ce que le lecteur cherche mais n'appartiennent pas au périmètre.
- [ ] La section 12 sépare le **site de levée** et l'**effet observable**. Les confondre crée des contradictions qui deviendront des promesses fausses au cycle 3.
- [ ] Les **dispatchs non résolus** sont posés comme tels, avec leurs candidats et leur question ouverte. Aucun candidat n'a été choisi silencieusement.

## Questions à poser au développeur

1. « Cette section 9, elle liste bien tous les appels sortants de ce chemin ? » — *un appel manquant est la lacune la plus coûteuse en aval*
2. « Ce contrat au barreau 3, vous savez s'il est encore juste ? » — *le commentaire manuscrit est celui qui ment sans le dire*
3. « Qu'est-ce que vous auriez cherché dans ce document et que vous n'y trouvez pas ? »
4. « Est-ce qu'il y a un aspect, un intercepteur ou un proxy qui modifie ce comportement ? » — *aucune traversée d'appels ne le trouve*

## Enregistrement

Les corrections sont enregistrées **avec leur raison**. Une correction dont on ne sait plus pourquoi elle a été faite se refera à l'envers au prochain run.
