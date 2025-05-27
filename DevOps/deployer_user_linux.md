# Comment déployer un utilisateur Linux et le configurer pour Ansible avec une connexion SSH par clé

Dans ce billet, nous verrons comment répliquer un utilisateur d'un serveur Linux vers un autre, en assurant que la connexion SSH fonctionne avec une clé publique/privée, et que cet utilisateur puisse être utilisé dans un playbook Ansible.

## 1. Récupérer les informations de l'utilisateur source

Sur le serveur source (ex. `server-source`) :

```bash
id deploy-user
getent passwd deploy-user
getent shadow deploy-user  # (si root)
getent group | grep deploy-user
```

Notez :

* UID / GID
* Shell
* Home directory
* Groupes secondaires (ex: `sudo`)
* Hash du mot de passe (pour l'importer sans demander à l'utilisateur de le réinitialiser)

## 2. Créer l'utilisateur sur le serveur cible

Sur le serveur de destination (ex. `server-target`) :

```bash
sudo groupadd -g 1006 deploy-user
sudo useradd \
  -u 1005 \
  -g 1006 \
  -G sudo \
  -s /bin/bash \
  -d /home/deploy-user \
  -m \
  deploy-user

# Ajouter le mot de passe hashé (si souhaité)
sudo usermod --password '$y$j9T$...$...' deploy-user
```

## 3. Copier le dossier .ssh de l'utilisateur

Depuis le serveur source :

```bash
rsync -avz /home/deploy-user/.ssh/ deploy-user@server-target:/tmp/.ssh/
```

Sur le serveur cible :

```bash
sudo mv /tmp/.ssh /home/deploy-user/.ssh
sudo chown -R deploy-user:deploy-user /home/deploy-user/.ssh
sudo chmod 700 /home/deploy-user/.ssh
sudo chmod 600 /home/deploy-user/.ssh/authorized_keys
```

## 4. Configuration sudo sans mot de passe (optionnel mais recommandé pour Ansible)

Éditez le fichier sudoers :

```bash
sudo visudo
```

Ajoutez :

```bash
deploy-user ALL=(ALL) NOPASSWD: ALL
```

## 5. Tester la connexion SSH

Depuis votre machine :

```bash
ssh -i ~/.ssh/id_ed25519 deploy-user@server-target
```

## 6. Utilisation dans un playbook Ansible

### Exemple de `inventory.ini`

```ini
[serveurs]
server-target ansible_user=deploy-user ansible_ssh_private_key_file=~/.ssh/id_ed25519 ansible_become=true
```

### Exemple de playbook

```yaml
- name: Déploiement test
  hosts: serveurs
  become: true
  tasks:
    - name: Affiche l'utilisateur courant
      command: whoami
```

### Exécution du playbook

* Si sudo ne demande pas de mot de passe :

```bash
ansible-playbook playbook.yml -i inventory.ini
```

* Si sudo demande un mot de passe :

```bash
ansible-playbook playbook.yml -i inventory.ini --ask-become-pass
```

## Conclusion

Ce guide permet de créer un utilisateur distant complet, fonctionnel pour des connexions SSH sans mot de passe et des automatisations Ansible. C'est idéal pour la gestion des serveurs dans une infrastructure DevOps.
