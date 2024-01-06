---
layout: page
title: "Windows 11 : Installer le sous-système Linux sans le Microsoft Store"
---

# Windows 11 : Installer le sous-système Linux sans le Microsoft Store
10 décembre 2021 - Andy, Logiciels

[Article original](https://ekiwi-blog.de/en/17814/windows-11-install-linux-subsystem-without-microsoft-store/?source=post_page-----f85571c1b819)

*Installer le sous-système Linux dans Windows 11 sans passer par le Microsoft Store.*

La façon la plus simple d'installer un Linux, comme Ubuntu, dans Windows 11 est via le Windows Store. Cependant, dans les entreprises, le store est souvent bloqué. Mais vous pouvez installer manuellement le sous-système Linux pour Windows. Ces instructions fonctionnent également pour Windows 10.

## Table des matières
- Instructions
- Téléchargement et installation

## Instructions
Dans les paramètres, allez dans Applications et ouvrez les "Fonctionnalités optionnelles".

Faites défiler jusqu'en bas et cliquez sur "Plus de fonctionnalités Windows".

Nous devons installer deux choses ici : la "Plateforme Hyper-V" et le "Sous-système Windows pour Linux". Les utilisateurs de Windows 10 n'ont pas besoin de la partie Hyper-V.

Windows configure les fonctionnalités et nécessite un redémarrage.

## Téléchargement et installation
Une fois de retour dans Windows, nous pouvons maintenant télécharger le système Linux que nous souhaitons utiliser. Puisque nous ne pouvons pas télécharger Linux depuis le store, voici quelques liens directs.

- [Ubuntu 20.04](https://aka.ms/wslubuntu2004)
- [Ubuntu 18.04](https://aka.ms/wsl-ubuntu-1804)
- [openSUSE Lead 15.2](https://aka.ms/wsl-opensuseleap15-2)
- [Debian](https://aka.ms/wsl-debian-gnulinux)

Le package que nous avons téléchargé est un package .appx. Ne démarrez pas le package. Au lieu de cela, nous devons extraire l'archive. [7-Zip](https://www.7-zip.org/download.html) est bien adapté pour cela.

Après avoir extrait le package, nous pouvons maintenant commencer l'installation de Linux. Au moins les utilisateurs de Windows 10 le peuvent.

Les utilisateurs de Windows 11 rencontreront probablement un message d'erreur, indiquant que WSL2 nécessite une mise à jour.

```
Installing, this may take a few minutes...
WslRegisterDistribution failed with error: 0x800701bc
Error: 0x800701bc WSL2 requires an update to ist kernel component.
```

Nous pouvons télécharger la mise à jour [ici](https://learn.microsoft.com/fr-fr/windows/wsl/install-manual#step-4---download-the-linux-kernel-update-package).

Exécutez l'installateur de la mise à jour.

Après avoir terminé la mise à jour, nous pouvons relancer l'installation de Linux. Dans la plupart des cas, cela devrait maintenant fonctionner. Si vous recevez l'erreur suivante :

Installation, cela peut prendre quelques minutes…
WslRegisterDistribution a échoué avec l'erreur : 0x80370102
Vérifiez si vous avez installé Hyper-V et activé la virtualisation dans le BIOS/UEFI de votre ordinateur.

L'installation de Linux se déroule maintenant et après un certain temps, vous pouvez définir un nom d'utilisateur et un mot de passe. Maintenant, vous avez installé Linux pour Windows.
