# Comment mettre une image Docker dans un registre ?

Mettre une image Docker dans un registre est une étape essentielle dans le cycle de vie d’une application conteneurisée. Cette opération permet de partager l’image avec d’autres membres de votre équipe ou de la déployer sur différents environnements. Voici un guide pas à pas pour y parvenir.

---

## Prérequis

Avant de commencer, assurez-vous d’avoir :

1. **Docker installé** sur votre machine.
2. Accès à un registre Docker comme Docker Hub, GitLab Registry, ou un registre privé.
3. Les **identifiants d’authentification** pour vous connecter au registre.

---

## Étape 1 : Créer une image Docker

Si vous avez déjà une image Docker, vous pouvez passer à l’étape suivante. Sinon, construisez une image à partir d’un fichier Dockerfile. Par exemple :

1. Créez un fichier `Dockerfile` :

   ```dockerfile
   FROM nginx:alpine
   COPY ./index.html /usr/share/nginx/html/index.html
   ```

2. Construisez l’image Docker :

   ```bash
   docker build -t mon-image:1.0 .
   ```

   - `-t mon-image:1.0` : Associe un nom et une version (“tag”) à l’image.
   - `.` : Spécifie le chemin contenant le Dockerfile.

---

## Étape 2 : Se connecter au registre Docker

La plupart des registres nécessitent une authentification. Utilisez la commande suivante :

```bash
docker login [url-du-registre] -u [utilisateur] -p [mot-de-passe]
```

- **Exemple pour Docker Hub** :

  ```bash
  docker login -u mon-utilisateur
  ```

- **Exemple pour un registre privé** :

  ```bash
  docker login registry.mon-entreprise.com -u user\$gitlab
  ```

**Remarque** : Pour plus de sécurité, préférez utiliser l’option `--password-stdin` :

```bash
echo "mot-de-passe" | docker login registry.mon-entreprise.com -u utilisateur --password-stdin
```

---

## Étape 3 : Taguer l’image

Pour envoyer une image à un registre, elle doit être taguée avec le chemin du registre. Par exemple :

```bash
docker tag mon-image:1.0 [url-du-registre]/[nom-projet]/mon-image:1.0
```

- **Exemple pour Docker Hub** :

  ```bash
  docker tag mon-image:1.0 mon-utilisateur/mon-image:1.0
  ```

- **Exemple pour un registre privé** :

  ```bash
  docker tag mon-image:1.0 registry.mon-entreprise.com/mon-projet/mon-image:1.0
  ```

---

## Étape 4 : Pousser l’image vers le registre

Une fois l’image taguée, poussez-la dans le registre avec la commande suivante :

```bash
docker push [url-du-registre]/[nom-projet]/mon-image:1.0
```

- **Exemple pour Docker Hub** :

  ```bash
  docker push mon-utilisateur/mon-image:1.0
  ```

- **Exemple pour un registre privé** :

  ```bash
  docker push registry.mon-entreprise.com/mon-projet/mon-image:1.0
  ```

Docker enverra alors l’image au registre. Vous pourrez voir une progression de l’upload dans le terminal.

---

## Étape 5 : Vérifier l’image dans le registre

Connectez-vous à l’interface web de votre registre (Docker Hub, GitLab, ou autre) pour confirmer que l’image a bien été uploadée. Vous devriez voir l’image avec son tag (par exemple : `mon-image:1.0`).

---

## Étape 6 : Télécharger l’image depuis un autre environnement (optionnel)

Pour utiliser l’image depuis un autre environnement, téléchargez-la avec la commande `docker pull` :

```bash
docker pull [url-du-registre]/[nom-projet]/mon-image:1.0
```

- **Exemple pour Docker Hub** :

  ```bash
  docker pull mon-utilisateur/mon-image:1.0
  ```

- **Exemple pour un registre privé** :

  ```bash
  docker pull registry.mon-entreprise.com/mon-projet/mon-image:1.0
  ```

---

## Conseils utiles

1. **Gérez vos tags avec soin** : Utilisez des conventions claires pour vos versions, comme `1.0`, `1.0.1`, ou `latest`.
2. **Nettoyez vos images locales** : Supprimez les anciennes images inutilisées avec `docker rmi` pour libérer de l’espace disque.
3. **Automatisez avec CI/CD** : Configurez votre pipeline pour pousser automatiquement les images dans un registre après chaque build ou release.

---

Vous avez maintenant les connaissances nécessaires pour uploader vos images Docker dans un registre. Bon travail !

