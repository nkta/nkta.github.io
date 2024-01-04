### Configuration Automatique de Docker avec WSL

**Objectif** : Faire démarrer Docker automatiquement lors de l'ouverture d'une session WSL.

**Étapes à suivre** :

1. **Modifier le fichier `.bashrc` ou `.zshrc`** :
   - Ouvrir avec `nano ~/.bashrc` ou `nano ~/.zshrc`.
   - Ajouter à la fin :
     ```bash
     if ! pgrep -x "dockerd" > /dev/null; then
         echo "Démarrage de Docker..."
         sudo service docker start
     fi
     ```
   - Cela vérifie si Docker est déjà en cours d'exécution et le démarre si nécessaire.

2. **Gestion des permissions sudo** :
   - Pour éviter de saisir le mot de passe sudo à chaque fois, modifier le fichier sudoers :
     - Exécuter `sudo visudo`.
     - Ajouter la ligne :
       ```
       votre_nom_utilisateur ALL=(ALL) NOPASSWD: /usr/sbin/service docker start
       ```
     - Remplacer `votre_nom_utilisateur` par votre nom d'utilisateur WSL.

3. **Recharger la configuration** :
   - Exécuter `source ~/.bashrc` ou `source ~/.zshrc`.

4. **Redémarrer WSL** :
   - Fermer et rouvrir le terminal WSL ou exécuter `wsl --shutdown` dans CMD/PowerShell de Windows, puis relancer WSL.

**Points Clés** :
- Vérifier que Docker est correctement installé dans WSL.
- S'assurer que le service Docker peut démarrer manuellement avec succès.
- Cette méthode permet de démarrer Docker automatiquement sans interaction manuelle à chaque lancement de WSL. 