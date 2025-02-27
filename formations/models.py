from django.db import models
from django.contrib.auth.models import User

class Departement(models.Model):
    nom = models.CharField(max_length=100)
    chef = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='departement_dirige')
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.nom

class Formation(models.Model):
    STATUT_CHOICES = [
        ('brouillon', 'Brouillon'),
        ('soumis', 'Soumis pour validation'),
        ('valide', 'Validé'),
        ('rejete', 'Rejeté'),
    ]
    
    titre = models.CharField(max_length=200)
    description = models.TextField()
    objectifs = models.TextField()
    departement = models.ForeignKey(Departement, on_delete=models.CASCADE, related_name='formations')
    responsable = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='formations_dirigees')
    credits_total = models.PositiveIntegerField(default=0)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='brouillon')
    
    def __str__(self):
        return self.titre

class Module(models.Model):
    formation = models.ForeignKey(Formation, on_delete=models.CASCADE, related_name='modules')
    titre = models.CharField(max_length=200)
    description = models.TextField()
    credits = models.PositiveIntegerField(default=0)
    enseignant = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='modules_enseignes')
    
    def __str__(self):
        return self.titre

