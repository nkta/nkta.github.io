### **Sécurisez vos secrets avec Ansible Vault : Guide Complet**

Dans un monde où la sécurité des données est une priorité absolue, **Ansible Vault** se présente comme un outil incontournable pour protéger les informations sensibles dans vos projets Ansible. Que vous soyez débutant ou utilisateur avancé, cet article vous guidera à travers les fonctionnalités essentielles et les possibilités avancées d'Ansible Vault.

---

### **Qu'est-ce qu'Ansible Vault ?**

Ansible Vault est un système intégré dans Ansible qui permet de **chiffrer, gérer et sécuriser** les données sensibles comme les mots de passe, les clés API ou les configurations critiques. En protégeant vos informations avec un chiffrement robuste (AES256), Vault garantit que vos secrets ne tombent pas entre de mauvaises mains.

---

### **Pourquoi utiliser Ansible Vault ?**

Imaginez que votre infrastructure Ansible contient des fichiers YAML exposant vos identifiants ou clés API en clair. Si ces fichiers sont partagés ou sauvegardés sans protection, les risques de fuite sont énormes. Ansible Vault agit comme un **coffre-fort numérique**, empêchant l'accès non autorisé à ces données.

---

### **Les bases : Fonctionnalités essentielles**

#### 1. **Créer un fichier chiffré**
Pour commencer, vous pouvez créer un fichier sécurisé en une seule commande :

```bash
ansible-vault create secrets.yml
```

- Vous entrez un mot de passe qui servira à verrouiller le fichier.
- Le fichier `secrets.yml` est chiffré et illisible sans ce mot de passe.

#### 2. **Lire ou modifier un fichier Vault**
Pour afficher ou modifier un fichier Vault sans compromettre sa sécurité :

- **Afficher :** `ansible-vault view secrets.yml`
- **Modifier :** `ansible-vault edit secrets.yml`

#### 3. **Chiffrer ou déchiffrer un fichier existant**
Vous pouvez protéger un fichier existant ou retirer sa protection :

- **Chiffrer :** `ansible-vault encrypt fichier.yaml`
- **Déchiffrer :** `ansible-vault decrypt fichier.yaml`

---

### **Utilisation des secrets dans vos playbooks**

Une fois vos secrets chiffrés, vous pouvez les utiliser comme n’importe quel fichier YAML. Par exemple, supposons que `secrets.yml` contient :

```yaml
db_username: admin
db_password: my_secure_password
```

Dans votre playbook :

```yaml
- hosts: all
  tasks:
    - name: Affiche le mot de passe
      debug:
        msg: "Mot de passe : {{ db_password }}"
```

Pour exécuter le playbook tout en déverrouillant les secrets, utilisez :

```bash
ansible-playbook playbook.yml --ask-vault-pass
```

---

### **Ajouter un secret contenu dans un fichier en clair à Ansible Vault**

#### **Pourquoi chiffrer un secret contenu dans un fichier en clair ?**
Un fichier en clair contenant des mots de passe, clés API, ou autres informations sensibles est une **vulnérabilité majeure**. Si ce fichier est partagé dans un dépôt Git ou exposé par erreur, vos secrets deviennent accessibles à tout le monde.

#### **Étapes pour chiffrer un secret existant**

##### 1. **Fichier en clair initial**
Prenons un fichier en clair `vars.yml` contenant :

```yaml
db_username: admin
db_password: my_secret_password
api_key: abc12345
```

Vous souhaitez protéger uniquement la valeur de `db_password`.

##### 2. **Chiffrement de la valeur du secret**
Pour chiffrer uniquement la valeur de `db_password`, utilisez la commande suivante :

```bash
ansible-vault encrypt_string 'my_secret_password' --name 'db_password'
```

Cela génère une section chiffrée comme ceci :

```yaml
db_password: !vault |
          $ANSIBLE_VAULT;1.1;AES256
          616462343733323934623365303733...
```

##### 3. **Mise à jour du fichier YAML**
Remplacez la valeur d'origine par la version chiffrée dans `vars.yml` :

```yaml
db_username: admin
db_password: !vault |
          $ANSIBLE_VAULT;1.1;AES256
          616462343733323934623365303733...
api_key: abc12345
```

##### 4. **Chiffrement de l’ensemble du fichier**
Si vous préférez protéger l’ensemble du fichier (au lieu d’une seule valeur), utilisez :

```bash
ansible-vault encrypt vars.yml
```

Une fois chiffré, le fichier entier sera illisible sans le mot de passe Vault :

```yaml
$ANSIBLE_VAULT;1.1;AES256
6262346165393166353961306662313539393361346532653739333161396332340a6535383434656361643138376664653738393331626233313137653736653332323838663064353732336365310a31356531633732306361353065323065646465346661633466303331633032303035383038333635356463303564636631313966633862333531
```

Pour afficher ou modifier ce fichier, utilisez respectivement les commandes :

- **Afficher :** `ansible-vault view vars.yml`
- **Modifier :** `ansible-vault edit vars.yml`

---

### **Fonctionnalités avancées : Libérez tout le potentiel d'Ansible Vault**

#### **1. Chiffrer uniquement certaines valeurs**
Vous pouvez chiffrer des portions spécifiques d’un fichier, au lieu de tout chiffrer. Par exemple :

```bash
ansible-vault encrypt_string 'mon_mot_de_passe' --name 'password'
```

Cela génère une section chiffrée que vous pouvez insérer dans un fichier YAML.

#### **2. Gérer plusieurs fichiers Vault avec Vault IDs**
Les projets complexes nécessitent souvent des secrets différents pour plusieurs environnements (développement, production, etc.). Ansible Vault permet de gérer plusieurs Vaults avec des identifiants distincts :

```bash
ansible-vault create --vault-id dev@prompt dev-secrets.yml
ansible-vault create --vault-id prod@prompt prod-secrets.yml
```

Lors de l’exécution :

```bash
ansible-playbook playbook.yml --vault-id dev@prompt --vault-id prod@prompt
```

#### **3. Changer le mot de passe d’un fichier Vault**
Pour renforcer la sécurité ou respecter une politique de rotation des mots de passe, utilisez :

```bash
ansible-vault rekey fichier.yaml
```

---

### **Automatisation et intégration dans les pipelines CI/CD**

Dans un environnement CI/CD, où les déploiements sont fréquents et automatisés, Ansible Vault s’intègre parfaitement. Vous pouvez utiliser un fichier contenant le mot de passe pour éviter les interactions manuelles :

1. Créez un fichier texte contenant le mot de passe (`vault_pass.txt`).
2. Limitez les permissions sur ce fichier :

```bash
chmod 600 vault_pass.txt
```

3. Exécutez le playbook avec :

```bash
ansible-playbook playbook.yml --vault-password-file vault_pass.txt
```

---

### **Conseils pratiques**

1. **Définir un éditeur préféré :** Par défaut, Ansible utilise **vi** pour éditer les fichiers Vault. Si vous préférez **nano**, définissez-le comme éditeur par défaut :

   ```bash
   export EDITOR=nano
   ```

2. **Vérifier si un fichier est chiffré :**

   ```bash
   ansible-vault is-encrypted fichier.yaml
   ```

3. **Comparer deux fichiers Vault :** Identifiez les différences entre deux fichiers chiffrés avec :

   ```bash
   ansible-vault diff fichier1.yaml fichier2.yaml
   ```

---

### **Conclusion**

Ansible Vault est un outil puissant pour sécuriser vos données sensibles dans des environnements DevOps modernes. Que vous gériez un simple serveur ou une infrastructure multi-environnements, Vault offre des solutions adaptées à vos besoins.

En intégrant ces pratiques dans vos projets Ansible, vous minimisez les risques de fuite et améliorez la sécurité de votre infrastructure.

---

Vous avez encore des secrets à sécuriser ? Essayez ces étapes dès aujourd'hui ! Si vous avez des questions ou souhaitez partager vos expériences, n'hésitez pas à commenter ! 😊