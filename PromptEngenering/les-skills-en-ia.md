# Les *skills* en IA : arrêter d'expliquer la même chose à chaque conversation

Il y a un moment que tout le monde ayant travaillé sérieusement avec un agent IA a vécu. Vous ouvrez une conversation, vous redonnez le contexte : « on est sur du Spring Boot, les DTO sont dans `api/dto`, les migrations passent par Liquibase, et surtout n'oublie pas d'ajouter le test d'intégration ». L'agent fait du bon travail. Le lendemain, nouvelle conversation, tout est à réexpliquer.

C'est exactement le problème que les **skills** viennent résoudre. Et le concept est bien plus simple qu'il n'y paraît.

## Un skill, c'est un dossier

Pas un modèle réentraîné, pas un plugin compilé, pas une API à héberger. Un skill est un **dossier contenant un fichier `SKILL.md`** — du Markdown avec un en-tête YAML — et, optionnellement, des fichiers de référence, des scripts et des ressources.

```
convention-api-interne/
├── SKILL.md              # instructions principales
├── reference/
│   ├── nommage.md        # conventions de nommage
│   └── erreurs.md        # format des réponses d'erreur
└── scripts/
    └── valider_openapi.py
```

Le `SKILL.md` minimal ressemble à ceci :

```markdown
---
name: convention-api-interne
description: Applique les conventions internes de conception d'API REST (nommage, pagination, format d'erreur). À utiliser dès qu'il s'agit de créer ou modifier un endpoint, un contrôleur ou une spécification OpenAPI.
---

# Conventions API internes

## Règles non négociables
- Pagination toujours par curseur, jamais par offset
- Les erreurs suivent le format RFC 7807 (`application/problem+json`)
- Aucun champ `null` dans les réponses : on omet la clé

## Détail
**Nommage des ressources** : voir [reference/nommage.md](reference/nommage.md)
**Catalogue des codes d'erreur** : voir [reference/erreurs.md](reference/erreurs.md)
```

La bonne métaphore n'est pas « je programme une fonction », c'est **« j'écris le guide d'onboarding d'un nouveau collègue »**. Un collègue déjà très compétent, à qui il faut transmettre non pas les bases du métier, mais ce qui est spécifique à votre contexte.

Ce format est devenu un standard ouvert : un skill écrit une fois peut être chargé dans différents environnements compatibles — outil en ligne de commande, interface web, API — sans être réécrit.

## Le mécanisme qui rend ça viable : la divulgation progressive

Naïvement, on pourrait se dire : « si j'ai cinquante skills, j'ai cinquante documents dans le contexte du modèle, ça ne passe pas ». C'est là que se trouve l'idée centrale.

Le chargement se fait en trois niveaux :

| Niveau | Contenu | Quand c'est chargé | Coût |
|---|---|---|---|
| 1 | `name` + `description` | Toujours, au démarrage | ~100 tokens par skill |
| 2 | Le corps de `SKILL.md` | Quand le skill se déclenche | Quelques milliers de tokens |
| 3 | Fichiers de référence, scripts | À la demande, un par un | Zéro tant que non lu |

Concrètement : l'agent ne connaît en permanence que le nom et la description de vos skills. Quand votre demande correspond à l'un d'eux, il lit le `SKILL.md` — et seulement alors. Si ce fichier renvoie vers `reference/erreurs.md`, il ira le chercher uniquement si la tâche le nécessite.

Le cas des scripts est particulièrement élégant : un script est **exécuté**, pas lu. Seule sa sortie entre dans le contexte, jamais son code. Un validateur de 400 lignes vous coûte donc trois mots : « Validation OK ».

C'est ce qui permet d'embarquer une documentation d'API complète, un schéma de base de données entier ou des dizaines d'exemples dans un skill, sans pénalité tant que personne n'en a besoin.

## Skill, prompt, MCP : qui fait quoi ?

La confusion est fréquente, alors clarifions :

- **Un prompt** est une instruction ponctuelle, valable pour une conversation. Il disparaît ensuite.
- **Un skill** est du savoir-faire procédural persistant, chargé automatiquement quand il est pertinent. Il répond à la question *« comment fait-on ça ici ? »*.
- **MCP** (Model Context Protocol) est un protocole de connexion à des systèmes externes. Il répond à *« à quoi l'agent a-t-il accès ? »*.

Les deux derniers sont complémentaires, pas concurrents : MCP donne l'accès à votre Jira, un skill explique votre workflow de tickets. L'un ouvre la porte, l'autre indique quoi faire une fois entré.

---

## Les bonnes pratiques

### 1. La description est le point le plus critique du fichier

C'est la seule chose que l'agent voit en permanence. C'est elle, et elle seule, qui décide si votre skill se déclenche ou reste inerte. Une description approximative produit un skill qui ne sert jamais — et le diagnostic est presque toujours là.

Trois règles :

**Dire ce que ça fait ET quand l'utiliser.** Les deux, pas l'un des deux.

**Écrire à la troisième personne.** La description est injectée dans le prompt système ; un « je peux vous aider à… » crée des incohérences de point de vue qui nuisent à la sélection.

**Inclure les mots que les gens tapent réellement.** Si vos collègues disent « la doc », « le readme » et « documenter », les trois doivent figurer.

```yaml
# ✗ Trop vague — ne se déclenchera jamais
description: Aide avec les documents

# ✓ Précise et déclenchable
description: Extrait le texte et les tableaux de fichiers PDF, remplit des
  formulaires, fusionne des documents. À utiliser dès qu'il s'agit de PDF, de
  formulaires ou d'extraction documentaire.
```

Un défaut connu des agents est de **sous-déclencher** les skills — de ne pas les utiliser alors qu'ils seraient utiles. Une description légèrement insistante (« utilise ce skill dès que l'utilisateur mentionne X, même sans demander explicitement Y ») corrige efficacement ce biais.

### 2. Être concis : le contexte est un bien commun

Votre skill partage la fenêtre de contexte avec l'historique de conversation, les autres skills et la demande réelle de l'utilisateur. Chaque paragraphe doit justifier son coût.

Le réflexe à adopter : **partez du principe que le modèle est déjà compétent**. Il sait ce qu'est un PDF, ce que fait `pip install`, ce qu'est une jointure SQL. Ce qu'il ignore, c'est que *chez vous* on exclut toujours les comptes de test, que la colonne `statut` a trois valeurs métier non documentées, et que la migration doit tourner avant le déploiement.

Devant chaque phrase, posez la question : « est-ce qu'il a vraiment besoin qu'on le lui dise ? »

### 3. Doser le degré de liberté selon la fragilité de la tâche

C'est un arbitrage, pas une préférence de style. L'image utile : un agent qui traverse un terrain.

**Terrain dégagé, plusieurs chemins valables → liberté élevée.** Des instructions en prose suffisent.

```markdown
## Revue de code
1. Analyser la structure et l'organisation
2. Chercher les bugs potentiels et cas limites
3. Vérifier le respect des conventions du projet
```

**Passerelle étroite avec du vide de chaque côté → liberté faible.** Un script précis, sans marge d'interprétation.

```markdown
## Migration de base
Exécuter exactement cette commande :
`python scripts/migrate.py --verify --backup`
Ne pas la modifier, ne pas ajouter d'options.
```

Une revue de code appelle du jugement contextuel. Une migration de production n'en appelle aucun.

### 4. Structurer plutôt qu'empiler

Visez **moins de 500 lignes** dans le `SKILL.md`. Au-delà, découpez vers des fichiers de référence.

Deux règles de structuration qui font une vraie différence :

**Un seul niveau de profondeur.** Tous les fichiers de référence doivent être liés depuis `SKILL.md` directement. Si `SKILL.md` renvoie vers `avance.md` qui renvoie vers `details.md`, l'agent aura tendance à ne lire les fichiers imbriqués que partiellement — et travaillera sur une information incomplète.

**Une table des matières dans les fichiers longs.** Au-delà de 100 lignes, un sommaire en tête de fichier permet à l'agent de voir tout ce qui est disponible même s'il ne lit qu'un extrait.

Et organisez par **domaine** plutôt que par ordre d'écriture. Une question sur la facturation ne devrait pas charger le schéma marketing.

### 5. Des workflows explicites et des boucles de validation

Pour toute opération à plusieurs étapes, décomposez-les et numérotez-les. Une checklist que l'agent recopie et coche au fur et à mesure évite les étapes sautées.

Encore plus efficace : la **boucle de rétroaction**.

```markdown
## Processus d'édition
1. Modifier `word/document.xml`
2. Valider immédiatement : `python scripts/validate.py dossier/`
3. Si la validation échoue : lire l'erreur, corriger, revalider
4. Ne continuer que si la validation passe
5. Reconstruire le document
```

Le validateur n'a pas besoin d'être un script. Un `GUIDE_STYLE.md` avec une checklist de relecture fonctionne selon la même logique : produire, confronter à un critère objectif, corriger, recommencer.

Pour les opérations en lot ou destructives, ajoutez une variante : **plan → validation du plan → exécution**. L'agent écrit d'abord ses changements dans un fichier intermédiaire, un script vérifie ce fichier, et l'exécution ne démarre qu'ensuite. Les erreurs sont attrapées avant d'avoir touché quoi que ce soit.

### 6. Les anti-patterns qui coûtent cher

**Les informations datées.** « Avant mars 2026, utiliser l'ancienne API » deviendra faux. Décrivez la méthode actuelle, et reléguez l'historique dans une section « anciens usages » repliée.

**Le vocabulaire flottant.** Choisissez un terme et tenez-le. Alterner entre « champ », « case », « élément » et « contrôle » pour désigner la même chose complique l'analyse.

**Le catalogue d'options.** « Vous pouvez utiliser pypdf, ou pdfplumber, ou PyMuPDF… » Donnez un défaut, et une porte de sortie pour les cas particuliers. Un seul chemin par défaut.

**Les chemins Windows.** Toujours des slashes avant : `scripts/helper.py`. Les antislashes cassent sur les environnements Unix, où tournent la plupart des agents.

**Les constantes magiques.** `TIMEOUT = 47` — pourquoi 47 ? Si vous ne savez pas justifier une valeur, l'agent ne le saura pas davantage. Commentez, ou choisissez une valeur défendable.

**Les scripts qui abandonnent.** Un script de skill doit gérer ses erreurs, pas les renvoyer à l'agent en espérant qu'il improvise. Fichier manquant ? Créez-le avec un contenu par défaut et signalez-le. La règle est : *résoudre, ne pas déléguer*.

### 7. Évaluer avant de documenter

C'est le conseil le moins intuitif, et probablement le plus rentable.

La tentation est d'écrire un skill exhaustif d'un coup. Le résultat classique : trois pages qui documentent des problèmes imaginaires et passent à côté des vrais.

L'approche inverse :

1. **Faire tourner l'agent sans skill** sur des tâches représentatives
2. **Noter les échecs concrets** — ce qu'il rate, ce qu'il ignore, ce qu'il invente
3. **Écrire le minimum** nécessaire pour corriger ces échecs précis
4. **Retester** et comparer à la référence sans skill
5. **Itérer**

Trois scénarios de test suffisent pour démarrer. Ils deviennent votre référence objective : sans eux, vous n'avez que des impressions.

### 8. Écrire ses skills avec l'agent lui-même

Le mode de travail le plus efficace utilise deux instances. Une instance **A** vous aide à concevoir et rédiger le skill ; une instance **B**, fraîche et équipée du skill, l'utilise sur de vraies tâches.

Vous observez B, vous rapportez à A. « Quand B a utilisé le skill, il a oublié de filtrer les comptes de test alors que la règle y figure — elle n'est peut-être pas assez visible ? » A propose une reformulation, vous retestez.

Ce qu'il faut observer chez B :

- **Des chemins d'exploration inattendus** : il lit les fichiers dans un ordre imprévu ? Votre structure n'est pas aussi évidente que vous le pensiez.
- **Des liens ignorés** : il ne suit pas une référence importante ? Le renvoi doit être plus explicite.
- **Un fichier jamais lu** : il est inutile, ou mal signalé.
- **Un fichier toujours lu** : son contenu a peut-être sa place directement dans `SKILL.md`.

Itérez sur ces observations, pas sur vos hypothèses.

Testez aussi avec les différents modèles que vous comptez utiliser : ce qui suffit à un modèle puissant peut manquer de détails pour un modèle plus rapide, et ce qui aide un petit modèle peut noyer un grand sous des explications inutiles.

---

## Un point de vigilance : un skill est du code

C'est le corollaire de sa puissance. Un skill donne des instructions et peut exécuter du code — donc un skill malveillant peut faire agir l'agent d'une manière qui ne correspond pas à ce qu'il annonce : exfiltration de données, accès non autorisé, appels réseau inattendus.

Traitez l'installation d'un skill comme l'installation d'une dépendance : n'utilisez que des sources de confiance, et auditez l'intégralité du dossier — le `SKILL.md`, mais aussi les scripts, les ressources et les fichiers de référence. Méfiance particulière envers les skills qui vont chercher du contenu sur des URL externes : ce contenu peut changer après votre audit.

## La checklist avant de partager

- [ ] La description dit ce que fait le skill **et** quand l'utiliser
- [ ] Elle contient les termes que les utilisateurs emploient réellement
- [ ] Le `SKILL.md` fait moins de 500 lignes
- [ ] Les références sont à un seul niveau de profondeur
- [ ] Aucune information datée hors section « anciens usages »
- [ ] Terminologie cohérente d'un bout à l'autre
- [ ] Les exemples sont concrets, pas abstraits
- [ ] Les scripts gèrent leurs erreurs
- [ ] Toutes les constantes sont justifiées
- [ ] Chemins en slashes avant uniquement
- [ ] Au moins trois évaluations écrites et passées
- [ ] Testé sur de vrais cas d'usage, pas seulement sur des scénarios inventés

## Pour finir

Un skill ne rend pas un modèle plus intelligent. Il lui donne le contexte qui lui manquait — et ce contexte, vous êtes le seul à l'avoir.

Le plus dur n'est d'ailleurs pas technique. C'est de repérer, dans ce que vous réexpliquez pour la troisième fois cette semaine, la partie qui mérite d'être écrite une bonne fois. Commencez par un seul skill, sur un seul irritant récurrent. Le format est du Markdown dans un dossier : le coût d'entrée est presque nul, et le coût de l'erreur aussi.

---

*Ressources : la documentation officielle des Agent Skills et le guide d'authoring d'Anthropic (`platform.claude.com/docs`), ainsi que le dépôt open source `github.com/anthropics/skills` pour des exemples complets.*
