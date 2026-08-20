# Headroom : la couche de compression qui réduit la facture tokens de vos agents IA

*Auteur : Nicolas Koudota — 20 août 2026*

---

## Introduction

Les agents IA (Claude Code, Cursor, Codex…) consomment des tokens à un rythme effréné, et la facture devient un vrai sujet en entreprise. Chaque tour de boucle agent renvoie au modèle l'historique de conversation, les sorties d'outils, les logs, les extraits de code — et tout ça se paye à chaque itération.

**Headroom** est un projet open source créé par **Tejas Chopra**, ingénieur senior chez Netflix, présenté à l'Open Source Summit. Son constat : près de 90 % de ce qu'on envoie à un grand modèle de langage serait de la redondance payée au prix fort. Headroom compresse tout ce contexte **avant** qu'il n'atteigne l'API — mêmes réponses, fraction des tokens.

## Comment ça marche

Headroom s'installe comme un **proxy local** (port 8787) entre votre agent et le fournisseur LLM. Pipeline :

1. **CacheAligner** — détecte le contenu volatile qui casserait le cache KV du provider ; ne réécrit jamais les prompts
2. **ContentRouter** — devine le type de contenu et le dirige vers le bon compresseur
3. **Compresseurs** :
   - **SmartCrusher** — JSON universel (70-90 % de réduction)
   - **CodeCompressor** — compression AST (tree-sitter) : préserve imports, signatures et types, compresse les corps de fonctions (Java, Python, JS/TS, Go, Rust, C/C++, Perl…)
   - **Kompress-v2-base** — modèle ML (HuggingFace) pour texte, logs et résultats RAG
4. **CCR (Compress-Cache-Retrieve)** — les originaux sont stockés localement (SQLite/Redis) ; si le modèle a besoin de la version complète, il les récupère à la demande via l'outil MCP `headroom_retrieve`

Point clé : la **live-zone compression** ne compresse que les nouveaux octets (sortie d'outil fraîche, dernier tour) — le préfixe gelé reste identique, donc le cache de contexte du provider continue de fonctionner.

## Installation et modes d'utilisation

```bash
# Installation (Python 3.10+)
uv tool install --python 3.13 "headroom-ai[all]"
# ou
pip install "headroom-ai[all]"
# ou Docker
docker pull ghcr.io/headroomlabs-ai/headroom:latest
```

Trois modes principaux :

| Mode | Commande | Usage |
|---|---|---|
| Proxy | `headroom proxy --port 8787` | Intermédiaire transparent compatible OpenAI/Anthropic, zéro changement de code |
| Agent wrap | `headroom wrap claude` (codex, grok, copilot, cursor, aider, opencode, cline…) | Lance le proxy + configure l'agent ; `headroom unwrap <tool>` pour annuler |
| MCP server | `headroom mcp install` | Outils `headroom_compress`, `headroom_retrieve`, `headroom_stats` pour tout client MCP |

Le mode proxy est compatible avec n'importe quel client OpenAI-compatible : il suffit de pointer l'URL de base de votre application vers `http://localhost:8787/v1`.

## Gains mesurés

| Workload | Avant | Après | Économie |
|---|---:|---:|---:|
| Recherche de code (100 résultats) | 17 765 | 1 408 | **92 %** |
| Debug incident SRE | 65 694 | 5 118 | **92 %** |
| Triage issue GitHub | 54 174 | 14 761 | **73 %** |
| Exploration de codebase | 78 502 | 41 254 | **47 %** |

Précision préservée sur les benchmarks standards : **GSM8K ±0.000**, **TruthfulQA +0.030**. Headroom annonce 60-95 % de tokens en moins sur les données JSON, 15-20 % sur les agents de codage, et aurait déjà économisé environ **700 000 $** à ses utilisateurs (200 milliards de tokens).

Bonus : le mode **output shaping** (`HEADROOM_OUTPUT_SHAPER=1`) réduit aussi ce que le modèle écrit en retour (préambules, code restaté, « thinking » superflu), avec une estimation honnête des gains via `headroom output-savings`.

## Pour qui ? (analyse honnête)

| Cas | Verdict |
|---|---|
| Équipe qui dépense 100-1000 $/mois en Claude/OpenAI (agents de code, CI) | ✅ ROI immédiat |
| Usage perso modéré | ⚠️ Gains réels mais faibles en euros |
| Provider déjà très bon marché (DeepSeek…) avec cache de contexte automatique | ⚠️ Une partie du gain est déjà captée côté provider |
| Environnement sandboxé (impossible de lancer un process local) | ❌ Pas adapté |

À surveiller : **latence ajoutée**, compatibilité du **tool calling** (des schémas JSON compressés peuvent casser un client strict), et le modèle ML qui doit être chargé en mémoire (RAM/CPU). L'idéal : tester sur un client secondaire avant d'intercaler le proxy en production.

## Conclusion

Headroom est un bel exemple d'ingénieur qui règle son propre problème — la facture tokens — et partage la solution gratuitement sous licence Apache 2.0, sans en faire une startup. Pour les équipes qui carburent aux agents IA, c'est un candidat sérieux pour réduire un poste de dépense devenu douloureux.

## Références

- Repo GitHub : https://github.com/headroomlabs-ai/headroom
- Documentation : https://headroom-docs.vercel.app/docs
- Modèle Kompress-v2-base : https://huggingface.co/chopratejas/kompress-v2-base
- Article The Register : https://www.theregister.com/ai-ml/2026/05/31/netflix-wiz-creates-app-to-slash-ai-bills-then-open-sources-it/5248702
- Article Korben : https://korben.info/un-ingenieur-de-netflix-cree-une-appli-pour-alleger-ses-factures-dia-puis-louvre-a-tout-le-monde.html
