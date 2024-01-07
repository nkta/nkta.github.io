---
layout: page
title: "Dockerisation d'un projet avec plusieurs pom et src/"
---

# Dockerisation d'un projet avec plusieurs pom et src/

## Structure du Projet

Imaginons que vous ayez une structure de projet comme celle-ci :

```
MonProjet/
├── module1/
│   ├── src/
│   └── pom.xml
├── module2/
│   ├── src/
│   └── pom.xml
└── pom.xml (pom parent)
```

## Dockerfile pour Projet Multi-Modules

Voici un exemple de `Dockerfile` pour construire un projet multi-modules :

```Dockerfile
# Étape 1: Construire l'application en utilisant Maven
FROM maven:3.8.4-openjdk-17-slim AS build
WORKDIR /app

# Copie le pom parent
COPY pom.xml .

# Copie les poms des modules et les résolutions de dépendances
COPY module1/pom.xml module1/
COPY module2/pom.xml module2/
# Si nécessaire, répétez l'opération pour les autres modules...

# Télécharge les dépendances pour le caching
RUN mvn -B dependency:go-offline

# Copie le code source
COPY module1/src module1/src
COPY module2/src module2/src
# Si nécessaire, répétez l'opération pour les autres modules...

# Construit l'application
RUN mvn -B package

# Étape 2: Image minimale pour exécuter l'application
FROM openjdk:17-slim
WORKDIR /app

# Copie le JAR à partir de l'étape de build
# Remplacez `nom_du_jar.jar` par le chemin et le nom de votre JAR exécutable généré
COPY --from=build /app/module1/target/nom_du_jar.jar ./app.jar
# Si votre application est répartie sur plusieurs modules, vous devrez peut-être copier plusieurs JARs ou un JAR uber/fat

ENTRYPOINT ["java","-jar","app.jar"]
```

## Points Importants

1. **Résolution de Dépendances** :
   - Utilisez `RUN mvn -B dependency:go-offline` pour télécharger les dépendances et tirer parti de la mise en cache des couches Docker.

2. **Construction des Modules** :
   - Le `Dockerfile` utilise `RUN mvn -B package` pour construire les modules. Assurez-vous que votre pom parent est configuré correctement pour construire tous les modules.

3. **Copie des JARs** :
   - Assurez-vous de copier le bon JAR exécutable dans votre image Docker. Dans un projet multi-modules, vous pouvez avoir un module spécifique qui génère le JAR exécutable (par exemple, un module `web` pour une application web).

4. **Optimisation de la Construction** :
   - Vous pouvez optimiser davantage votre `Dockerfile` en ne copiant que ce qui est nécessaire pour chaque étape de build pour minimiser la taille de l'image et les temps de build.

5. **Path du JAR** :
   - Assurez-vous de remplacer `nom_du_jar.jar` par le chemin et le nom correct du JAR généré par la construction Maven.

## Docker Compose (Facultatif)

Si vous utilisez Docker Compose et que vous avez besoin de construire plusieurs images pour différents modules, vous pouvez définir chaque module comme un service dans votre `docker-compose.yml` et spécifier un `Dockerfile` différent pour chaque service, si nécessaire.
   - À la racine de votre projet, créez un fichier `docker-compose.yml` avec le contenu suivant :
     ```yaml
     version: '3.8'
     services:
       app:
         build: .
         ports:
           - "8080:8080" # Port de l'application
           - "5005:5005" # Port pour le débogage à distance
         environment:
           - JAVA_TOOL_OPTIONS=-agentlib:jdwp=transport=dt_socket,server=y,suspend=n,address=*:5005
         volumes:
           - .:/app
           - maven_cache:/root/.m2
     volumes:
       maven_cache:
     ```
   - Adaptez les ports si nécessaire, en fonction des ports que votre application utilise.