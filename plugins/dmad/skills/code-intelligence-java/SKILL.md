---
name: code-intelligence-java
description: Prérequis outillage d'un run DMAD sur un projet JVM - protocole de démarrage de l'indexeur sémantique, chaîne des quatre causes d'échec cumulées, fallbacks et plafonds de confiance associés. À lire AVANT la première invocation, pas après le premier échec.
---

# Outillage sémantique sur un projet JVM

Ce skill n'explique pas comment naviguer dans du code : il explique **pourquoi la navigation échoue**, et comment distinguer une panne d'un démarrage lent. C'est un prérequis du cycle 1, à lire avant la première invocation.

La raison d'être de ce document tient en une observation : sur un projet réel, l'indexeur a échoué pour **quatre raisons cumulées, dont trois n'apparaissent qu'une fois la précédente résolue**. Chacune, prise isolément, ressemble à « l'outil ne marche pas ».

## Ce que la navigation sémantique apporte, et ce qu'elle ne peut pas

| Question | Outil | Fiabilité |
|---|---|---|
| que fait cette méthode ? | recherche de symbole avec corps | élevée |
| qui appelle cette méthode ? | recherche de références | élevée, mais **non transitive** — itérer |
| quelles implémentations de cette interface ? | recherche d'implémentations | élevée — le moyen le plus rapide de lister des stratégies |
| quels symboles dans ce fichier ? | vue d'ensemble des symboles | élevée |
| où sont les occurrences de ce **code métier** ? | ❌ | un code dans un commentaire n'est pas un symbole — **c'est du grep** |
| quel contrat porte cet appel sortant ? | ❌ | l'annotation vit dans un artefact hors du projet indexé — **c'est de la lecture d'archive** |

Les deux dernières lignes sont la source d'erreur la plus fréquente : chercher longtemps avec le bon outil sur une question qu'il ne peut pas traiter.

## Le protocole de démarrage — deux temps, obligatoire

**Un indexeur qui répond vide au premier appel n'est pas en panne : il chauffe.** Il n'importe le projet qu'au premier appel, et sur un dépôt à plusieurs dizaines de modules cet import prend des minutes.

1. Un appel léger sur un fichier connu. **Le résultat ne compte pas, quel qu'il soit.**
2. Attendre — quelques minutes sur un gros dépôt, sans autre appel.
3. Rejouer le même appel. **C'est ce résultat qui fait foi.**
4. Si le second échoue : consigner l'erreur exacte et ne rien retoucher avant d'avoir lu la section suivante.

Conclure à l'échec au premier appel fait basculer tout le run en mode dégradé pour rien — et le plafond de confiance avec lui.

## Les quatre causes, de la plus profonde à la plus visible

### 1. Le magasin de certificats de l'environnement d'exécution embarqué

L'indexeur embarque **son propre environnement d'exécution**, distinct de celui du système. S'il doit atteindre un dépôt d'artefacts interne en TLS et que l'autorité de certification n'est pas dans **ce** magasin, la résolution échoue en cascade : pas de plan de build, pas d'import, pas de classpath, aucun symbole.

**Le piège** : la ligne de commande utilise l'environnement système. Si le certificat n'est que là, `mvn compile` réussit alors que l'indexeur échoue silencieusement. **Ne jamais conclure « les dépendances sont là » sur la foi d'une compilation en ligne de commande.**

*Diagnostic* : chercher `PKIX`, `CertificateException` ou `handshake` dans les journaux de l'indexeur.

### 2. Les marqueurs d'échec de résolution

Quand une résolution de dépendance échoue, le gestionnaire pose un marqueur d'échec dans le dépôt local. **Tant qu'il existe et n'a pas expiré, la résolution n'est pas réessayée** — même si la cause réelle a été corrigée entre-temps.

*Diagnostic* : `find ~/.m2/repository -name '*.lastUpdated' | wc -l`. Purge : le même avec `-delete`.

### 3. Le cache de symboles empoisonné

Si l'indexeur scanne une fois pendant que le classpath est absent, il persiste **des listes de symboles vides comme des résultats valides**, indexées sur le hash du contenu des fichiers. Un fichier non modifié ne sera jamais réévalué : le cache reste empoisonné indéfiniment.

**Aggravant** : le cache est aussi chargé en mémoire au démarrage. Supprimer le fichier en cours de session ne suffit pas.

*Diagnostic* : compter les entrées à zéro symbole dans le cache. Toutes vides = empoisonné. *Réparation* : arrêter le **processus** de l'indexeur, supprimer le cache, relancer.

### 4. Les processus orphelins

Chaque session lance son propre serveur de langage. Si le parent meurt brutalement, l'enfant est reparenté et continue de tourner en immobilisant plusieurs centaines de mégaoctets. Quelques orphelins suffisent à faire échouer l'import suivant, faute de mémoire.

*Diagnostic* : lister les processus dont le parent est le processus initial et dont la ligne de commande porte le serveur de langage.

## Symptôme → suspect

| Symptôme | Suspect | Vérification |
|---|---|---|
| réponse instantanée sur un fichier connu | cache (3) | compter les entrées vides |
| réponse rapide mais toujours vide, plusieurs fichiers | cache (3) ou classpath absent (1, 2) | journaux de l'indexeur |
| terminaison du serveur au premier appel | mémoire (4) | lister les orphelins |
| vide au premier appel après un redémarrage propre | démarrage paresseux | attendre et rejouer |
| délai d'attente sur une recherche globale | index pas prêt | restreindre la recherche à un fichier |

## Fallbacks et plafonds

| Niveau | Ce qu'on perd | Plafond du run |
|---|---|---|
| indexeur sémantique nominal | — | `V` |
| analyse syntaxique sans résolution de types | le dispatch dynamique, les types injectés | `C` |
| recherche textuelle | l'exhaustivité | `I` — **aucune affirmation d'exhaustivité autorisée** |

Le plafond n'est pas une punition : c'est ce qui rend la dégradation **visible dans le document produit** au lieu d'être silencieuse. Il se déclare au gate 0 et s'affiche dans le bandeau des trois documents.
