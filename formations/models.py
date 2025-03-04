from django.db import models
from django.conf import settings
from accounts.models import User

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
    departement = models.CharField(max_length=100)  # Champ texte pour saisie manuelle
    responsable = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='formations_responsable',
        limit_choices_to={'role': 'enseignant'}
    )
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='brouillon')
    
    def __str__(self):
        return self.titre

    class Meta:
        verbose_name = "Formation"
        verbose_name_plural = "Formations"
        ordering = ['titre']

class Cours(models.Model):
    formation = models.ForeignKey(Formation, on_delete=models.CASCADE, related_name='cours')
    titre = models.CharField(max_length=200)
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField()
    credits = models.PositiveIntegerField(default=0)
    enseignant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='cours_enseignes')
    volume_horaire = models.PositiveIntegerField(help_text="Nombre d'heures total")
    
    def __str__(self):
        return f"{self.code} - {self.titre}"

    class Meta:
        verbose_name = "Cours"
        verbose_name_plural = "Cours"
        ordering = ['code']