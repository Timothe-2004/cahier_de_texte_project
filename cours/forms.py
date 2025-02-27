
# forms.py (cours)
from django import forms
from .models import Cours, Ressource

class CoursForm(forms.ModelForm):
    class Meta:
        model = Cours
        fields = ['module', 'titre', 'description', 'date_debut', 'date_fin', 'heures_total']
        widgets = {
            'date_debut': forms.DateInput(attrs={'type': 'date'}),
            'date_fin': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 5}),
        }

class RessourceForm(forms.ModelForm):
    class Meta:
        model = Ressource
        fields = ['titre', 'description', 'fichier', 'lien']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }