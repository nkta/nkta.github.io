

**Titre : Personnaliser la Gestion DNS dans WSL : Empêcher la Réinitialisation de `/etc/resolv.conf`**

---

**Introduction**

Dans cet article, nous abordons un défi courant pour les utilisateurs de WSL (Windows Subsystem for Linux) : la réinitialisation automatique du fichier `/etc/resolv.conf`. Nous vous guidons pas à pas pour empêcher cette réinitialisation et maintenir vos paramètres DNS personnalisés, même après un redémarrage de WSL.

---

**Étape 1 : Comprendre `/etc/resolv.conf`**

Sous Linux, `/etc/resolv.conf` est essentiel pour définir les serveurs DNS. Dans WSL, ce fichier est souvent réinitialisé automatiquement, ce qui peut poser problème si vous avez besoin de configurations DNS spécifiques.

---

**Étape 2 : Désactiver la Génération Automatique de `/etc/resolv.conf`**

Suivez ces étapes pour empêcher WSL de réinitialiser `/etc/resolv.conf` :

1. Ouvrez un terminal WSL.
2. Exécutez `sudo nano /etc/wsl.conf`.
3. Ajoutez ces lignes au fichier :

   ```
   [network]
   generateResolvConf = false
   ```

4. Enregistrez et quittez l'éditeur.

---

**Étape 3 : Redémarrer WSL**

Après avoir changé `wsl.conf`, redémarrez WSL avec `wsl --shutdown` dans l'invite de commande Windows, puis relancez WSL.

---

**Étape 4 : Que Faire Si `/etc/resolv.conf` est Supprimé au Redémarrage**

Dans certains cas, malgré ces changements, `/etc/resolv.conf` peut être supprimé au redémarrage de WSL. Voici comment y remédier :

1. Après le redémarrage de WSL, créez manuellement le fichier `/etc/resolv.conf` si nécessaire.
2. Utilisez un script de démarrage pour vérifier la présence du fichier et le créer si absent. Par exemple, ajoutez ceci à votre `.bashrc` :

   ```bash
   if [ ! -f /etc/resolv.conf ]; then
       echo "Création de /etc/resolv.conf"
       echo "nameserver 8.8.8.8" | sudo tee /etc/resolv.conf > /dev/null
       echo "nameserver 8.8.4.4" | sudo tee -a /etc/resolv.conf > /dev/null
       sudo chmod 444 /etc/resolv.conf
   fi
   ```

3. Pour éviter de saisir le mot de passe sudo à chaque démarrage, ajustez les permissions sudo via `sudo visudo` avec :

   ```
   yourusername ALL=(ALL) NOPASSWD: /bin/tee /etc/resolv.conf, /bin/tee -a /etc/resolv.conf, /bin/chmod 444 /etc/resolv.conf
   ```

---

**Conclusion**

Cette approche garantit que vos paramètres DNS personnalisés dans WSL restent intacts, même après un redémarrage. Elle est particulièrement utile pour les environnements de développement et de test où la cohérence de la configuration réseau est essentielle.

---

**Note de sécurité :** Comme toujours, manipuler les configurations de réseau et de sudo comporte des risques. Assurez-vous de comprendre les implications et demandez de l'aide à un professionnel si nécessaire.
