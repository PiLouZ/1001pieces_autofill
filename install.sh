#!/bin/bash

echo "Installation de l'environnement..."

# Crée un environnement virtuel (facultatif mais recommandé)
python3 -m venv venv
source venv/bin/activate

# Installe les dépendances
pip install -r requirements.txt

echo "Installation terminée. Lancement de l'application..."

# Lance le programme
python main.py
