#!/bin/bash

# Mise à jour de pip
python -m pip install --upgrade pip

# Installation des dépendances
pip install -r requirements.txt

# Collecte des fichiers statiques
python manage.py collectstatic --noinput

# Migration de la base de données (si nécessaire)
python manage.py migrate --noinput