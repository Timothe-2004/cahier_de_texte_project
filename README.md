# Cahier de Texte Universitaire

Une application web Django pour la gestion des cours, des enseignants et des séances dans un contexte universitaire.

## 🚀 Installation

1. Cloner le dépôt :
```bash
git clone <url-du-depot>
cd cahier_de_texte
```

2. Créer un environnement virtuel Python :
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Installer les dépendances :
```bash
pip install -r requirements.txt
```

4. Configurer la base de données :
```bash
python manage.py migrate
```

5. Créer un super utilisateur :
```bash
python manage.py createsuperuser
```

6. Lancer le serveur de développement :
```bash
python manage.py runserver
```

## 👥 Rôles et Permissions

L'application gère plusieurs types d'utilisateurs avec des permissions différentes :

### Administrateur
- Créer et gérer les comptes utilisateurs
- Accès complet à toutes les fonctionnalités

### Directeur Adjoint (DA) / Chef de Département (CD)
- Charger l'offre de formation
- Affecter les cours aux enseignants
- Consulter et imprimer les récapitulatifs des cours par enseignant

### Enseignant
- Consulter ses cours affectés
- Consulter et gérer ses séances
- Remplir le cahier de texte pour chaque séance

### Responsable Salle
- Planifier les séances de cours
- Gérer l'occupation des salles

## 🔑 Fonctionnalités principales

### Gestion des Formations
- Création et modification des formations
- Association des cours aux formations
- Définition des volumes horaires

### Gestion des Cours
- Affectation des enseignants aux cours
- Suivi des volumes horaires
- Génération de récapitulatifs

### Gestion des Séances
- Planification des séances
- Gestion du cahier de texte
- Suivi des présences

## 🛠 Technologies utilisées

- Python 3.8+
- Django 5.0
- Bootstrap 5
- FontAwesome
- SQLite (base de données)

## 📝 Utilisation

1. Se connecter avec les identifiants appropriés
2. Accéder au tableau de bord personnalisé selon le rôle
3. Utiliser les différentes fonctionnalités selon les permissions

## 🔒 Sécurité

- Authentification requise pour toutes les pages
- Permissions basées sur les rôles
- Protection CSRF active
- Sessions sécurisées

## 📊 Base de données

Le schéma de la base de données comprend les tables principales suivantes :

- User (utilisateurs et rôles)
- Formation (offres de formation)
- Cours (cours et leurs attributions)
- Seance (séances de cours)
- Presence (suivi des présences)

## 🤝 Contribution

Pour contribuer au projet :

1. Forker le dépôt
2. Créer une branche pour votre fonctionnalité
3. Commiter vos changements
4. Pousser vers la branche
5. Créer une Pull Request

## 📫 Support

Pour toute question ou problème, veuillez :

1. Consulter la documentation
2. Vérifier les issues existantes
3. Créer une nouvelle issue si nécessaire

## 📝 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails. 