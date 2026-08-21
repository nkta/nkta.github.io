# VisiData : le couteau suisse ultime pour explorer vos CSV dans le terminal

Ouvrir un tableur lourd juste pour inspecter un export CSV de plusieurs centaines de mégaoctets est souvent une corvée. Entre les lenteurs de chargement, les conversions automatiques de formats non désirées et la consommation de mémoire vive, l’expérience s'avère vite frustrante.

C'est ici qu'intervient **VisiData** (`vd`), un utilitaire en ligne de commande conçu pour visualiser, nettoyer, filtrer et analyser des données tabulaires directement dans le terminal Linux.

---

## Pourquoi adopter VisiData ?

Contrairement aux simples paginateurs comme `less` ou à la commande `column`, VisiData ne se contente pas d'afficher des données : il s'agit d'un véritable environnement d'analyse interactif.

* **Performances remarquables :** gestion fluide de millions de lignes sans saturer la mémoire.
* **Flexibilité des formats :** support natif des séparateurs personnalisés (point-virgule, tabulation, pipe) et de formats variés (CSV, TSV, JSON, SQLite, Parquet).
* **Navigation fluide :** prise en main naturelle basée sur les raccourcis classiques de Vim (`h`, `j`, `k`, `l`).
* **Non destructif :** vos fichiers originaux restent intacts tant que vous ne forcez pas une sauvegarde explicite.

---

## Installation et premier lancement

L'outil s'installe très simplement via le gestionnaire de paquets de votre distribution ou avec le gestionnaire de paquets Python :

```bash
# Via APT (Debian/Ubuntu)
sudo apt install visidata

# Via pip
pip install visidata

```

Pour ouvrir un fichier standard :

```bash
vd donnees.csv

```

Si votre fichier utilise une extension inhabituelle ou un séparateur particulier (par exemple un point-virgule), précisez simplement les options au lancement :

```bash
vd -f csv --csv-delimiter=";" export.dat

```

---

## Les raccourcis indispensables pour démarrer

L'interface de VisiData repose sur une navigation au clavier particulièrement intuitive une fois les commandes de base assimilées :

| Action | Raccourci |
| --- | --- |
| **Déplacement** | Flèches directionnelles ou `h` `j` `k` `l` |
| **Ajuster la largeur d'une colonne** | `_` (underscore) |
| **Masquer / Réafficher une colonne** | `-` pour masquer, `gv` pour tout réafficher |
| **Trier (croissant / décroissant)** | `[` / `]` |
| **Typer les données** | `#` (entier), `%` (décimal), `@` (date), `~` (texte) |
| **Quitter la vue actuelle** | `q` |
| **Aide contextuelle** | `Ctrl + h` |

---

## Rechercher et filtrer comme un pro

La force de VisiData réside dans sa rapidité d'interrogation. Le flux de travail s'articule généralement autour de trois axes :

### 1. La navigation directe

Pour vous déplacer d'occurrence en occurrence :

* Tapez `/` suivi de votre mot-clé pour chercher dans la colonne active vers le bas.
* Utilisez `g/` pour étendre la recherche à **l'ensemble des colonnes**.
* Naviguez entre les résultats avec `n` (suivant) et `N` (précédent).

### 2. La sélection par expression régulière

Pour sélectionner les lignes pertinentes sans modifier l'affichage global :

* Tapez `|` suivi d'une regex pour marquer les lignes correspondantes dans la colonne active.
* Tapez `g|` pour appliquer le motif sur toutes les colonnes.
* Utilisez `u` pour désélectionner toutes les lignes actives.

> **Astuce :** pour ignorer la casse, préfixez simplement votre recherche par `(?i)`, par exemple : `|(?i)france`.

### 3. L'isolation des résultats

Une fois vos lignes sélectionnées en surbrillance :

* Appuyez sur **`"`** (guillemet double) : VisiData ouvre immédiatement une **nouvelle vue** contenant exclusivement vos données filtrées.
* Vous pouvez y effectuer des calculs, des tris supplémentaires ou exporter ce sous-ensemble avec `Ctrl + s`.
* Appuyez sur `q` pour fermer cette vue temporaire et retrouver votre tableau complet.

---

## Analyse instantanée : la table de fréquences

Besoin d'un aperçu statistique d'une colonne sans écrire une seule ligne de SQL ou de script Python ? Placez votre curseur sur l'en-tête de la colonne et appuyez sur **`Shift + f`** (`F`).

VisiData génère instantanément une table récapitulative listant chaque valeur unique, son occurrence exacte ainsi que son pourcentage par rapport au total. Un gain de temps considérable pour auditer la qualité d'un jeu de données en un coup d'œil.

---

Adopté au quotidien, VisiData transforme l'exploration de données brutes en une tâche rapide, fluide et directement intégrée à vos flux de travail en terminal.