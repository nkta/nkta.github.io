# **Configurer Git Flow pour GitLab CI/CD avec gestion de `main` et des releases**

Git Flow est une convention de gestion de branches largement utilisée pour structurer le cycle de développement d’un projet. Cependant, lorsqu'on l’intègre avec **GitLab CI/CD**, plusieurs défis se posent, notamment la gestion du **nom de la branche principale** (`main` au lieu de `master`) et l'automatisation des releases.

Cet article explique comment **initialiser et configurer Git Flow** pour GitLab CI/CD tout en automatisant le processus de release de manière contrôlée.

---

## **1️⃣ Initialiser Git Flow avec `main` au lieu de `master`**

Par défaut, **Git Flow s’attend à une branche `master`**. Or, sur GitLab, la convention récente est d’utiliser `main`. Pour que Git Flow prenne en compte `main`, on doit l’indiquer explicitement.

### **🛠 Initialisation manuelle de Git Flow**
Dans votre dépôt local, exécutez :

```bash
git flow init
```

Lorsque Git Flow demande la **branche principale**, entrez : `main`.

Si vous voulez automatiser cela dans un script CI/CD :

```bash
git flow init -d
# Forcer l'utilisation de main au lieu de master
git config --local gitflow.branch.master main
git config --local gitflow.branch.develop develop
```

Ensuite, vérifiez la configuration avec :

```bash
git config --local --list | grep gitflow
```

Cela devrait afficher :

```ini
gitflow.branch.master=main
gitflow.branch.develop=develop
gitflow.prefix.feature=feature/
gitflow.prefix.release=release/
gitflow.prefix.hotfix=hotfix/
```

---

## **2️⃣ Configurer GitLab CI/CD avec Git Flow**

### **📌 Objectif du pipeline**
1. **Créer la release (`release start`) depuis `develop`**.
2. **Déployer la branche `release/*` en production (manuellement)**.
3. **Finaliser la release (`release finish`) après validation de la MEP**.

Voici un `.gitlab-ci.yml` adapté :

```yaml
stages:
  - setup
  - deploy
  - release_finish

setup_gitflow:
  stage: setup
  script:
    - git flow init -d
    - git config --local gitflow.branch.master main
    - git config --local gitflow.branch.develop develop
    - git config --local --list | grep gitflow
  only:
    - release/*

deploy:
  stage: deploy
  script:
    - echo "Déploiement manuel pour la release $CI_COMMIT_REF_NAME..."
    # Ajouter ici le script réel de déploiement
  only:
    - /^release\/.*/
  when: manual  # Déploiement déclenché manuellement

release_finish:
  stage: release_finish
  script:
    - echo "Finalisation manuelle de la release après validation en prod"
    - RELEASE_VERSION=$(echo $CI_COMMIT_REF_NAME | sed 's/release\///')
    - git flow release finish -m "Release $RELEASE_VERSION validée en prod" $RELEASE_VERSION
    - git push origin main
    - git push origin develop
    - git push --tags
  only:
    - /^release\/.*/
  when: manual  # Merge et tag déclenchés manuellement
```

### **💡 Explication du pipeline**
- **`setup_gitflow`** : Initialise Git Flow et s'assure que `main` est bien utilisé.
- **`deploy`** : Déploiement **manuel** de la release (pour valider avant merge).
- **`release_finish`** : Finalisation de la release **manuelle**, seulement si la MEP est validée.

Avec cette configuration, **le pipeline ne force pas la fusion dans `main` tant que le déploiement n’est pas validé**. Cela permet d'éviter d'introduire une release instable dans `main`.

---

## **3️⃣ Workflow Git Flow optimisé pour GitLab CI/CD**

Avec ce pipeline, voici comment gérer une release efficacement :

1. **Démarrer une nouvelle release** depuis `develop` :
   ```bash
   git flow release start 1.2.3
   git push origin release/1.2.3
   ```
   ➜ **Cela déclenche automatiquement le pipeline sur `release/1.2.3`.**

2. **Déployer `release/1.2.3` en prod (manuellement via GitLab CI/CD)**.

3. **Si la MEP casse, modifier `release/*` et redeployer** avant de finaliser.

4. **Finaliser la release (manuellement via GitLab CI/CD)** :
   ```bash
   git flow release finish 1.2.3
   git push origin main develop --tags
   ```
   ➜ **Le pipeline exécute `release_finish` et merge dans `main` et `develop`.**

---

## **✅ Avantages de cette approche**
✔️ **Git Flow fonctionne avec `main` sans souci**.  
✔️ **Automatisation des releases avec GitLab CI/CD**.  
✔️ **Contrôle manuel du déploiement pour éviter d’impacter `main` en cas de problème**.  
✔️ **Possibilité de modifier `release/*` et redéployer avant de finaliser**.  
✔️ **Facilité de rollback** : `main` ne change pas tant que la release n'est pas validée.

---

## **🎯 Conclusion**
En adaptant **Git Flow à GitLab CI/CD**, on assure un cycle de développement propre et sécurisé. L’approche avec **déploiement manuel et finalisation de release après validation** est idéale pour éviter d'impacter `main` trop tôt.

Avec ce guide, vous avez **un pipeline prêt à l'emploi** pour intégrer Git Flow avec GitLab CI/CD tout en garantissant la stabilité en production. 🚀

