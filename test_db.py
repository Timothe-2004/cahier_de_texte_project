import os
import django
from django.db import connections
from django.conf import settings

# Configuration de l'environnement Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cahier_de_texte.settings')
os.environ['DATABASE_URL'] = 'postgresql://admin:u9gBdkqfIGj69mglbgtfRReXJ5za9WmP@dpg-cv46b95ds78s73e4hvlg-a:5432/cahier_de_texte'

django.setup()

def test_connection():
    try:
        connection = connections['default']
        connection.ensure_connection()
        print("Connexion à PostgreSQL réussie!")
        
        # Effectuer les migrations
        from django.core.management import call_command
        print("\nApplication des migrations...")
        call_command('migrate')
        print("Migrations terminées avec succès!")
        
    except Exception as e:
        print(f"Erreur de connexion : {str(e)}")
        
if __name__ == '__main__':
    test_connection() 