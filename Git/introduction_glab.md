## glab : amener GitLab dans ton terminal

### Introduction

Dans les workflows modernes de développement, on alterne souvent entre la ligne de commande (git, éditeur de code) et l’interface web de GitLab pour des opérations comme créer des issues, des merge requests, vérifier les pipelines, etc. **glab** est un outil CLI (interface en ligne de commande) open source qui permet de faire beaucoup de ces actions directement depuis le terminal, sans avoir à retourner dans le navigateur.

GitLab a officiellement adopté **glab** comme leur outil CLI “officiel”, ce qui renforce son importance dans l’écosystème GitLab. Donc, si tu veux fluidifier ta productivité, glab est un outil intéressant à maîtriser.

---

## Fonctionnalités principales

Voici quelques‑unes des capacités majeures de **glab** :

| Domaine                   | Ce que tu peux faire avec glab                                                                                  |
| ------------------------- | --------------------------------------------------------------------------------------------------------------- |
| Authentification          | `glab auth login`, configurer via token, gérer plusieurs hôtes                                                  |
| Issues                    | lister, créer, modifier des issues : `glab issue list`, `glab issue update`                                     |
| Merge Requests (MR)       | créer, consulter, approuver, fusionner une MR : `glab mr create`, `glab mr view`, `glab mr merge`               |
| Pipelines / CI            | suivre l’état d’un pipeline, lancer une exécution, lister les jobs : `glab ci list`, `glab pipeline view`, etc. |
| Repositories / Projets    | cloner un dépôt, créer un nouveau projet, archiver : `glab repo clone`, `glab repo create`                      |
| Variables & configuration | gérer les variables de projet ou de groupe, configurer le CLI lui-même                                          |
| Accès à l’API             | `glab api` permet d’appeler directement l’API GitLab depuis le CLI                                              |
| Autres commandes          | labels, releases, snippet, ssh‑key, schedule, etc.                                                              |

---

## Installation & configuration

### Installation

L’installation varie selon ton système :

* **Linux** : via paquet binaire, snap, apt selon distribution, ou compilation depuis la source.
* **macOS** : via Homebrew, par exemple `brew install glab`.
* **Windows** : via WinGet, Scoop ou un installateur exécutable.
* **Via asdf** (gestionnaire de versions multi‑langages et outils) :

  ```bash
  asdf plugin add glab https://github.com/vitalis/asdf-glab.git
  asdf install glab latest
  asdf global glab latest
  ```

  Cela permet de gérer plusieurs versions de glab et de rester à jour facilement.

Après installation, tu peux vérifier avec :

```bash
glab version
```

### Authentification

Pour utiliser glab, il faut l’authentifier auprès de GitLab. Ça se fait généralement via un **Personal Access Token** (PAT) :

```bash
glab auth login
```

Tu peux aussi passer le token par stdin ou avec des flags (`--token`, `--hostname`) selon le contexte (GitLab.com ou instance auto‑hébergée).
Ensuite, glab conserve une configuration dans `~/.config/glab-cli` (et un fichier local `.git/glab-cli` dans un projet) pour stocker les paramètres.

---

## Exemple de workflow avec glab

1. Tu fais une feature sur une branche locale.
2. Tu veux ouvrir une MR pour intégrer ta branche.

   ```bash
   glab mr create
   ```
3. Tu veux visualiser le pipeline en cours ou les logs :

   ```bash
   glab pipeline view
   ```
4. Tu veux approuver ou fusionner la MR :

   ```bash
   glab mr approve
   glab mr merge
   ```

Tu peux aussi lister les issues qui t’ont été assignées :

```bash
glab issue list
```

Ou cloner un repo GitLab sans avoir à copier l’URL :

```bash
glab repo clone mon-groupe/mon-projet
```

---

## Conclusion

**glab** est une très belle avancée pour ceux qui veulent travailler efficacement avec GitLab sans quitter leur terminal. Grâce à son intégration avec des gestionnaires comme **asdf**, son installation et sa mise à jour deviennent encore plus simples. Il ne remplacera peut‑être jamais complètement l’interface web pour certains cas très visuels, mais pour la majorité des actions courantes (issues, MR, pipelines), c’est un excellent compagnon.
