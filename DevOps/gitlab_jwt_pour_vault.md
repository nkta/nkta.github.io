# Sécuriser vos Déploiements CI/CD avec Vault et les ID Tokens de GitLab

Dans un environnement DevOps moderne, la gestion des secrets est cruciale pour assurer la sécurité des déploiements. Dans cet article, nous verrons comment utiliser HashiCorp Vault en combinaison avec GitLab CI/CD pour sécuriser l'accès aux secrets à l'aide des ID tokens. Nous aborderons la configuration de GitLab pour générer des tokens d'identité, la mise en place des rôles et policies dans Vault, ainsi que l'intégration de cette solution dans vos pipelines.

---

## 1. Pourquoi utiliser Vault avec GitLab CI/CD ?

Les pipelines CI/CD nécessitent l'accès à divers secrets (clés API, certificats, mots de passe, etc.) pour déployer des applications en toute sécurité. Utiliser Vault permet de centraliser la gestion de ces secrets et de contrôler finement qui a accès à quoi. En intégrant Vault avec GitLab, vous bénéficiez notamment :

- **D'une authentification sécurisée** : grâce aux ID tokens conformes à OpenID Connect.
- **D'une gestion centralisée** : chaque projet peut se voir attribuer des droits spécifiques en fonction des claims présents dans le token.
- **D'une flexibilité** : en configurant des rôles et des policies dans Vault, vous orientez les accès aux bons secrets selon l'origine des requêtes.

---

## 2. Comprendre les ID Tokens dans GitLab CI/CD

### Qu'est-ce qu'un ID token ?

Les ID tokens sont des JSON Web Tokens (JWT) générés automatiquement par GitLab pour chaque job CI/CD configuré avec la directive `id_tokens`. Ils contiennent des informations standards telles que :

- **iss** (*Issuer*) : L'émetteur du token, généralement l'URL de votre instance GitLab.
- **sub** (*Subject*) : Le sujet du token, qui correspond souvent au chemin complet du projet (par exemple, `"datahub/hr-data-api"`).
- **aud** (*Audience*) : La cible pour laquelle le token est émis (par exemple, l'URL de votre instance Vault).
- **iat** et **exp** : La date d'émission et l'expiration du token.

### Configuration dans le `.gitlab-ci.yml`

Pour générer un ID token et l'injecter dans votre job, modifiez votre fichier `.gitlab-ci.yml` comme suit :

```yaml
affiche_id_token:
  stage: test
  image: alpine:latest
  id_tokens:
    VAULT_ID_TOKEN:
      aud: "https://vault.hop.fr"
  script:
    - echo "L'ID token est : $VAULT_ID_TOKEN"
```

Dans cet exemple, GitLab génère un ID token destiné à l’audience `https://vault.hop.fr` et le stocke dans la variable d’environnement `VAULT_ID_TOKEN`.

---

## 3. Configurer Vault pour accepter les ID Tokens

Pour que Vault puisse authentifier correctement un job GitLab à l'aide d'un ID token, il faut configurer la méthode d'authentification JWT dans Vault et créer des rôles spécifiques.

### a) Configuration globale de Vault

Activez et configurez le backend JWT dans Vault pour qu’il récupère les clés publiques (JWKS) de GitLab :

```bash
vault auth enable jwt

vault write auth/jwt/config \
    issuer="https://gitlab.hop.fr" \
    jwks_url="https://gitlab.hop.fr/oauth/discovery/keys"
```

Cette configuration indique à Vault que les tokens doivent être émis par GitLab et que la vérification des signatures se fera via l’URL JWKS.

### b) Création d’un rôle pour un dépôt spécifique

Pour restreindre l’accès aux secrets d’un dépôt particulier, vous pouvez créer un rôle dans Vault qui valide le claim `sub` du token. Par exemple, pour le dépôt `datahub/hr-data-api` :

```bash
vault write auth/jwt/role/gitlab-hr-data-api-access \
    role_type="jwt" \
    bound_audiences="https://vault.hop.fr" \
    bound_claims.sub="datahub/hr-data-api" \
    user_claim="sub" \
    policies="rct-drh-hr-data-api" \
    ttl="1h"
```

Ici, Vault vérifiera que le token possède :

- Un audience (`aud`) correspondant à `https://vault.hop.fr`.
- Un claim `sub` égal à `datahub/hr-data-api`.

Si ces conditions sont remplies, le token se verra attribuer la policy `rct-drh-hr-data-api` qui définit les accès aux secrets.

---

## 4. Gérer plusieurs dépôts : Stratégies et bonnes pratiques

Si vous avez plusieurs dépôts GitLab, plusieurs approches s’offrent à vous.

### 4.1. Rôles et policies dédiés pour chaque dépôt

Pour chaque dépôt, vous pouvez créer un rôle distinct dans Vault. Par exemple :

- **Pour ****`datahub/hr-data-api`** :

  ```bash
  vault write auth/jwt/role/gitlab-hr-data-api-access \
      role_type="jwt" \
      bound_audiences="https://vault.hop.fr" \
      bound_claims.sub="datahub/hr-data-api" \
      user_claim="sub" \
      policies="rct-drh-hr-data-api" \
      ttl="1h"
  ```

- **Pour ****`datahub/autre-projet`** :

  ```bash
  vault write auth/jwt/role/gitlab-autre-projet-access \
      role_type="jwt" \
      bound_audiences="https://vault.hop.fr" \
      bound_claims.sub="datahub/autre-projet" \
      user_claim="sub" \
      policies="rct-drh-autre-projet" \
      ttl="1h"
  ```

Chaque rôle vérifie le claim `sub` du token pour déterminer le dépôt concerné et applique la policy adéquate.

### 4.2. Politiques dynamiques avec templates

Si vous préférez éviter de multiplier les rôles et policies, vous pouvez utiliser des politiques dynamiques qui se basent sur des templates. Par exemple, en configurant une policy qui intègre le claim `sub` dans le chemin d’accès aux secrets :

```hcl
path "secret/data/gitlab/{{identity.entity.metadata.sub}}/*" {
  capabilities = ["read", "list"]
}
```

Avec cette configuration, Vault attribuera automatiquement les droits d’accès aux secrets basés sur le chemin qui contient le claim `sub`. Pour que cela fonctionne, il faut que l’identité Vault soit mappée correctement aux claims du token.

### 4.3. Accès global à tous les dépôts

Si vous désirez autoriser un ID token à accéder à l’ensemble des dépôts, vous pouvez créer un rôle unique dans Vault qui valide un claim `sub` plus générique. Par exemple :

```bash
vault write auth/jwt/role/gitlab-global-access \
    role_type="jwt" \
    bound_audiences="https://vault.hop.fr" \
    bound_claims.sub=".*" \
    user_claim="sub" \
    policies="rct-drh-global" \
    ttl="1h"
```

- `bound_claims.sub=".*"` autorise tous les tokens dont le `sub` correspond à n’importe quel projet GitLab.
- La policy `rct-drh-global` (à adapter selon votre nomenclature) définit l’ensemble des permissions nécessaires pour accéder aux secrets de tous les projets.

> **Attention** : cette configuration est très permissive, car elle donne accès à l’ensemble des secrets définis par la policy associée. Il est donc essentiel de bien définir cette policy, et de la réserver éventuellement à un usage spécifique (par exemple, un dépôt de configuration « infrastructure » ou des scripts d’automatisation globaux).

---

## 5. Tester l’intégration

Une fois la configuration en place, il est essentiel de tester le flux complet :

1. **Génération de l’ID token dans GitLab**\
   Configurez un job pour afficher ou utiliser le token généré.

2. **Authentification auprès de Vault**\
   Utilisez la commande suivante pour tester la connexion :

   ```bash
   vault login -method=jwt role=gitlab-hr-data-api-access jwt=$VAULT_ID_TOKEN
   ```

3. **Vérification des accès**\
   Assurez-vous que le token se voit attribuer un token Vault avec la policy adéquate et que l’accès aux secrets est restreint selon vos besoins.

---

## Conclusion

L’intégration de GitLab CI/CD et Vault via les ID tokens offre une solution robuste pour sécuriser vos déploiements. En générant automatiquement un token d’identité par job, GitLab simplifie l’authentification auprès de Vault, tandis que la configuration fine des rôles et policies dans Vault garantit que chaque dépôt n’accède qu’aux secrets qui lui sont destinés.

En adoptant cette approche, vous améliorez non seulement la sécurité de vos pipelines, mais vous bénéficiez également d’une gestion centralisée et flexible des secrets pour l’ensemble de vos projets.

N’hésitez pas à adapter ces configurations à votre environnement et à consulter la documentation officielle de GitLab et HashiCorp Vault pour plus de détails et d’exemples pratiques.