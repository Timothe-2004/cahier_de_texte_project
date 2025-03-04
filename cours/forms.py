# forms.py (cours)
from django import forms
from formations.models import Cours
from .models import Ressource

class CoursForm(forms.ModelForm):
    class Meta:
        model = Cours
        fields = ['code', 'titre', 'description', 'credits', 'volume_horaire', 'formation']
        widgets = {
            'code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: INFO101'}),
            'titre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Titre du cours'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'credits': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'volume_horaire': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'formation': forms.Select(attrs={'class': 'form-control'})
        }

class RessourceForm(forms.ModelForm):
    class Meta:
        model = Ressource
        fields = ['titre', 'description', 'fichier']
        widgets = {
            'titre': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'fichier': forms.FileInput(attrs={'class': 'form-control'})
        }