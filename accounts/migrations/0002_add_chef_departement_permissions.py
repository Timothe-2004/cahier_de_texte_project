from django.db import migrations

def copy_permissions(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Permission = apps.get_model('auth', 'Permission')
    
    try:
        directeur_adjoint = Group.objects.get(name='directeur_adjoint')
        chef_departement = Group.objects.get(name='chef_departement')
        
        # Copier toutes les permissions du directeur adjoint au chef de département
        chef_departement_permissions = chef_departement.permissions.all()
        directeur_adjoint_permissions = directeur_adjoint.permissions.all()
        
        # Ajouter les permissions manquantes
        for permission in directeur_adjoint_permissions:
            if permission not in chef_departement_permissions:
                chef_departement.permissions.add(permission)
                
    except Group.DoesNotExist:
        pass

class Migration(migrations.Migration):
    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(copy_permissions),
    ] 