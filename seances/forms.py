# forms.py (seances)
from django import forms
from django.forms import inlineformset_factory
from .models import Seance, Presence, Objectif
from formations.models import Cours as FormationCours
from accounts.models import User

class SeanceForm(forms.ModelForm):
    class Meta:
        model = Seance
        fields = ['description', 'date', 'heure_debut', 'heure_fin', 'salle', 'enseignant']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'heure_debut': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'heure_fin': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'salle': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'enseignant': forms.Select(attrs={'class': 'form-control'}),
        }

PresenceFormSet = inlineformset_factory(
    Seance, Presence,
    fields=['etudiant', 'present', 'justification'],
    extra=1,
    can_delete=True
)

ObjectifFormSet = inlineformset_factory(
    Seance, Objectif,
    fields=['description', 'atteint'],
    extra=1,
    can_delete=True
)

class CahierTexteForm(forms.ModelForm):
    enseignant = forms.ModelChoiceField(
        queryset=User.objects.filter(role='enseignant'),
        label='Enseignant',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = Seance
        fields = ['cours', 'description', 'date', 'heure_debut', 'heure_fin', 'salle']
        widgets = {
            'cours': forms.Select(attrs={
                'class': 'form-control'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Description détaillée du contenu prévu'
            }),
            'date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'heure_debut': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time'
            }),
            'heure_fin': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time'
            }),
            'salle': forms.TextInput(attrs={
                'class': 'form-control'
            })
        }
        labels = {
            'cours': 'Cours',
            'description': 'Description de la séance',
            'date': 'Date de la séance',
            'heure_debut': 'Heure de début',
            'heure_fin': 'Heure de fin',
            'salle': 'Salle'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.cours:
            self.fields['enseignant'].initial = self.instance.cours.enseignant
            self.fields['cours'].queryset = FormationCours.objects.filter(enseignant=self.instance.cours.enseignant)
        else:
            self.fields['cours'].queryset = FormationCours.objects.all() 