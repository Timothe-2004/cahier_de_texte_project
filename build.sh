#!/bin/bash

# Mise à jour de pip
python -m pip install --upgrade pip

# Installation des dépendances
pip install -r requirements.txt

# Vérification de l'installation de crispy-forms
pip show django-crispy-forms
pip show crispy-bootstrap5

# Collecte des fichiers statiques
python manage.py collectstatic --noinput

python manage.py migrate