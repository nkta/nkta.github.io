## Tout ce qu’il faut savoir sur le *Prompt Engineering*  
### Synthèse du white‑paper Google (février 2025)

Le *prompt engineering* n’est plus un simple art occulte réservé aux data‑scientists : c’est devenu la compétence n°1 pour quiconque souhaite exploiter la puissance des grands modèles de langage (LLM). Le document technique publié par Google en février 2025 dresse une cartographie complète des méthodes, réglages et bonnes pratiques. En voici l’essentiel.

---

### 1. Un rappel : pourquoi "ingénier‑les‑prompts" ?

Un LLM est avant tout un moteur de prédiction de tokens ; la moindre virgule que vous écrivez change la suite de la phrase que le modèle anticipe. Un prompt mal conçu entraîne donc ambiguïtés, réponses approximatives et même hallucinations ; un prompt soigné maximise la pertinence et la fiabilité. Le *prompt engineering* est le processus itératif qui consiste à concevoir, tester et ajuster ces invites pour guider la génération vers le résultat voulu. [^1]

---

### 2. Régler le modèle : longueur, température, *top‑k*, *top‑p*

- **Longueur de sortie** : plus de tokens = plus de coût et de latence. Coupez‑court si vous n’avez pas besoin d’un roman. [^1]  
- **Température** : 0 → réponse déterministe ; 1 → créativité maximale.  
- **Top‑k / Top‑p** : limites sur le nombre ou la probabilité cumulée des tokens candidats. Mixer ces paramètres permet d'équilibrer cohérence et diversité.  
  > *Astuce de départ* : temp 0,2 / top‑p 0,95 / top‑k 30 pour un style "créatif mais pas trop" ; temp 0 pour les tâches à réponse unique (p. ex. calcul). [^1]

---

### 3. Techniques de prompting incontournables

| Technique | Principe | Quand l'utiliser |
|-----------|----------|------------------|
| **Zero‑shot** | On pose la question, sans exemple | Tâches simples, rapidité | [^1] |
| **One/Few‑shot** | On fournit 1 à 5 démos | Classification, formatage précis | [^1] |
| **System / Role / Context** | On impose un rôle, un style ou un cadre | Personnaliser le ton, garantir un format (JSON, etc.) | [^1] |
| **Step‑back** | Le modèle répond d'abord à une question générale, puis à la spécifique | Débloquer la créativité, activer des connaissances latentes | [^1] |
| **Chain of Thought (CoT)** | "Pensons étape par étape" | Problèmes de raisonnement (maths, logique) | [^1] |
| **Self‑Consistency** | On génère plusieurs CoT, on vote | Monter la fiabilité quand l'erreur coûte cher | [^1] |
| **Tree of Thoughts (ToT)** | Exploration arborescente plutôt que linéaire | Tâches complexes à multiples solutions | [^1] |
| **ReAct** | Raisonner **et** agir via des outils externes | Agents autonomes, recherche web, code execution | [^1] |
| **Automatic Prompt Engineering (APE)** | Le modèle génère et évalue ses propres prompts | Scalabilité, collecte de formulations variées | [^1] |

---

### 4. Bonnes pratiques à retenir

1. **Toujours donner des exemples** : un seul exemple réduit déjà l'ambiguïté ; trois à cinq débloquent les tâches subtiles. [^1]  
2. **Privilégier la clarté** : phrase courte, verbe d'action clair ("Classe", "Résume", "Génère"). [^1]  
3. **Spécifiez le format de sortie** : JSON validé, tableau Markdown, tweet de 280 caractères… plus c'est précis, moins ça hallucine. [^1]  
4. **Instructions > contraintes** : dites ce que le modèle *doit* faire plutôt que de lister tout ce qu'il ne doit pas faire. [^1]  
5. **Contrôlez le budget de tokens** : plafonnez ou demandez "en 3 phrases". [^1]  
6. **Variable‑isez vos prompts** : remplacez `{ville}`, `{produit}`… pour réutiliser le même canevas dans le code. [^1]  
7. **Documentez vos essais** : conservez un tableau "Nom / Objectif / Température / Prompt / Résultat" pour tracer l'itération. [^1]

---

### 5. En pratique : par où commencer ?

1. **Choisissez votre modèle** (Gemini, GPT‑4o, Claude, etc.).  
2. **Fixez temp / top‑k / top‑p** avec les valeurs "cohérentes mais créatives".  
3. **Prototypage rapide** dans un IDE ou Vertex AI Studio pour observer les sorties.  
4. **Itérez** : modifiez un paramètre à la fois, enregistrez, comparez.  
5. **Mettez en production** seulement après avoir cramé les pires hallucinations — et surveillez les coûts de tokens !

---

### Conclusion

Le white‑paper de Google témoigne : le *prompt engineering* est désormais une discipline complète, avec ses réglages fins, ses recettes et ses pièges. En appliquant ces techniques — de la simple *zero‑shot* aux arbres de pensées — vous transformerez vos LLM en collaborateurs fiables et créatifs. Alors, à vos prompts : testez, mesurez, itérez !

[^1]: Source : White-paper Google, février 2025.