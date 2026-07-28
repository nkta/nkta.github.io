# OpenRewrite : automatiser la migration et la modernisation de votre code Java

Refactoriser un projet Java à grande échelle est rarement une partie de plaisir. Monter de version Spring Boot, migrer de JUnit 4 à JUnit 5, remplacer une API dépréciée dans des dizaines de modules... ce sont des tâches répétitives, chronophages, et sources d'erreurs quand elles sont faites à la main. C'est exactement le problème que résout **OpenRewrite**.

## Qu'est-ce qu'OpenRewrite ?

OpenRewrite est un outil open source de **refactoring automatisé** pour du code source (principalement Java, mais aussi Kotlin, YAML, XML, propriétés, etc.). Contrairement à un simple `sed` ou une recherche-remplace basée sur du texte, OpenRewrite travaille sur un **arbre syntaxique abstrait (AST)** enrichi d'informations sémantiques (types, imports, structure). Il comprend donc réellement votre code, ce qui permet des transformations fiables et sans effet de bord.

Concrètement, OpenRewrite s'articule autour de trois notions clés :

- **LST (Lossless Semantic Tree)** : une représentation du code qui conserve tout, y compris la mise en forme, les commentaires et les espaces, pour ne rien casser lors de la réécriture.
- **Recipes (recettes)** : des unités de transformation réutilisables (ex. "migrer vers Java 17", "remplacer `@RequestMapping` par `@GetMapping`").
- **Visitors** : le mécanisme interne qui parcourt le LST pour appliquer les modifications définies par une recette.

## Pourquoi l'utiliser ?

- **Migrations de version** : Java 8 → 17/21, Spring Boot 2 → 3, Spring Framework, JUnit 4 → 5, etc. Des recettes officielles existent déjà pour la plupart des montées de version majeures.
- **Mise en conformité de style/conventions** : imposer des règles d'équipe (nommage, organisation des imports, usage d'API interne) de façon automatisée plutôt que via des revues de code répétitives.
- **Dette technique** : supprimer des usages dépréciés, remplacer des bibliothèques, nettoyer du code mort.
- **Reproductibilité** : les recettes sont versionnées et applicables sur l'ensemble d'un mono-repo ou d'un parc de microservices en une seule commande.

## Mise en place avec Maven

Le moyen le plus simple de démarrer est le plugin Maven :

```xml
<plugin>
  <groupId>org.openrewrite.maven</groupId>
  <artifactId>rewrite-maven-plugin</artifactId>
  <version>5.46.0</version>
  <configuration>
    <activeRecipes>
      <recipe>org.openrewrite.java.spring.boot3.UpgradeSpringBoot_3_2</recipe>
    </activeRecipes>
  </configuration>
  <dependencies>
    <dependency>
      <groupId>org.openrewrite.recipe</groupId>
      <artifactId>rewrite-spring</artifactId>
      <version>5.19.0</version>
    </dependency>
  </dependencies>
</plugin>
```

Puis on lance :

```bash
# Voir le diff sans rien appliquer
mvn rewrite:dryRun

# Appliquer réellement les changements
mvn rewrite:run
```

`dryRun` génère un rapport (`target/rewrite/rewrite.patch`) que vous pouvez relire avant de committer — un vrai filet de sécurité pour ne pas se faire surprendre.

## Mise en place avec Gradle

```groovy
plugins {
    id("org.openrewrite.rewrite") version "6.9.0"
}

rewrite {
    activeRecipe("org.openrewrite.java.testing.junit5.JUnit4to5Migration")
}

dependencies {
    rewrite("org.openrewrite.recipe:rewrite-testing-frameworks:2.13.0")
}
```

```bash
./gradlew rewriteDryRun
./gradlew rewriteRun
```

## Un exemple concret : migrer de JUnit 4 à JUnit 5

Avant :

```java
import org.junit.Test;
import static org.junit.Assert.assertEquals;

public class CalculatorTest {
    @Test
    public void testAdd() {
        assertEquals(4, Calculator.add(2, 2));
    }
}
```

Après application de la recette `org.openrewrite.java.testing.junit5.JUnit4to5Migration` :

```java
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.assertEquals;

public class CalculatorTest {
    @Test
    void testAdd() {
        assertEquals(4, Calculator.add(2, 2));
    }
}
```

Les imports sont réécrits, les annotations mises à jour, et les signatures ajustées (suppression du `public` inutile sur les méthodes de test) — automatiquement, sur l'ensemble du projet.

## Écrire sa propre recette

Pour des besoins spécifiques à votre codebase, deux approches existent :

**1. Recette déclarative (YAML)**, idéale pour combiner des recettes existantes :

```yaml
type: specs.openrewrite.org/v1beta/recipe
name: com.exemple.NettoyageInterne
displayName: Nettoyage des conventions internes
recipeList:
  - org.openrewrite.java.RemoveUnusedImports
  - org.openrewrite.java.OrderImports
  - org.openrewrite.java.format.AutoFormat
```

**2. Recette impérative (Java)**, pour des transformations plus complexes basées sur un `TreeVisitor` :

```java
public class RenameMethod extends Recipe {
    @Override
    public String getDisplayName() {
        return "Renomme uneMethode() en maNouvelleMethode()";
    }

    @Override
    public TreeVisitor<?, ExecutionContext> getVisitor() {
        return new JavaIsoVisitor<ExecutionContext>() {
            @Override
            public J.MethodDeclaration visitMethodDeclaration(J.MethodDeclaration method, ExecutionContext ctx) {
                if (method.getSimpleName().equals("uneMethode")) {
                    return method.withName(method.getName().withSimpleName("maNouvelleMethode"));
                }
                return super.visitMethodDeclaration(method, ctx);
            }
        };
    }
}
```

## Intégration en CI/CD

Un usage courant consiste à lancer `rewrite:dryRun` dans une pipeline (par exemple GitLab CI) pour détecter les dérives par rapport aux conventions, ou à programmer un job périodique qui ouvre automatiquement une merge request avec `rewrite:run` appliqué et le diff en pièce jointe. Cela évite d'avoir à faire ces migrations "à la main" sur chaque microservice d'un parc applicatif.

## Bonnes pratiques

- Toujours commencer par `dryRun` et relire le patch généré.
- Appliquer les recettes une par une sur un projet pilote avant de les déployer sur tout un mono-repo.
- Versionner ses recettes personnalisées dans un module dédié, réutilisable d'un projet à l'autre.
- Combiner OpenRewrite avec les tests existants : le refactoring automatisé ne dispense pas de faire tourner la suite de tests après application.

## Pour aller plus loin

Le catalogue officiel de recettes est disponible sur [docs.openrewrite.org](https://docs.openrewrite.org/recipes), avec des packs prêts à l'emploi pour Spring, Micronaut, Quarkus, la sécurité (détection de CVE), ou encore la migration vers les dernières versions de Java.

OpenRewrite ne remplace pas la réflexion humaine sur l'architecture d'un projet, mais il élimine une grande partie du travail mécanique et répétitif des migrations — ce qui laisse plus de temps pour ce qui compte vraiment.
