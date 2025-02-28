# 📌 **Les Différentes Façons d’Utiliser SOQL avec Salesforce**  

## **🔍 Introduction**
**SOQL (Salesforce Object Query Language)** est le langage utilisé pour interroger les bases de données Salesforce. Il est optimisé pour fonctionner avec la structure orientée objet de Salesforce et permet d'extraire des données efficacement.  

Contrairement au SQL classique, **SOQL ne permet pas de faire `SELECT *`**, mais offre des fonctionnalités puissantes adaptées à l’architecture Salesforce. Il est utilisé dans plusieurs contextes : **Developer Console, Workbench, API REST, Apex, et plus encore**.  

Dans cet article, nous allons voir **les différentes façons d’exécuter des requêtes SOQL dans Salesforce**, avec des exemples pratiques.  

---

## **1️⃣ Utiliser SOQL dans la Developer Console**
### **📌 Qu’est-ce que la Developer Console ?**
La **Developer Console** est un outil intégré à Salesforce qui permet de tester du code Apex et d’exécuter des requêtes **SOQL/SOSL** en temps réel.

### **🛠️ Comment exécuter une requête SOQL ?**
1. **Ouvre la Developer Console** :
   - Clique sur ton avatar (en haut à droite).
   - Sélectionne **"Developer Console"**.
2. **Va dans l'onglet "Query Editor"** (en bas).
3. **Tape ta requête SOQL**, par exemple :
   ```soql
   SELECT Id, Name FROM Account LIMIT 10
   ```
4. **Clique sur "Execute"**.

### ✅ **Avantages**
✔ Rapide et facile à utiliser.  
✔ Permet de **tester rapidement des requêtes**.  
✔ Les résultats s’affichent sous forme de tableau.  

### ❌ **Limitations**
🚫 Impossible d’utiliser `SELECT *`, il faut lister chaque champ.  
🚫 Ne permet pas d’exécuter des requêtes sur plusieurs objets en même temps (utiliser SOSL pour cela).  

---

## **2️⃣ Utiliser SOQL avec Workbench**
### **📌 Qu’est-ce que Workbench ?**
**Workbench** est un outil web permettant d'exécuter **SOQL, SOSL, et d’interagir avec l’API Salesforce**. Il est souvent utilisé par les administrateurs et développeurs pour tester des requêtes plus complexes.

### **🛠️ Comment utiliser Workbench ?**
1. **Va sur** [Workbench](https://workbench.developerforce.com).
2. **Connecte-toi avec ton compte Salesforce**.
3. **Va dans "Queries" > "SOQL Query"**.
4. **Tape ta requête** et clique sur "Execute".

### ✅ **Avantages**
✔ Permet d’exécuter des requêtes **sans écrire de code Apex**.  
✔ Peut récupérer **tous les champs d’un objet** facilement.  
✔ Pratique pour tester des requêtes avec l’API REST.  

### ❌ **Limitations**
🚫 Nécessite une connexion Internet.  
🚫 Peut être bloqué par certaines entreprises.  

---

## **3️⃣ Utiliser SOQL avec Apex**
### **📌 Pourquoi utiliser SOQL dans Apex ?**
SOQL est souvent intégré dans **du code Apex** pour exécuter des requêtes dynamiquement et automatiser des traitements sur les données Salesforce.

### **🛠️ Exemple de SOQL dans Apex**
```apex
public class AccountHandler {
    public static void getAccounts() {
        List<Account> accounts = [SELECT Id, Name FROM Account LIMIT 10];
        for (Account acc : accounts) {
            System.debug('Compte trouvé : ' + acc.Name);
        }
    }
}
```
📌 **Explication** :
- On récupère une **liste d’objets `Account`** avec `SELECT Id, Name FROM Account`.
- On affiche les résultats dans les logs (`System.debug`).

### ✅ **Avantages**
✔ Intégré directement dans **les classes Apex**.  
✔ Permet de **manipuler les données Salesforce** avec des boucles et des conditions.  
✔ Utile pour **développer des applications et des triggers**.  

### ❌ **Limitations**
🚫 **Les requêtes SOQL sont limitées à 50 000 enregistrements** dans une transaction.  
🚫 **Les requêtes trop fréquentes peuvent causer des erreurs de gouvernance**.  

---

## **4️⃣ Utiliser SOQL avec l’API REST**
### **📌 Pourquoi utiliser SOQL avec l’API REST ?**
L’API REST de Salesforce permet d’exécuter **des requêtes SOQL à distance** depuis une autre application (ex: **Postman, Python, JavaScript**).

### **🛠️ Exemple d’appel API REST**
```http
GET https://yourInstance.salesforce.com/services/data/v60.0/query/?q=SELECT+Id,Name+FROM+Account
Authorization: Bearer ACCESS_TOKEN
```
📌 **Explication** :
- **On interroge Salesforce via une requête GET.**
- **On passe la requête SOQL en paramètre (`q=SELECT+Id,Name+FROM+Account`).**
- **On doit inclure un `ACCESS_TOKEN` pour s’authentifier.**

### ✅ **Avantages**
✔ Idéal pour **intégrer Salesforce avec des applications externes**.  
✔ Permet d’automatiser l’extraction de données.  
✔ Fonctionne avec **Postman, Python, JavaScript, etc.**.  

### ❌ **Limitations**
🚫 **Nécessite une authentification OAuth 2.0.**  
🚫 **Peut être soumis à des limites d’appels API Salesforce.**  

---

## **5️⃣ Utiliser SOQL avec Python (Script Automatisé)**
### **📌 Pourquoi utiliser Python avec SOQL ?**
Si tu veux automatiser l’extraction de données depuis Salesforce, **Python + API REST** est une excellente option.

### **🛠️ Exemple de script Python**
```python
import requests

# 1. Authentification OAuth 2.0 pour obtenir un access_token
auth_url = "https://login.salesforce.com/services/oauth2/token"
auth_data = {
    "grant_type": "password",
    "client_id": "TON_CLIENT_ID",
    "client_secret": "TON_CLIENT_SECRET",
    "username": "TON_USERNAME",
    "password": "TON_PASSWORD"
}
auth_response = requests.post(auth_url, data=auth_data)
access_token = auth_response.json().get("access_token")
instance_url = auth_response.json().get("instance_url")

# 2. Exécuter une requête SOQL via l’API REST
query = "SELECT Id, Name FROM Account LIMIT 10"
api_url = f"{instance_url}/services/data/v60.0/query/?q={query}"
headers = {"Authorization": f"Bearer {access_token}"}

response = requests.get(api_url, headers=headers)
print(response.json())
```
✅ **Ce script automatise l’extraction des comptes depuis Salesforce.**  

### ✅ **Avantages**
✔ Automatisation des requêtes SOQL.  
✔ Compatible avec **Flask, Pandas et d’autres outils Python**.  
✔ Permet d’analyser des données Salesforce avec **Data Science et Machine Learning**.  

### ❌ **Limitations**
🚫 Nécessite un accès API REST activé.  
🚫 Besoin de gérer la sécurité et les tokens OAuth.  

---

## **🎯 Conclusion**
| **Méthode** | **Outil** | **Utilisation** |
|------------|----------|----------------|
| **Developer Console** | Interface web Salesforce | Tester des requêtes SOQL |
| **Workbench** | Outil web externe | Explorer les objets et tester SOQL |
| **Apex** | Code Salesforce | Automatiser des requêtes en interne |
| **API REST** | Postman, Python | Intégrer Salesforce avec d'autres applications |
| **Python** | Script automatisé | Extraire et analyser des données Salesforce |

👉 **Quelle méthode veux-tu tester en priorité ? 😊**