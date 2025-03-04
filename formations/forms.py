# forms.py (formations)
from django import forms
from .models import Formation, Cours
from accounts.models import User

class FormationForm(forms.ModelForm):
    """
    Formulaire pour la création et la modification d'une formation.
    Note: Le champ 'responsable' n'est pas inclus dans le formulaire car il est
    automatiquement défini comme l'utilisateur qui crée la formation dans la vue.
    """
    class Meta:
        model = Formation
        fields = ['titre', 'description', 'responsable']
        widgets = {
            'titre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Titre de la formation'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Description de la formation'
            }),
            'responsable': forms.Select(attrs={
                'class': 'form-control'
            })
        }
        labels = {
            'titre': 'Titre de la formation',
            'description': 'Description',
            'responsable': 'Responsable de la formation'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['responsable'].queryset = User.objects.filter(role='enseignant')

class CoursForm(forms.ModelForm):
    """
    Formulaire pour la création et la modification d'un cours.
    Note: Le champ 'formation' n'est pas inclus dans le formulaire car il est
    automatiquement défini dans la vue en fonction de la formation parente.
    """
    class Meta:
        model = Cours
        fields = ['titre', 'description', 'formation', 'enseignant']
        widgets = {
            'titre': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'formation': forms.Select(attrs={'class': 'form-control'}),
            'enseignant': forms.Select(attrs={'class': 'form-control'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrer les enseignants pour n'afficher que ceux qui ont le rôle d'enseignant
        self.fields['enseignant'].queryset = User.objects.filter(role='enseignant')
        self.fields['enseignant'].empty_label = "Sélectionner un enseignant"
