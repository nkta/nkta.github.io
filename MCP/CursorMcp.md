# Configurer un serveur MCP dans Cursor sous Windows 11 + WSL

*Auteur : \[Votre Nom] — 7 mai 2025*

---

## Introduction

Le **Model Context Protocol (MCP)** arrive dans l’écosystème des IDE intelligents ! Avec **Cursor**, il devient possible d’exposer vos propres « outils » (fonctions, APIs internes, modèles IA…) directement dans la palette de commandes. Cet article décrit **pas à pas** comment :

1. Installer et configurer **FastMCP** dans **WSL Ubuntu 22.04** ;
2. Écrire un serveur MCP minimaliste en Python ;
3. Connecter ce serveur à Cursor via le transport **STDIO** ;
4. Tester et déboguer l’intégration.

> Vous êtes pressé ? Clonez l’exemple complet 👉 `https://github.com/votre‑repo/mcp‑cursor‑demo` puis suivez la section *Test rapide*.

---

## Pourquoi choisir MCP ?

| Avantages            | Explications                                                                            |
| -------------------- | --------------------------------------------------------------------------------------- |
| 🔌 **Interopérable** | Basé sur JSON‑RPC, fonctionne avec n’importe quel langage                               |
| 🛠️ **Extensible**   | Chaque fonction décorée devient un « outil » utilisable par Cursor ou tout autre client |
| ⚡ **Rapide**         | Le transport STDIO évite la latence réseau                                              |
| 🔒 **Sécurisé**      | Pas d’ouverture de port externe nécessaire en mode local                                |

---

## Prérequis

* **Windows 11** avec **WSL 2** (distro Ubuntu 22.04)
* **Cursor ≥ 0.45** (onglet *Features › MCP*)
* **Python ≥ 3.10** installé dans WSL

```bash
# Vérifier côté WSL
python3 --version   # Python 3.10+
pip --version       # pip 23+
```

---

## Étape 1 : installer FastMCP dans WSL

```bash
# Dans WSL
python3 -m pip install --upgrade "fastmcp[stdlib]"
```

> La variante `[stdlib]` installe uniquement les dépendances nécessaires au transport STDIO, évitant une image Docker plus lourde.

---

## Étape 2 : écrire un serveur MCP minimaliste

Créez le fichier **`server.py`** :

```python
#!/usr/bin/env python3
"""
Serveur MCP avec FastMCP – mode STDIO pour Cursor
"""
import logging
from fastmcp import FastMCP

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

mcp = FastMCP("MonServeurMCP")

@mcp.tool()
def add(a: int, b: int) -> int:
    """Additionne deux nombres"""
    return a + b

@mcp.tool()
def multiply(a: int, b: int) -> int:
    """Multiplie deux nombres"""
    return a * b

@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Retourne une salutation personnalisée"""
    return f"Bonjour, {name}!"

if __name__ == "__main__":
    mcp.run()  # bloque sur stdin/stdout jusqu’à l’arrêt
```

Test manuel :

```bash
python3 server.py  # doit rester bloqué
```

---

## Étape 3 : déclarer le serveur dans Cursor

Dans `Cursor Settings › Features › MCP` ajoutez :

```jsonc
{
  "mcpServers": {
    "serveurLocal": {
      "command": "wsl",
      "args": ["python3", "/home/<user>/Workspace_c/essai-mcp/server.py"],
      "transport": "stdio",
      "env": {
        "PYTHONUNBUFFERED": "1",
        "LOG_LEVEL": "DEBUG"
      }
    }
  }
}
```

Relancez Cursor → l’état du serveur doit passer à **READY (stdio)**.

---

## Étape 4 : tester depuis la palette Cursor

1. Ouvrez un fichier quelconque dans l’éditeur.
2. ⌥/Alt + ⎵ → tapez `add` ou `multiply`.
3. Saisissez les paramètres ; Cursor affiche la réponse instantanément.

![Demo Cursor MCP](https://github.com/votre‑repo/assets/cursor‑mcp‑demo.gif)

---

## Débogage & astuces

| Problème                             | Cause probable                        | Solution                                            |
| ------------------------------------ | ------------------------------------- | --------------------------------------------------- |
| *Client closed* dans les logs Cursor | FastMCP parle en HTTP ou s’est crashé | Forcer `mcp.run()` en STDIO et vérifier les imports |
| *ModuleNotFoundError*                | FastMCP absent ou version < 0.6       | `pip install --upgrade fastmcp[stdlib]`             |
| Aucune sortie visible                | Buffering Python                      | Vérifier `PYTHONUNBUFFERED=1`                       |

---

## Aller plus loin

* **Transports alternatifs :** `mcp.run("sse", host="0.0.0.0", port=8000)` pour exposer via HTTP.
* **Outils asynchrones :** déclarez `async def` et laissez FastMCP gérer l’event‑loop.
* **Packaging :** `python -m build` puis `pipx install dist/monserveurmcp-*.whl`.

---

## Conclusion

Vous disposez maintenant d’un serveur MCP fonctionnel, accessible directement depuis Cursor. Cette architecture vous permet d’injecter vos propres workflows IA, requêtes base de données ou automations internes **sans quitter l’éditeur**. Améliorez‑le, partagez‑le à votre équipe, et contribuez à l’écosystème MCP !

> Questions, suggestions ? Ouvrez une issue sur le repo ou laissez un commentaire 👇
