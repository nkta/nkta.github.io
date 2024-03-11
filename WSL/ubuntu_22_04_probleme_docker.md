 Titre: Résolution du problème de version iptables dans Ubuntu 22.04 en utilisant iptables-legacy

Introduction:
Lors de l'utilisation d'Ubuntu 22.04, vous pouvez rencontrer des problèmes liés à la version iptables qui peuvent empêcher certaines applications, telles que Docker, de fonctionner correctement. Ce guide explique comment basculer vers la version iptables-legacy pour résoudre ce problème.

Problème:
Parfois, lorsque vous utilisez Ubuntu 22.04 et essayez de vérifier l'état d'iptables, il peut sembler inactif ou non opérationnel. Cela est souvent dû au fait que la dernière version d'iptables n'est pas entièrement compatible avec certains services tels que Docker. Pour corriger ce problème, nous allons changer la version iptables par défaut en utilisant iptables-legacy.

Solution:
1. Ouvrir une fenêtre terminal et saisissez la commande suivante pour afficher les options disponibles pour iptables:

```
sudo update-alternatives --config iptables
```

2. Vous verrez une liste similaire à celle-ci:

```
Il existe 3 choix pour l'alternative iptables (qui fournit /usr/sbin/iptables).

  Sélection   Chemin               Priorité  État
-----------------------------------------------
* 0            /usr/sbin/iptables-nft   35        mode automatique
  1            /usr/sbin/iptables-legacy 10        mode manuel
  2            /usr/sbin/iptables-nft   35        mode manuel
  3            /usr/sbin/iptables-xtables 10        mode manuel

Appuyez sur <ENTRÉE> pour conserver la valeur actuelle[0], ou tapez le numéro sélectionné :
```

3. Choisissez "1" pour sélectionner `/usr/sbin/iptables-legacy`, puis appuyez sur Entrée.

4. Redémarrer maintenant le service Docker en tapant la commande suivante:

```
sudo service docker start
```

5. Enfin, vérifiez l'état actuel du service Docker en tapant:

```
sudo service docker status
```

Votre sortie doit indiquer que Docker est actif et prêt à être utilisé sans aucun message concernant iptables. Le passage à iptables-legacy devrait permettre aux utilisateurs d'éviter tout problème potentiel associé à la nouvelle version d'iptables.

Conclusion:
En suivant ces étapes, vous avez pu résoudre les problèmes causés par la mauvaise compatibilité entre la dernière version d'iptables et Docker sous Ubuntu 22.04. Si vous suivez régulièrement les versions logicielles récentes, gardez un œil attentif sur les futures corrections officielles apportées à iptables afin de revenir éventuellement à la toute dernière version si elle devient plus stable et mieux adaptée à votre environnement système.
