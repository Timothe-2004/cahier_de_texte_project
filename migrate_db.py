import os
import sys
import django
from django.core.management import call_command
from django.db import connections
from django.conf import settings
import json

# Configuration de l'environnement Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cahier_de_texte.settings')
django.setup()

def migrate_data():
    try:
        # Liste des applications à migrer
        apps = ['accounts', 'formations', 'cours', 'seances', 'reporting']
        
        print("Création des sauvegardes par application...")
        
        # Sauvegarde de chaque application séparément
        for app in apps:
            print(f"Sauvegarde de l'application {app}...")
            backup_file = f'{app}_backup.json'
            try:
                with open(backup_file, 'w', encoding='utf-8') as f:
                    call_command('dumpdata', app, 
                               '--indent', '2',
                               '--exclude', 'auth.permission',
                               stdout=f)
                print(f"Sauvegarde de {app} terminée!")
            except Exception as app_error:
                print(f"Erreur lors de la sauvegarde de {app}: {str(app_error)}")
                continue

        # Configuration pour PostgreSQL
        os.environ['DATABASE_URL'] = 'postgresql://admin:u9gBdkqfIGj69mglbgtfRReXJ5za9WmP@dpg-cv46b95ds78s73e4hvlg-a:5432/cahier_de_texte'
        
        # Migration vers PostgreSQL
        print("\nMigration du schéma vers PostgreSQL...")
        call_command('migrate')
        
        # Chargement des données dans PostgreSQL
        print("\nChargement des données dans PostgreSQL...")
        for app in apps:
            backup_file = f'{app}_backup.json'
            if os.path.exists(backup_file):
                try:
                    print(f"Chargement des données de {app}...")
                    call_command('loaddata', backup_file)
                    print(f"Données de {app} chargées avec succès!")
                except Exception as load_error:
                    print(f"Erreur lors du chargement de {app}: {str(load_error)}")
        
        print("\nMigration terminée!")
        
    except Exception as e:
        print(f"Une erreur s'est produite : {str(e)}")
        import traceback
        traceback.print_exc()
        
if __name__ == '__main__':
    migrate_data() 