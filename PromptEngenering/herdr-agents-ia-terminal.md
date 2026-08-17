# Rédiger du code et piloter des agents IA sans quitter son terminal : à la découverte de Herdr

Le développement assisté par IA a profondément transformé notre manière de coder. Entre les IDE lourds, les extensions propriétaires et les interfaces web qui coupent du flux de travail, trouver le juste équilibre relève parfois du parcours du combattant. Et si la solution tenait dans un simple terminal ?

C'est tout l'objet d'**Herdr**, un outil en ligne de commande conçu pour héberger, orchestrer et interagir directement avec des agents IA au cœur de son environnement de travail habituel.

---

## Pourquoi intégrer ses agents IA dans un terminal ?

En tant que développeur, quitter sa console pour lancer une requête ou surveiller un agent casse le rythme. Centraliser ces processus dans un terminal apporte plusieurs avantages évidents :

* **Zéro rupture de contexte :** tout se passe là où se trouvent déjà les outils de build, les logs et le gestionnaire de versions.
* **Légèreté et rapidité :** pas de lourdeur d'interface graphique, l'affichage est immédiat.
* **Maîtrise totale de l'environnement :** l'outil s'exécute localement ou sur une machine distante, s'intègre aux scripts et s'automatise facilement.

---

## Installation et accès au projet

Le projet est hébergé en open source sur GitHub :

* **Dépôt officiel :** `[https://github.com/herdr-ai/herdr](https://github.com/herdr-ai/herdr)` *(ou `[https://github.com/](https://github.com/)<orga>/herdr` selon le dépôt cible)*

### Méthodes d'installation

Selon ton environnement (Linux natif ou WSL2), plusieurs options sont généralement disponibles :

1. **Via le gestionnaire de paquets (recommandé si binaire dispo) :**
```bash
# Si distribué via npm / npx
npm install -g herdr

# Ou via Cargo (Rust) si compilé à la source
cargo install herdr

```


2. **Depuis les sources (Git) :**
```bash
git clone https://github.com/herdr-ai/herdr.git
cd herdr
# Lancer l'installation / build local selon le runtime (Node/Rust/Go)

```



---

## Comment ça fonctionne sous le capot ?

Contrairement aux idées reçues, faire tourner ce type d'outil en arrière-plan ne nécessite pas forcément une artillerie lourde comme `systemd`.

Sous Linux ou via **WSL2** (Windows Subsystem for Linux), Herdr et ses équivalents s'appuient sur des mécanismes standards :

* Des **pseudo-terminaux (PTY)** et des multiplexeurs pour détacher les processus.
* Une architecture où un démon gère les flux d'exécution pendant que l'interface s'y connecte.

Pour ceux qui souhaitent industrialiser le déploiement sur un serveur ou un poste de travail fixe, l'utilisation de `systemd` dans WSL2 permet un démarrage automatique au boot et un suivi centralisé via les logs du système.

---

## Quelques astuces pour l'intégrer proprement sous WSL2

Si tu utilises WSL2 au quotidien, quelques réglages s'imposent pour éviter que tes agents ne se coupent dès la fermeture de ta fenêtre de commande :

1. **Garder l'instance active :** édite ton fichier global `C:\Users\<Ton_Nom>\.wslconfig` sous Windows pour y ajouter le paramètre suivant afin d'empêcher l'arrêt automatique de la machine virtuelle :
```ini
[wsl2]
vmIdleTimeout=-1

```


2. **Activer `systemd` :** si tu souhaites piloter ton agent via des services propres, assure-toi d'activer systemd dans `/etc/wsl.conf` :
```ini
[boot]
systemd=true

```


Pense ensuite à appliquer les changements avec un `wsl --shutdown` depuis PowerShell.

---

## En résumé

Herdr s'inscrit dans cette volonté de reprendre le contrôle sur ses outils de développement. En combinant la puissance des agents IA et la souplesse d'un terminal sous Linux ou WSL, il devient possible de déléguer des tâches complexes tout en gardant un œil sur le code, sans friction superflue.