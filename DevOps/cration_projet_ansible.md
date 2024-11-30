## Structurer un Projet Ansible de Façon Professionnelle : Guide Pratique

Ansible est un outil très puissant pour l'automatisation et la gestion de la configuration, mais comme tout projet d'ingénierie, sa structure est essentielle pour en tirer le meilleur parti. Une bonne structuration permet de maintenir la lisibilité, de faciliter la collaboration, et d'assurer la scalabilité. Dans cet article, nous allons voir comment structurer un projet Ansible de manière professionnelle, afin d'éviter les écueils communs et de créer une base solide pour la gestion de votre infrastructure.

### 1. L'Organisation de la Structure de Dossiers

La structuration d'un projet Ansible commence par une organisation logique des dossiers et fichiers. Voici une structure recommandée qui suit les meilleures pratiques :

```
project-ansible/
├── ansible.cfg
├── inventory/
│   ├── production
│   └── staging
├── group_vars/
│   ├── all.yml
│   ├── production.yml
│   └── staging.yml
├── host_vars/
│   └── my_host.yml
├── roles/
│   ├── webserver/
│   │   ├── tasks/
│   │   ├── templates/
│   │   ├── handlers/
│   │   ├── files/
│   │   └── defaults/
│   └── database/
├── playbooks/
│   ├── deploy.yml
│   └── setup.yml
├── requirements.yml
└── README.md
```

- **ansible.cfg** : Fichier de configuration pour Ansible. Centralisez ici des options comme l'inventaire par défaut, la journalisation, et les paramètres liés à SSH.
- **inventory/** : Contient les fichiers d'inventaire, tels que *production* et *staging*, permettant de définir quels hôtes seront ciblés par vos playbooks.
- **group_vars/** : Définit les variables communes à des groupes d'hôtes. Cette section est importante pour éviter de dupliquer des informations dans plusieurs fichiers.
- **host_vars/** : Contient des variables spécifiques à un seul hôte. Cela permet de personnaliser des déploiements précis sans modifier la logique globale.
- **roles/** : Les rôles facilitent la réutilisation de tâches communes (exemple : *webserver*, *database*). Chaque rôle est divisé en sous-dossiers comme *tasks*, *templates*, et *handlers* pour une meilleure organisation.
- **playbooks/** : Contient vos playbooks Ansible principaux. Chaque playbook décrit une série de tâches à exécuter sur un inventaire d'hôtes.
- **requirements.yml** : Contient la liste des collections ou plugins Ansible nécessaires au projet.

#### Exemple

Supposons que vous souhaitiez déployer un serveur web Apache et une base de données MySQL. Vous pouvez créer deux rôles distincts : *webserver* et *database*. Votre structure pourrait ressembler à ceci :

```
roles/
├── webserver/
│   ├── tasks/
│   │   ├── main.yml
│   ├── templates/
│   │   ├── httpd.conf.j2
│   └── handlers/
│       └── main.yml
├── database/
│   ├── tasks/
│   │   ├── main.yml
│   └── handlers/
│       └── main.yml
```

Dans le rôle *webserver*, le fichier `tasks/main.yml` pourrait contenir les étapes pour installer Apache :

```yaml
---
- name: Installer Apache
  apt:
    name: apache2
    state: present

- name: Copier la configuration Apache
  template:
    src: httpd.conf.j2
    dest: /etc/apache2/apache2.conf
  notify:
    - Redémarrer Apache
```

Le fichier `handlers/main.yml` pourrait contenir :

```yaml
---
- name: Redémarrer Apache
  service:
    name: apache2
    state: restarted
```

Pour la base de données, `tasks/main.yml` pourrait être :

```yaml
---
- name: Installer MySQL
  apt:
    name: mysql-server
    state: present
```

### 2. La Définition des Rôles (Roles)

La création de rôles est un moyen idéal pour rendre votre projet modulaire et maintenable. Voici quelques conseils pour structurer vos rôles :

- **tasks/** : Décomposez les actions à accomplir dans des fichiers distincts si nécessaire (par exemple, `main.yml`, `install.yml`, `config.yml`).
- **handlers/** : Les handlers sont utilisés pour déclencher des actions à la suite d'un changement (par exemple, redémarrer un service).
- **templates/** : Conservez ici les fichiers *Jinja2* pour la configuration dynamique.
- **files/** : Contient des fichiers statiques à déployer.
- **defaults/** : Définissez les valeurs par défaut des variables. Ces valeurs peuvent être écrasées par des variables définies dans *group_vars*, *host_vars* ou directement dans le playbook.

#### Exemple de Création de Rôles

Imaginons un rôle *nginx* pour déployer un serveur web Nginx. Voici à quoi pourrait ressembler le fichier `tasks/main.yml` :

```yaml
---
- name: Installer Nginx
  apt:
    name: nginx
    state: present

- name: Démarrer et activer Nginx
  service:
    name: nginx
    state: started
    enabled: true
```

Et dans le rôle, nous pourrions avoir un fichier de template `templates/nginx.conf.j2` pour la configuration du serveur :

```
server {
    listen 80;
    server_name {{ domain_name }};

    location / {
        proxy_pass http://127.0.0.1:8080;
    }
}
```

Ce fichier est ensuite utilisé dans une tâche pour générer une configuration personnalisée en fonction des variables d'hôtes ou de groupe.

### 3. Utiliser des Bonnes Pratiques pour l'Inventaire

L'inventaire est le point de départ de chaque exécution de playbook. Utilisez des inventaires différents pour chaque environnement : *production*, *staging*, ou *develop*. Cela évite d'avoir des erreurs qui affectent la production lors de tests. Il est aussi possible d'utiliser un inventaire dynamique si vous travaillez sur une infrastructure cloud qui évolue constamment.

#### Gestion des Inventaires Production et Recette

Pour les environnements de *production* et *recette*, vous pouvez définir des adresses de serveurs spécifiques dans les fichiers d'inventaire `inventory/production` et `inventory/staging`.

Voici un exemple typique :

```
[webservers]
prod-web1.example.com
prod-web2.example.com

[databases]
prod-db1.example.com

[recette-webservers]
recette-web1.example.com
recette-web2.example.com

[recette-databases]
recette-db1.example.com
```

Chaque environnement a ses propres groupes d'hôtes, ce qui permet de gérer de manière distincte les configurations de production et de recette.#### Exemple

Voici un exemple d'inventaire statique :

```
[webservers]
web1.example.com
web2.example.com

[databases]
db1.example.com
```

Et un exemple d'inventaire dynamique avec AWS :

```json
{
  "_meta": {
    "hostvars": {}
  },
  "webservers": [
    "ec2-54-23-12-34.compute-1.amazonaws.com",
    "ec2-52-12-24-56.compute-1.amazonaws.com"
  ],
  "databases": [
    "ec2-34-56-78-90.compute-1.amazonaws.com"
  ]
}
```

### 4. La Configuration du Fichier `ansible.cfg`

Le fichier `ansible.cfg` est essentiel pour centraliser vos paramètres. Quelques options à configurer :

- **inventory** : Spécifiez l'emplacement de votre fichier d'inventaire par défaut.
- **retry_files_enabled** : Désactivez la création de fichiers `.retry` si cela n'est pas utile.
- **host_key_checking** : Désactivez la vérification des clés d'hôte si vous avez des problèmes de connexion à de nouveaux serveurs.

#### Exemple

Voici un exemple de fichier `ansible.cfg` :

```
[defaults]
inventory = ./inventory/production
retry_files_enabled = False
host_key_checking = False
```

### 5. Documentation et Organisation des Variables

Il est crucial de bien documenter vos fichiers, que ce soit en ajoutant un fichier `README.md` à chaque rôle ou en utilisant des commentaires clairs dans vos playbooks. Pour les variables, préférez utiliser `group_vars` pour celles qui sont partagées et `host_vars` pour des spécificités locales, en gardant en tête la portée et l'écrasement potentiel.

### 5.1 Variables Globales, Liées à un Environnement, Externes

Il est souvent nécessaire d'utiliser des variables globales qui sont partagées à travers plusieurs environnements ou qui peuvent provenir de sources externes, comme des fichiers de configuration spécifiques à chaque environnement.

Pour cela, vous pouvez créer un fichier de variables globales dans `group_vars/all.yml` ou utiliser des fichiers externes importés dans votre playbook. Ces fichiers de variables peuvent contenir des informations sensibles ou des paramètres globaux communs à tous les hôtes.

#### Exemple

Dans `group_vars/all.yml` :

```yaml
app_version: "1.2.3"
log_level: "INFO"
max_connections: 100
```

Ces variables seront disponibles pour tous les groupes d'hôtes définis dans votre inventaire. Vous pouvez aussi utiliser un fichier externe pour différencier les environnements :

```
project-ansible/
├── vars/
│   ├── production.yml
│   └── staging.yml
```

Et dans votre playbook, vous pouvez inclure ce fichier en fonction de l'environnement :

```yaml
- name: Charger les variables d'environnement
  include_vars: "vars/{{ env }}.yml"
```

Cela permet de séparer les configurations spécifiques à chaque environnement tout en utilisant un modèle commun de playbooks et de rôles.

#### Exemple

Dans `group_vars/production.yml` :

```yaml
domain_name: "example.com"
nginx_worker_processes: 4
```

Dans `host_vars/web1.example.com.yml` :

```yaml
nginx_worker_connections: 1024
```

### 6. Testing avec Molecule

L'utilisation de **Molecule** est recommandée pour tester vos rôles Ansible. Molecule vous permet de créer un environnement de test (généralement avec Docker) et de valider que vos rôles fonctionnent comme prévu avant de les exécuter en production. 

#### Exemple

Pour tester un rôle avec Molecule, vous pouvez utiliser la commande suivante :

```sh
molecule test
```

Cela va créer un environnement, appliquer le rôle, vérifier son bon fonctionnement, puis détruire l'environnement. Voici un exemple de fichier `molecule.yml` :

```yaml
---
driver:
  name: docker

platforms:
  - name: instance
    image: ubuntu:latest

provisioner:
  name: ansible

verifier:
  name: ansible
```

### 7. Gestion des Plugins avec `requirements.yml`

Lorsque vous utilisez des plugins ou des collections externes dans Ansible, il est recommandé de les définir dans un fichier `requirements.yml`. Ce fichier permet de centraliser la liste des dépendances du projet, facilitant ainsi leur installation et la reproductibilité du projet.

#### Exemple de Fichier `requirements.yml`

Voici un exemple de fichier `requirements.yml` pour un projet Ansible :

```yaml
---
collections:
  - name: community.general
    version: "3.4.0"
  - name: ansible.posix
    version: "1.3.0"

roles:
  - name: geerlingguy.apache
    src: geerlingguy.apache
    version: "4.0.0"
  - name: custom_role
    src: git@gitlab.com:your_namespace/custom_role.git
    version: "1.0.0"
```

Avec ce fichier, vous pouvez installer toutes les collections et rôles en une seule commande :

```sh
ansible-galaxy install -r requirements.yml
```

Cela garantit que toutes les dépendances nécessaires à votre projet sont correctement installées, rendant votre projet plus portable et facile à partager.

### 8. Automatiser avec CI/CD

L'inclusion d'un processus CI/CD est cruciale pour assurer la qualité de votre code Ansible. Des outils comme Jenkins, GitLab CI ou GitHub Actions peuvent être configurés pour tester et déployer automatiquement les modifications. Cela permet d'éviter les erreurs humaines et de maintenir une infrastructure en état de marche.

#### Exemple

Avec GitHub Actions, vous pouvez créer un workflow pour exécuter vos tests Molecule automatiquement :

```yaml
name: Ansible Molecule CI

on:
  push:
    branches:
      - main
  pull_request:
    branches:
      - main

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v2

      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.x'

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install molecule docker

      - name: Run Molecule tests
        run: molecule test
```

### Conclusion

Structurer un projet Ansible de manière professionnelle nécessite une approche rigoureuse et une bonne organisation. Une fois la structure mise en place, cela vous permet de gagner en productivité, en fiabilité, et d'assurer une meilleure collaboration avec les autres membres de l'équipe. Suivre ces bonnes pratiques et bien documenter chaque partie de votre projet est la clé du succès.

