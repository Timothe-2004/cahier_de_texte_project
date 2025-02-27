# models.py (cours)
from django.db import models
from django.contrib.auth.models import User
from formations.models import Module

class Cours(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='cours')
    titre = models.CharField(max_length=200)
    description = models.TextField()
    enseignant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cours_enseignes')
    date_debut = models.DateField()
    date_fin = models.DateField()
    heures_total = models.PositiveIntegerField()
    
    def __str__(self):
        return self.titre
    
    def progression(self):
        heures_realisees = sum(seance.duree for seance in self.seances.all())
        if self.heures_total == 0:
            return 0
        return (heures_realisees / self.heures_total) * 100

class Ressource(models.Model):
    cours = models.ForeignKey(Cours, on_delete=models.CASCADE, related_name='ressources')
    titre = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    fichier = models.FileField(upload_to='ressources/', blank=True, null=True)
    lien = models.URLField(blank=True, null=True)
    date_ajout = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.titre