# Revue de cycle 3 — la SFG

**Qui valide :** un utilisateur métier du domaine — celui qui subit ou déclenche le traitement, pas celui qui le maintient.
**Durée cible :** 45 minutes, plus le temps d'arbitrage des intentions.
**Ce qui se passe si on saute cette revue :** le document est publié avec des intentions inventées présentées comme des règles, et les vingt-six hypothèses qu'il contient deviennent, en six mois, des faits que plus personne ne questionne.

## Prérequis bloquant

Le `Curator` a vérifié que la SFD ne se contredit pas. **Si ce contrôle n'a pas été passé, la revue ne commence pas.**

Une contradiction laissée en SFD devient ici une promesse fausse faite à l'utilisateur, et son lecteur n'a aucun moyen de la détecter. C'est asymétrique : une erreur de STD se corrige devant un développeur qui la repère ; une erreur de SFG se découvre en production, chez quelqu'un qui avait cru.

## Le contrôle qui compte le plus

**Ouvrir une section au hasard, seule, sans le reste du document. Est-elle actionnable ?**

Un renvoi vers un autre cas d'usage est un échec de ce test. Le cas d'usage est l'unité d'évolution : s'il ne se tient pas seul, il n'est l'unité de rien.

## Vérifications mécaniques

**Elles se lancent avant la séance, pas pendant.**

```bash
python3 <plugin>/tools/validate.py     dmad-output/ --code .
python3 <plugin>/tools/okf-index.py    dmad-output/ --check
python3 <plugin>/tools/check-corpus.py dmad-output/
```

**C'est le relecteur ou l'orchestrateur qui les lance, jamais l'agent producteur.** Un agent qui atteste son propre travail rend une affirmation d'état vérifié, pas un état vérifié.

Une revue humaine ne doit pas servir à trouver ce qu'une machine trouve. Ce qui suit est ce que les outils vérifient — la liste est là pour dire au relecteur ce qu'il n'a **pas** à faire, et donc où porter son attention.

- [ ] **Sept blocs par cas d'usage**, dont « Ce qui n'est pas couvert ». Aucune exception, et ce bloc-là ne peut pas être vide.
- [ ] **Aucune règle sans ligne de traçabilité.** Une règle non sourcée est une invention jusqu'à preuve du contraire.
- [ ] **Aucune intention sans marquage** tant qu'elle n'est pas validée, et le marquage est **visible sans dérouler le tableau**.
- [ ] **Index inverse régénéré, pas édité.** Compter les règles du corps et les entrées de l'index : l'écart est un défaut.
- [ ] **Grep des interdits d'audience** sur le corps hors bloc traçabilité : noms de composants, d'applications, de tables, codes techniques, vocabulaire d'exploitation.
- [ ] **Toute cadence porte son fuseau horaire**, au format `HH:MM:SS <ZoneId>`.
- [ ] Frontmatter parsable, champs en phrase libre entre guillemets doubles.

## Vérifications de fond

- [ ] **Le test de découpage est rejoué sur chaque cas d'usage et sur chaque variation candidate**, pas seulement sur les nouveaux. Trois codes de traitement ne font pas trois cas d'usage.
- [ ] **Chaque règle présente dans plus d'un cas d'usage a une décision d'arbitrage écrite** — remontée en invariant, ou contextualisée dans chacun. Pas seulement subie.
- [ ] La section « ce que le domaine résout » **ne parle pas du système**.
- [ ] Le bloc « ce que l'utilisateur voit » couvre **l'échec autant que le succès**. L'échec est le cas le plus consulté.
- [ ] Les constats **distinguent méthode et arbitrage attendu**, et chaque arbitrage énonce ses options.

## Questions à poser à l'utilisateur métier

1. « Cette intention, c'est la bonne ? » — *pour chacune. C'est la seule façon de faire monter une hypothèse, et c'est le principal intérêt de la séance*
2. « Ce cas d'usage, vous le demanderiez d'un bloc ? » — *teste l'unité d'évolution*
3. « Quand ça échoue, c'est bien ce qui se passe pour vous ? » — *le plus discriminant : c'est là que les promesses fausses se révèlent*
4. « Il manque une situation ? » — *les cas d'usage sans code, procédures manuelles ou tableurs parallèles, sont invisibles pour DMAD et souvent critiques*

## Enregistrement

Chaque intention validée est tracée avec **qui** et **quand** — c'est ce qui la fait passer d'hypothèse à corroborée, et c'est la seule promotion qu'un humain puisse prononcer.

Les corrections factuelles sont consignées dans l'historique du document **avec ce qui était écrit et pourquoi c'était faux**. C'est la seule trace qu'un relecteur aura de la fiabilité du document — et elle vaut souvent plus que la correction elle-même.
