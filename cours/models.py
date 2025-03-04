# models.py (cours)
from django.db import models
from django.conf import settings  # Changer cet import
from formations.models import Cours as FormationCours

class Ressource(models.Model):
    seance = models.ForeignKey('seances.Seance', on_delete=models.CASCADE, related_name='ressources')
    titre = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    fichier = models.FileField(upload_to='ressources/', blank=True, null=True)
    lien = models.URLField(blank=True, null=True)
    date_ajout = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.titre