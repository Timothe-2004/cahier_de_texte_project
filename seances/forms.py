# forms.py (seances)
from django import forms
from django.forms import inlineformset_factory
from .models import Seance, Presence, Objectif
from cours.models import Cours

class SeanceForm(forms.ModelForm):
    class Meta:
        model = Seance
        fields = ['cours', 'titre', 'description', 'contenu', 'date', 'heure_debut', 'heure_fin', 'salle']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'heure_debut': forms.TimeInput(attrs={'type': 'time'}),
            'heure_fin': forms.TimeInput(attrs={'type': 'time'}),
            'description': forms.Textarea(attrs={'rows': 3}),
            'contenu': forms.Textarea(attrs={'rows': 5}),
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(SeanceForm, self).__init__(*args, **kwargs)
        if user:
            # Limiter les choix de cours à ceux enseignés par l'utilisateur
            self.fields['cours'].queryset = Cours.objects.filter(enseignant=user)

PresenceFormSet = inlineformset_factory(
    Seance, Presence,
    fields=['etudiant', 'present', 'justification'],
    extra=1, can_delete=True
)

ObjectifFormSet = inlineformset_factory(
    Seance, Objectif,
    fields=['description', 'atteint'],
    extra=1, can_delete=True
)
