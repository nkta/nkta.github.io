# GitWand : le client Git qui arrête de vous faire arbitrer les conflits triviaux

Il y a un moment très précis dans la vie d'un développeur où la motivation s'effondre : celui où un `git merge` renvoie douze fichiers en rouge. On sait déjà, avant même d'ouvrir le premier, que dix d'entre eux ne demandent aucune réflexion — un `package-lock.json` où les deux branches ont bumpé une version, un fichier de config où une seule des deux branches a réellement modifié quelque chose, un import ajouté en haut de fichier des deux côtés. Le travail intellectuel est nul. Le coût en attention, lui, est bien réel.

C'est exactement le problème que **GitWand** attaque, et uniquement celui-là.

## Le pari : du déterminisme, pas un LLM lâché sur vos merges

GitWand est un client Git natif, open source sous licence MIT, développé par Laurent Guitton (Devlint). Sa proposition centrale n'est pas « une IA résout vos conflits », mais l'inverse : **classer chaque hunk conflictuel selon des règles fixes et ne résoudre automatiquement que les cas où le résultat ne fait aucun doute**.

Concrètement, le moteur s'appuie sur une petite dizaine de patterns déterministes, dont les noms disent bien de quoi il s'agit : `whitespace_only`, `same_change` (les deux branches ont écrit strictement la même chose), `one_side_change`, `reorder_only`, `insertion_at_boundary`, `value_only_change` (typiquement un numéro de version)… Et un pattern fourre-tout, `complex`, pour les modifications qui se chevauchent réellement — celui-là n'est jamais résolu automatiquement.

Chaque hunk reçoit un **score de confiance** et une **trace de décision** : quel pattern a matché, pourquoi, et quelle résolution en découle. Le site affiche l'exemple canonique :

```
<<<<<<< HEAD
const theme = 'dark'
=======
const theme = localStorage.getItem('theme') ?? 'dark'
>>>>>>> feature/settings
```

Résolu en `const theme = localStorage.getItem('theme') ?? 'dark'`, avec la mention *confiance 97 % · prefer-theirs · semantic*. Ce n'est pas magique, c'est un `one_side_change` reconnu comme tel — et surtout, c'est auditable.

L'annonce marketing est de 95 % des conflits triviaux résolus automatiquement, avec un argument que j'aime bien : **zéro hallucination**. Pas parce que le modèle est bon, mais parce qu'il n'y a pas de modèle sur le chemin critique. L'IA n'intervient qu'en *fallback*, sur les hunks complexes, et toujours en opt-in.

## Le reste du client Git : correct, et rapide

Un moteur de résolution ne suffit pas à faire adopter un client. GitWand couvre le workflow quotidien complet : vue des changements avec staging au niveau du hunk, historique complet et graphe DAG interactif, blame, recherche de commits, gestion des branches, push/pull avec compteurs ahead/behind et auto-fetch en tâche de fond.

Deux points valent le détour :

- **La prévisualisation de merge.** Avant de merger, GitWand prédit le résultat sans toucher au working tree, avec un découpage fichier par fichier : auto-résolvable, ou à relire. Un badge résume l'ensemble — merge propre, 100 % auto-résolvable, ou N conflits à traiter. Savoir *avant* de lancer la commande, c'est déjà la moitié du confort.
- **La revue de Pull Request intégrée**, avec commentaires inline, statut CI et annotations de checks superposées directement sur le diff. Le multi-forge est supporté : GitHub, GitLab, Bitbucket, Azure DevOps.

Côté technique, le choix est **Tauri 2 + Rust**, avec un front Vue 3 — donc pas d'Electron. Le binaire tourne autour de 8 Mo, avec un démarrage à froid annoncé sous la seconde, un fast-path libgit2 et des panneaux chargés paresseusement. Quand on a l'habitude des 150 Mo et du café pendant le lancement, la différence se sent.

Le même moteur est exposé via trois interfaces : l'application desktop (macOS Intel et Apple Silicon, Linux en `.deb`/`.AppImage`/`.rpm`, Windows en `.exe`/`.msi`/winget), une CLI (`npm i -g @gitwand/cli`) et une extension VS Code. Interface disponible en français.

## Le vrai angle mort de l'IA : le serveur MCP

C'est la partie que je trouve la plus intéressante, et la plus juste conceptuellement.

Les agents de code sont excellents pour écrire du code et catastrophiques sur les merges — parce qu'un merge n'est pas un problème de génération, c'est un problème d'arbitrage entre trois états d'un même fichier. Lâcher un LLM dessus, c'est accepter qu'il invente une synthèse plausible plutôt que correcte.

GitWand inverse la répartition des rôles. Son serveur MCP expose le moteur de résolution aux agents : l'agent demande une vue d'ensemble, récupère les hunks déjà tranchés déterministiquement, et ne garde que les cas ambigus — avec `ours`, `theirs`, `base` et la trace de décision sous les yeux. **Le modèle ne touche que ce qu'aucune règle ne sait traiter.** C'est exactement l'inverse de ce qu'on voit d'habitude.

L'installation tient en une ligne avec Claude Code :

```bash
claude mcp add gitwand -- npx -y @gitwand/mcp
```

Le serveur tourne en local sur stdio, sans clé d'API ni accès réseau, et il est référencé sur le MCP Registry officiel — donc découvrable automatiquement par les clients qui parcourent le registre. Claude Desktop, Cursor, Windsurf, opencode et Continue sont également supportés via le bloc `mcpServers` classique.

Pour les fonctions IA natives de l'application (génération de messages de commit, titres et descriptions de PR, revue de code inline, squash sémantique, recherche de commits en langage naturel), on branche son propre backend : API Claude, endpoint compatible OpenAI, Ollama en local, ou un agent CLI déjà installé. Votre clé, votre modèle.

## Où GitWand se situe face aux autres

| | GitWand | GitHub Desktop | GitKraken |
|---|---|---|---|
| Résolution auto déterministe | ✓ | ✗ | IA uniquement |
| Gratuit / open source | ✓ | ✓ | ✗ |
| Natif (sans Electron) | ✓ | ✗ | ✗ |
| Serveur MCP pour agents | ✓ | ✗ | ✓ |

Il faut aussi citer le voisinage direct : `git rerere`, qui rejoue les résolutions que vous avez déjà faites à la main, et Mergiraf, qui s'accroche à `git merge` et arbitre en lisant l'arbre syntaxique du code. GitWand se distingue moins par l'idée que par le packaging : un moteur explicable, trois interfaces, et une porte d'entrée MCP.

## Ce qu'il faut garder en tête

Le projet est jeune, et ça se voit. Le rythme de sortie est très rapide — v3.6 au moment où j'écris, avec des versions majeures qui s'enchaînent en quelques mois — ce qui est bon signe pour la vitalité, moins pour la stabilité si vous en faites votre outil unique dès demain. Les critiques les plus dures pointent la part de code généré par IA dans le dépôt. À vous de juger sur pièces : le code est sous MIT, publiquement lisible, et les issues aussi.

Le télémétrie mérite une mention honnête : depuis une version récente, l'application envoie un ping anonyme unique au lancement — pas d'identifiant utilisateur, pas d'empreinte machine, pas d'événements d'analytics — désactivable dans les réglages.

## Verdict

GitWand ne cherche pas à remplacer votre client Git parce qu'il serait plus joli. Il résout un problème étroit, mesurable et quotidien, avec la bonne méthode : des règles avant les modèles, une trace pour chaque décision, et l'IA reléguée là où elle est réellement utile — les 5 % de cas où il faut effectivement réfléchir.

Si vous travaillez sur des branches longues, dans un monorepo, ou avec une équipe qui touche aux mêmes fichiers de config, l'essai coûte un téléchargement et rien d'autre : gratuit, sans compte, MIT.

- Site : [gitwand.app](https://gitwand.app/)
- Dépôt : [github.com/devlint/GitWand](https://github.com/devlint/GitWand)
