# Structurer un Projet Ansible de Façon Professionnelle avec Ansible Galaxy

## Introduction

Ansible est un outil puissant pour l’automatisation et la gestion de la configuration des infrastructures. Pour un projet bien organisé, il est essentiel de structurer ses rôles et dépendances de manière professionnelle. Dans cet article, nous allons explorer différentes manières d'utiliser `ansible-galaxy`, avec des exemples pratiques pour simplifier la gestion des rôles et collections.

---

## 1. Organisation d'un Projet Ansible

Avant d’utiliser `ansible-galaxy`, il est important d’avoir une structure de projet claire. Voici un exemple de structure recommandée :

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
├── collections/
├── playbooks/
│   ├── deploy.yml
│   └── setup.yml
├── requirements.yml
└── README.md
```

Dans cette structure, nous allons voir comment utiliser `ansible-galaxy` pour gérer efficacement les rôles et collections.

---

## 2. Utilisation de `ansible-galaxy` pour Gérer les Rôles

### a. Installer un rôle depuis Ansible Galaxy

Ansible Galaxy est une plateforme où l'on peut télécharger et partager des rôles Ansible. Pour installer un rôle depuis Galaxy, utilisez la commande suivante :

```bash
ansible-galaxy install geerlingguy.nginx
```

Cela installera le rôle dans `~/.ansible/roles/` par défaut.

Si vous souhaitez l’installer dans un dossier spécifique, utilisez :

```bash
ansible-galaxy install -p roles/ geerlingguy.nginx
```

---

### b. Installer un rôle depuis un dépôt Git

Plutôt que d’avoir des rôles locaux, il est préférable de les stocker dans des dépôts Git distincts et de les inclure via `requirements.yml`.

Exemple de fichier `requirements.yml` :

```yaml
roles:
  - name: webserver
    src: git+https://gitlab.com/your-namespace/ansible-webserver.git
    version: main
  - name: database
    src: git+https://gitlab.com/your-namespace/ansible-database.git
    version: main
```

Pour installer ces rôles, exécutez :

```bash
ansible-galaxy install -r requirements.yml --force
```

Cela garantit que tous les contributeurs du projet utilisent les mêmes versions des rôles.

---

## 3. Organisation des Rôles dans GitLab

Lorsque vous travaillez avec GitLab, il est recommandé d’organiser vos rôles sous forme de dépôts distincts dans un groupe spécifique, par exemple :

```
GitLab Group: ansible-roles
  ├── ansible-role-webserver
  ├── ansible-role-database
  ├── ansible-role-monitoring
```

Ensuite, utilisez `requirements.yml` pour les récupérer dynamiquement.

Dans votre CI/CD, vous pouvez ajouter un job pour vérifier la qualité des rôles :

```yaml
stages:
  - lint

ansible-lint:
  stage: lint
  script:
    - ansible-lint roles/
```

---

## 4. Conseils pour Écrire un Bon Rôle Ansible

### a. Suivre une Structure Standardisée
Un rôle bien structuré suit une organisation standard :

```
roles/
  webserver/
    tasks/
      main.yml
    handlers/
      main.yml
    templates/
    files/
    vars/
      main.yml
    defaults/
      main.yml
    meta/
      main.yml
```

### b. Utiliser des Variables avec Précaution
- Définir les valeurs par défaut dans `defaults/main.yml`.
- Ne pas surcharger `vars/main.yml`, sauf si nécessaire.

### c. Écrire des Handlers pour Optimiser les Exécutions
Les handlers permettent d'éviter les redémarrages inutiles :

```yaml
- name: Redémarrer Nginx
  service:
    name: nginx
    state: restarted
  listen: "nginx-restart"
```

### d. Tester et Valider les Rôles
- Utiliser `ansible-lint` pour s’assurer de la qualité du code.
- Tester avec `molecule` avant de publier un rôle :

```bash
molecule test
```

---

## 5. Gérer les Collections Ansible avec `ansible-galaxy`

Ansible Galaxy permet également de gérer des collections, qui sont des ensembles de rôles, modules et plugins. Pour installer une collection, utilisez :

```bash
ansible-galaxy collection install community.general
```

Pour inclure une collection dans un fichier `requirements.yml` :

```yaml
collections:
  - name: ansible.posix
  - name: community.general
```

Puis installez les collections avec :

```bash
ansible-galaxy collection install -r requirements.yml
```

---

## 6. Utilisation des Rôles et Collections dans un Playbook

Une fois les rôles et collections installés, vous pouvez les utiliser dans vos playbooks :

```yaml
- hosts: webservers
  roles:
    - role: webserver

- hosts: databases
  roles:
    - role: database
```

---

## 7. Automatiser l’Installation avec un Pipeline CI/CD

Dans un pipeline GitLab CI/CD, on peut inclure une étape pour installer les dépendances :

```yaml
stages:
  - setup

install_roles:
  stage: setup
  script:
    - ansible-galaxy install -r requirements.yml --force
    - ansible-galaxy collection install -r requirements.yml
```

Cela garantit que l’environnement d’exécution dispose de tous les rôles et collections nécessaires.

---

## 8. Conclusion

Utiliser `ansible-galaxy` pour gérer les rôles et collections permet d’améliorer la modularité et la maintenabilité d’un projet Ansible. En stockant les rôles dans des dépôts Git distincts et en utilisant un fichier `requirements.yml`, il est plus facile de partager et d’automatiser leur gestion. De plus, l’intégration dans un pipeline CI/CD assure un environnement homogène à chaque déploiement.

L'organisation dans GitLab et la standardisation des rôles permettent une meilleure collaboration et un code plus robuste, assurant ainsi la pérennité des infrastructures gérées avec Ansible.

