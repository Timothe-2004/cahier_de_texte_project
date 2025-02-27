# forms.py (formations)
from django import forms
from .models import Formation, Module, Departement

class FormationForm(forms.ModelForm):
    class Meta:
        model = Formation
        fields = ['titre', 'description', 'objectifs', 'departement', 'credits_total']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
            'objectifs': forms.Textarea(attrs={'rows': 5}),
        }

class ModuleForm(forms.ModelForm):
    class Meta:
        model = Module
        fields = ['titre', 'description', 'credits', 'enseignant']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
        }
