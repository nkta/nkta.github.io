# Pense-bête des commandes Git essentielles

Git est un outil incontournable pour la gestion de version en développement. Voici un pense-bête des commandes essentielles pour travailler efficacement avec Git.

---

## 1. Configuration de Git

Avant de commencer, configurez Git avec votre nom et votre email :

```sh
# Configurer le nom d'utilisateur
git config --global user.name "Votre Nom"

# Configurer l'email
git config --global user.email "votre.email@example.com"
```

Vérifier la configuration actuelle :

```sh
git config --list
```

---

## 2. Initialisation et clonage

Initialiser un nouveau dépôt Git :

```sh
git init
```

Cloner un dépôt existant :

```sh
git clone URL_DU_DEPOT
```

---

## 3. Gestions des fichiers

Voir l'état actuel des fichiers :

```sh
git status
```

Ajouter un fichier à l'index :

```sh
git add NOM_DU_FICHIER
```

Ajouter tous les fichiers modifiés :

```sh
git add .
```

Annuler l'ajout d'un fichier :

```sh
git reset NOM_DU_FICHIER
```

---

## 4. Commit et historique

Faire un commit avec un message :

```sh
git commit -m "Message du commit"
```

Modifier le dernier commit :

```sh
git commit --amend -m "Nouveau message"
```

Voir l'historique des commits :

```sh
git log
```

Voir les commits sous forme compacte :

```sh
git log --oneline --graph --decorate --all
```

---

## 5. Gestion des branches

Lister les branches locales :

```sh
git branch
```

Créer une nouvelle branche :

```sh
git branch NOM_DE_LA_BRANCHE
```

Basculer sur une branche existante :

```sh
git checkout NOM_DE_LA_BRANCHE
```

Créer et basculer sur une nouvelle branche directement :

```sh
git checkout -b NOM_DE_LA_BRANCHE
```

Supprimer une branche locale :

```sh
git branch -d NOM_DE_LA_BRANCHE
```

Supprimer une branche distante :

```sh
git push origin --delete NOM_DE_LA_BRANCHE
```

---

## 6. Gestion des mises à jour et fusions

Récupérer les dernières modifications sans les fusionner :

```sh
git fetch
```

Récupérer et fusionner les modifications d'une branche distante :

```sh
git pull origin NOM_DE_LA_BRANCHE
```

Fusionner une branche dans la branche courante :

```sh
git merge NOM_DE_LA_BRANCHE
```

Résoudre un conflit de fusion :

1. Modifier les fichiers concernés.
2. Ajouter les modifications : `git add .`
3. Finaliser la fusion avec un commit : `git commit -m "Fusion corrigée"`

---

## 7. Gestion des dépôts distants

Lister les dépôts distants :

```sh
git remote -v
```

Ajouter un dépôt distant :

```sh
git remote add origin URL_DU_DEPOT
```

Changer l'URL d'un dépôt distant :

```sh
git remote set-url origin NOUVELLE_URL
```

Envoyer les modifications vers un dépôt distant :

```sh
git push origin NOM_DE_LA_BRANCHE
```

Forcer l'envoi des modifications (attention, cela peut écraser l'historique) :

```sh
git push --force
```

---

## 8. Revert, reset et nettoyage

Revenir à un commit précédent sans modifier l'historique :

```sh
git revert ID_DU_COMMIT
```

Réinitialiser un fichier à son état du dernier commit :

```sh
git checkout -- NOM_DU_FICHIER
```

Supprimer tous les fichiers non suivis :

```sh
git clean -f
```

Réinitialiser complètement un dépôt local (attention, cela efface toutes les modifications locales) :

```sh
git reset --hard
```

Revenir à un commit précis et supprimer tous les commits suivants :

```sh
git reset --hard ID_DU_COMMIT
```

---

## 9. Stash : Mettre de côté des modifications

Sauvegarder temporairement des modifications non commitées :

```sh
git stash
```

Lister les stashs enregistrés :

```sh
git stash list
```

Appliquer le dernier stash et le supprimer de la liste :

```sh
git stash pop
```

Appliquer un stash sans le supprimer de la liste :

```sh
git stash apply
```

---

Ce pense-bête Git couvre les commandes essentielles pour naviguer dans un projet et gérer efficacement son code source. En le gardant sous la main, vous gagnerez en rapidité et en productivité ! 🚀

