# models.py (seances)
from django.db import models
from django.contrib.auth.models import User
from formations.models import Cours as FormationCours
from django.conf import settings
from django.utils import timezone

# ..


class Seance(models.Model):
    cours = models.ForeignKey(FormationCours, on_delete=models.CASCADE, related_name='seances')
    description = models.TextField(verbose_name="Description de la séance", help_text="Description détaillée du contenu prévu", blank=True)
    date = models.DateField()
    heure_debut = models.TimeField()
    heure_fin = models.TimeField()
    salle = models.CharField(max_length=50)
    enseignant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='seances_enseignees')
    
    class Meta:
        ordering = ['-date', '-heure_debut']
        verbose_name = "Séance"
        verbose_name_plural = "Séances"

    def __str__(self):
        return f"{self.cours.titre} ({self.date})"
    
    @property
    def est_passee(self):
        now = timezone.now()
        seance_datetime = timezone.make_aware(
            timezone.datetime.combine(self.date, self.heure_fin)
        )
        return seance_datetime < now

class Presence(models.Model):
    seance = models.ForeignKey(Seance, on_delete=models.CASCADE, related_name='presences')
    etudiant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
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