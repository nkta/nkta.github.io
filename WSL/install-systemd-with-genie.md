---
layout: page
title: "Installation de Systemd dans WSL 2 avec Genie"
---

# Installation de Systemd dans WSL 2 avec Genie

L’installation de systemd dans Windows Subsystem for Linux (WSL 2) n’est pas une tâche triviale, car WSL 2 ne prend pas en charge systemd par défaut. Cependant, en utilisant un outil tiers appelé Genie, vous pouvez configurer et utiliser systemd dans WSL 2. Cet article vous guide à travers les étapes nécessaires pour installer et configurer systemd dans WSL 2.

## Pré-requis

Avant de commencer, assurez-vous que vous avez :

- WSL 2 installé et configuré sur votre machine Windows.
- Une distribution Linux (Ubuntu) installée dans WSL 2.
- Des privilèges sudo pour installer des packages et modifier les configurations.

## Étape 1 : Préparer l’environnement

Commencez par mettre à jour les paquets de votre distribution Ubuntu :

```bash
sudo apt update
sudo apt upgrade -y
```

Ensuite, installez les dépendances nécessaires pour Genie :

```bash
sudo apt install -y daemonize dbus-bin libc6 systemd-sysv
```

## Étape 2 : Installer Genie

Le package Genie n'est pas disponible dans les dépôts standards, nous allons donc le télécharger directement depuis GitHub.

1. Accédez à la page des [releases de Genie sur GitHub](https://github.com/arkane-systems/genie/releases) et téléchargez les fichiers `.deb` nécessaires pour votre architecture (`amd64`).

2. Installez les fichiers téléchargés en utilisant `dpkg` :

```bash
sudo dpkg -i systemd-genie_<version>_amd64.deb
```

Remplacez `<version>` par la version spécifique que vous avez téléchargée.

## Étape 3 : Configuration de Genie

Pour que Genie fonctionne correctement, nous devons le configurer pour utiliser `multi-user.target` comme cible par défaut. Ouvrez le fichier de configuration de Genie :

```bash
sudo nano /etc/genie.ini
```

Modifiez la ligne de `target` pour qu'elle corresponde à :

```ini
target = multi-user.target
```

Enregistrez le fichier et quittez l’éditeur (Ctrl+O puis Ctrl+X pour nano).

## Étape 4 : Configurer le script de démarrage

Ajoutez les lignes suivantes à votre fichier `~/.bashrc` pour démarrer Genie automatiquement à l’ouverture de votre session WSL :

```bash
if [ -z "$INSIDE_GENIE" ]; then
    exec /usr/bin/genie -s
fi
```

Enregistrez et fermez le fichier.

## Étape 5 : Redémarrer WSL

Pour appliquer toutes les modifications, redémarrez WSL :

```powershell
wsl --shutdown
```

## Étape 6 : Vérification

Vérifiez que `systemd` est actif en listant les unités :

```bash
systemctl --user list-units
```

Si `systemd` est en état dégradé, vous pouvez examiner les journaux pour identifier et résoudre les problèmes :

```bash
journalctl -u systemd-sysusers.service
```

## Conclusion

Avec ces étapes, vous devriez avoir `systemd` fonctionnel dans votre environnement WSL 2 en utilisant Genie. Cette configuration vous permet de tirer parti des services gérés par `systemd`, ce qui peut être particulièrement utile pour le développement et les tests dans un environnement WSL.

N’oubliez pas de consulter la [documentation de Genie](https://github.com/arkane-systems/genie) pour des informations supplémentaires et des solutions aux problèmes courants. Profitez de votre nouvelle configuration systemd dans WSL 2 !