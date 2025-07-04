# 1001pieces_autofill

Application locale de complétion automatique pour appareils électroménagers à partir d’un tableau interactif, avec base de données intégrée.

## 🚀 Objectif de l’outil

L'application permet de **coller rapidement des données issues d’un tableur** (Excel, OpenOffice, etc.), de les **compléter automatiquement**, puis de les **mémoriser dans une base locale**.

Les correspondances sont trouvées à partir des colonnes **C (reference_modele)** et **D (commercial_reference)**, et permettent de compléter automatiquement les colonnes **A (type)** et **B (manufacturer)**.

---

## 🖥️ Fonctionnalités principales

- ✅ Coller des données depuis le presse-papiers (Ctrl+V / Cmd+V)
- ✅ 6 colonnes intégrées :  
  - A : `type`  
  - B : `manufacturer`  
  - C : `reference_modele`  
  - D : `commercial_reference`  
  - E : `other_reference`  
  - F : `treatment_column`
- ✅ Complétion automatique des colonnes A et B si elles sont vides
- ✅ Recherche de correspondances en base SQLite existante
- ✅ Enregistrement de nouveaux appareils en base
- ✅ Tri par colonne (clic sur l'en-tête)
- ✅ Duplication haut/bas comme dans un tableur :
  - `Ctrl + ↑` : dupliquer cellule vers le haut
  - `Ctrl + ↓` : dupliquer cellule vers le bas
- ✅ Encoche de duplication façon Excel (glisser-remplir)
- ✅ Export CSV rapide

---

## ⚙️ Installation rapide

### 💡 Prérequis

- Python 3.9 ou plus
- macOS ou Windows
- Aucun accès internet requis pendant l'utilisation

### 🚀 Installation en 3 lignes

Ouvre un terminal dans le dossier cloné, puis :

```bash
chmod +x install.sh
./install.sh


📁 Structure du projet
bash
Copier
Modifier
1001pieces_autofill/
├── main.py                  # Application PyQt5
├── install.sh               # Script d'installation rapide
├── requirements.txt         # Dépendances
├── README.md                # Ce fichier
├── appareils.db             # Base de données SQLite (auto-générée)
└── .gitignore               # Exclut le cache et venv
🧠 Données persistantes
Tous les appareils complétés ou injectés sont stockés localement dans appareils.db. Cela permet une complétion plus intelligente à chaque nouvelle utilisation.

🗓️ Roadmap V2 (à venir)
Association des références de pièces détachées

Export vers des formats spécifiques (clients, marketplaces)

Interface multi-onglets ou onglet “Pièces”

Mode recherche avancée et filtres dynamiques

Export Excel avec mise en forme

Version avec installeur .app ou .exe

🤝 Contributeur principal
Pierre-Louis SILLIERE

🛡️ Licence
Projet privé pour usage interne. Non destiné à la distribution publique.