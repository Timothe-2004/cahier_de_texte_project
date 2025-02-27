# models.py (seances)
from django.db import models
from django.contrib.auth.models import User
from cours.models import Cours

class Seance(models.Model):
    cours = models.ForeignKey(Cours, on_delete=models.CASCADE, related_name='seances')
    titre = models.CharField(max_length=200)
    description = models.TextField()
    contenu = models.TextField(verbose_name="Cahier de texte")
    date = models.DateField()
    heure_debut = models.TimeField()
    heure_fin = models.TimeField()
    duree = models.PositiveIntegerField(help_text="Durée en heures")
    salle = models.CharField(max_length=50, blank=True)
    
    def __str__(self):
        return f"{self.titre} - {self.date}"
    
    @property
    def est_passee(self):
        from django.utils import timezone
        now = timezone.now().date()
        return self.date < now

class Presence(models.Model):
    seance = models.ForeignKey(Seance, on_delete=models.CASCADE, related_name='presences')
    etudiant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='presences')
    present = models.BooleanField(default=False)
    justification = models.TextField(blank=True)
    
    class Meta:
        unique_together = ['seance', 'etudiant']

class Objectif(models.Model):
    seance = models.ForeignKey(Seance, on_delete=models.CASCADE, related_name='objectifs')
    description = models.TextField()
    atteint = models.BooleanField(default=False)
    
    def __str__(self):
        return self.description[:50]