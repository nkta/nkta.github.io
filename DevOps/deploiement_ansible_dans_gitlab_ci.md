### **Automatiser le Déploiement avec Ansible et GitLab CI/CD : Un Guide Complet**

L'automatisation du déploiement est une étape clé dans le cycle de vie de développement logiciel, et combiner GitLab CI/CD avec Ansible est une solution puissante pour cela. GitLab CI permet d'automatiser l'intégration continue et le déploiement de votre code, tandis qu'Ansible gère les tâches complexes de configuration et de provisionnement des serveurs. Cet article vous guidera à travers la configuration d'Ansible avec GitLab CI, y compris la gestion des **tokens d'accès**, des **clés SSH**, et des **playbooks Ansible** pour assurer une exécution fluide.

---

### **Pourquoi GitLab CI et Ansible ?**

- **GitLab CI** : Permet d'automatiser les tâches telles que les tests, la construction, le déploiement et plus encore via des pipelines définis dans des fichiers `.gitlab-ci.yml`.
- **Ansible** : Un outil open-source de gestion de configuration qui automatise les tâches comme l'installation de packages, la gestion de services, ou le déploiement d'applications sur des serveurs distants.

L'intégration d'Ansible dans un pipeline CI/CD avec GitLab vous permet de :
- Automatiser complètement le déploiement sur les serveurs de production ou de staging.
- Gérer les configurations serveurs et les dépendances applicatives de manière déclarative.
- Simplifier le provisionnement des infrastructures.

---

### **Étape 1 : Créer et Configurer un Token d'Accès GitLab**

#### **Pourquoi un Token d'Accès ?**

Pour permettre à GitLab CI de cloner un dépôt Git privé, vous devez configurer un **Token d’Accès Personnel** (PAT) ou utiliser une clé SSH. Le PAT est plus simple à configurer et peut être utilisé pour accéder aux dépôts Git via HTTPS.

#### **Comment créer un Token d'Accès ?**

1. **Accéder aux Paramètres du Compte GitLab** :
   - Allez dans GitLab, ouvrez votre profil, et accédez à **Settings** > **Access Tokens**.

2. **Générer un Token d’Accès** :
   - Donnez un nom à votre token (par exemple `GitLab CI Token`).
   - Définissez les **scopes** nécessaires : `read_repository` pour la lecture des dépôts.
   - Cliquez sur **Create personal access token** et **copiez-le immédiatement**.

#### **Ajouter le Token à GitLab CI**

Une fois le token généré, il doit être ajouté à GitLab CI comme variable d'environnement :

1. **Dans votre projet GitLab** :
   - Allez dans **Settings** > **CI/CD** > **Variables**.
   - Cliquez sur **Add Variable** :
     - **Key** : `ANSIBLE_GITLAB_TOKEN`
     - **Value** : Collez le token généré.
     - **Masqué** et **Protégé** : Cochez ces options pour la sécurité.

#### **Utiliser le Token dans `.gitlab-ci.yml`**

Voici un exemple de configuration GitLab CI pour cloner un dépôt via HTTPS en utilisant le token :

```yaml
clone_repository:
  stage: clone
  image: registry.hop.fr/docker.io/alpine
  before_script:
    - apk update && apk add --no-cache git
    # Cloner le dépôt Git avec le token d'accès personnel
    - git config --global http.sslVerify false
    - git clone https://oauth2:${ANSIBLE_GITLAB_TOKEN}@gitlab.hop.fr/infrastructure/ansible/hop.git
```

---

### **Étape 2 : Configurer l’Accès SSH pour GitLab CI**

Si vous préférez utiliser SSH pour cloner les dépôts GitLab, voici comment configurer l'accès par clés SSH dans GitLab CI.

#### **Générer une Clé SSH**

Sur votre machine locale ou dans l'environnement CI, générez une paire de clés SSH :

```bash
ssh-keygen -t rsa -b 4096 -C "votre.email@exemple.com"
```

Cela génère deux fichiers :
- **id_rsa** : La clé privée.
- **id_rsa.pub** : La clé publique.

#### **Ajouter la Clé Publique à GitLab**

1. **Accédez à GitLab** :
   - Allez dans **Settings** > **SSH Keys**.
   - Collez le contenu de votre fichier `id_rsa.pub`.

#### **Ajouter la Clé Privée à GitLab CI**

Dans votre projet GitLab, ajoutez la clé privée comme variable CI :

1. **Allez dans Settings > CI/CD > Variables** :
   - **Key** : `SSH_PRIVATE_KEY`
   - **Value** : Collez le contenu de votre fichier `id_rsa`.

#### **Configurer `.gitlab-ci.yml` pour Utiliser SSH**

Modifiez votre fichier `.gitlab-ci.yml` pour utiliser la clé SSH pour le clonage des dépôts :

```yaml
clone_repository:
  stage: clone
  image: registry.hop.fr/docker.io/alpine
  before_script:
    - apk update && apk add --no-cache git openssh-client
    # Configurer SSH pour cloner le dépôt
    - mkdir -p ~/.ssh
    - echo "$SSH_PRIVATE_KEY" | tr -d '\r' > ~/.ssh/id_rsa
    - chmod 600 ~/.ssh/id_rsa
    - ssh-keyscan gitlab.hop.fr >> ~/.ssh/known_hosts
    # Cloner via SSH
    - git clone git@gitlab.hop.fr:infrastructure/ansible/hop.git
```

---

### **Étape 3 : Configurer Ansible dans GitLab CI**

Une fois que vous avez configuré l'accès Git, vous devez configurer Ansible pour gérer vos déploiements.

#### **Installer Ansible dans le Pipeline GitLab CI**

Pour exécuter Ansible dans GitLab CI, installez-le via `apk` (gestionnaire de paquets Alpine) et configurez votre environnement pour les dépendances Ansible.

Voici un exemple de configuration pour installer Ansible et exécuter un playbook :

```yaml
deploy_application:
  stage: deploy
  image: registry.hop.fr/docker.io/alpine
  before_script:
    - apk update && apk add --no-cache git openssh-client python3 py3-pip ansible
  script:
    - cd hop
    # Exécuter un playbook Ansible pour déployer l'application
    - ansible-playbook $ANSIBLE_PROJECT_FILENAME -i hosts/test.yml -u $ANSIBLE_SSH_USER --private-key ~/.ssh/id_rsa -e "ansible_ssh_pass=$SSH_PASSWORD ansible_become_pass=$SUDO_PASSWORD version=$VERSION"
```

#### **Variables Sensibles dans GitLab CI**

Ajoutez les variables sensibles comme le mot de passe SSH ou le mot de passe sudo dans **CI/CD > Settings > Variables**. Par exemple :

- **ANSIBLE_SSH_USER** : L'utilisateur SSH pour Ansible.
- **SSH_PASSWORD** : Mot de passe pour l'utilisateur SSH (si nécessaire).
- **SUDO_PASSWORD** : Mot de passe sudo pour les tâches nécessitant des privilèges élevés.

---

### **Étape 4 : Gérer les Dépendances Python avec un Environnement Virtuel**

Si vous avez besoin d’installer des modules Python supplémentaires (comme `hvac` pour interagir avec HashiCorp Vault), vous pouvez créer un environnement virtuel Python.

Voici un exemple pour installer des dépendances Python dans un environnement virtuel :

```yaml
install_dependencies:
  stage: setup
  image: registry.hop.fr/docker.io/alpine
  before_script:
    - apk update && apk add --no-cache python3 py3-pip
    - python3 -m venv /opt/venv
    - source /opt/venv/bin/activate
    - pip install hvac
  script:
    - source /opt/venv/bin/activate
    - ansible-playbook playbook.yml
```

---

### **Conclusion**

En configurant GitLab CI avec Ansible, vous pouvez automatiser entièrement vos déploiements, qu'il s'agisse de la configuration des serveurs ou du déploiement d'applications. Voici un résumé des étapes principales :

1. **Configurer un Token d'Accès Personnel** ou **Clé SSH** pour cloner des dépôts Git privés.
2. **Configurer Ansible** dans votre pipeline GitLab CI pour automatiser le déploiement.
3. **Gérer les variables sensibles** comme les mots de passe SSH et sudo dans les paramètres GitLab CI.
4. **Utiliser un environnement virtuel Python** pour installer des dépendances supplémentaires si nécessaire.

Avec ce pipeline en place, vous pouvez déployer vos applications de manière sécurisée et automatisée, tout en bénéficiant de la flexibilité d'Ansible et de la puissance de GitLab CI.