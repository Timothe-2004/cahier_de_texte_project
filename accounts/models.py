from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Administrateur'),
        ('directeur_adjoint', 'Directeur Adjoint'),
        ('chef_departement', 'Chef de Département'),
        ('enseignant', 'Enseignant'),
        ('responsable_classe', 'Responsable de classe'),
    ]
    
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='enseignant'
    )
    telephone = models.CharField(max_length=15, blank=True)
    bureau = models.CharField(max_length=50, blank=True)
    
    class Meta:
        verbose_name = 'Utilisateur'
        verbose_name_plural = 'Utilisateurs'
    
    def is_admin(self):
        return self.role == 'admin'
    
    def is_directeur_adjoint(self):
        return self.role == 'directeur_adjoint'
    
    def is_chef_departement(self):
        return self.role == 'chef_departement'
    
    def is_enseignant(self):
        return self.role == 'enseignant'
    
    def is_responsable_classe(self):
        return self.role == 'responsable_classe'
