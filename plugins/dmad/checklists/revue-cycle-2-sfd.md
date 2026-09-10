# Revue de cycle 2 — la SFD

**Qui valide :** un analyste ou un référent métier du processus, accompagné d'un développeur pour les ancrages.
**Durée cible :** 45 à 60 minutes par document.
**Ce qui se passe si on saute cette revue :** la SFG hérite des contradictions de la SFD, et les transforme en promesses faites à l'utilisateur — indétectables par son lecteur, qui n'a ni le code, ni le graphe, ni la STD.

## Le contrôle qui compte le plus

**Chercher les contradictions internes**, section contre section. Pas les imprécisions : les contradictions.

Une SFD peut se contredire sans que ce soit une faute d'analyse — deux sections peuvent être **vraies toutes les deux, à deux moments différents du traitement**. Un lot qui échoue en bloc puis se rejoue unité par unité en est le cas type : la portée est le lot au moment de la levée, l'unité au moment de l'effet observé.

**Quand une contradiction apparaît, elle se tranche dans le code, pas dans le document.** Et le plus souvent, la résolution n'est pas « l'une des deux est fausse » mais « il manquait la distinction entre les deux temps ». C'est cette distinction qui est l'information.

## Vérifications mécaniques

**Elles se lancent avant la séance, pas pendant.**

```bash
python3 <plugin>/tools/validate.py     dmad-output/ --code .
python3 <plugin>/tools/okf-index.py    dmad-output/ --check
python3 <plugin>/tools/check-corpus.py dmad-output/
```

**C'est le relecteur ou l'orchestrateur qui les lance, jamais l'agent producteur.** Un agent qui atteste son propre travail rend une affirmation d'état vérifié, pas un état vérifié.

Une revue humaine ne doit pas servir à trouver ce qu'une machine trouve. Ce qui suit est ce que les outils vérifient — la liste est là pour dire au relecteur ce qu'il n'a **pas** à faire, et donc où porter son attention.

- [ ] **Aucun bloc de code, aucun nom de classe, aucun nom de méthode, aucun nom de patron de conception** (D16).
- [ ] **Chaque section de niveau référence au moins un ancrage de la STD** (D17). Une section sans ancrage est une information apparue de nulle part.
- [ ] **Les six blocs ISO 25010 sont présents** à chaque section de niveau, un bloc vide portant son constat d'absence.
- [ ] Chaque **diagramme respecte les seuils** de `run.yaml` et **porte sa question**.
- [ ] La **table de synthèse** couvre tous les business objects du document.
- [ ] Le **glossaire** a été appliqué : aucun identifiant de framework ou de table dans le corps.

## Vérifications de fond

- [ ] Les **business objects sont nommés par leur sens fonctionnel**. Un nom qu'un analyste ne reconnaîtrait pas signale un filtre de pertinence trop laxiste.
- [ ] **Une variation n'a pas été promue en niveau.** Deux business objects qui partagent leur arbre de feuilles et ne diffèrent que par une valeur sont un seul objet et un paramètre.
- [ ] Les **données ad-hoc chargées en boucle** sont signalées explicitement, avec leur cardinalité si elle est connue.
- [ ] Le nombre de niveaux est **justifié par les seuils**, pas par le confort de rédaction. Ni empilement de niveaux triviaux, ni diagramme saturé.
- [ ] Les **affirmations d'exhaustivité** (« toujours », « jamais ») ont été vérifiées sur tous les appelants, ou reformulées en « sur le chemin X ».

## Questions à poser au métier

1. « Ce découpage en processus, c'est le vôtre ? » — *un découpage que le métier ne reconnaît pas est un découpage faux*
2. « Cette règle, elle vous surprend ? » — *la surprise est le signal le plus rentable d'une revue*
3. « Ce cas d'erreur, il vous arrive ? À quelle fréquence ? » — *distingue le chemin possible du chemin emprunté*
4. « Qu'est-ce qui devrait être là et n'y est pas ? »

## Enregistrement

Corrections avec leur raison. **Et les contradictions résolues sont consignées avec les deux versions initiales** : c'est la trace qui empêchera de refaire l'arbitrage à l'envers, et c'est souvent une information métier en soi.
