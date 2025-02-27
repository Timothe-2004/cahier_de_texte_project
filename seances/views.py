# views.py (seances)
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Seance, Presence, Objectif
from .forms import SeanceForm, PresenceFormSet, ObjectifFormSet
from cours.models import Cours

@login_required
def liste_seances(request):
    # Récupérer les seances des cours enseignés par l'utilisateur
    seances = Seance.objects.filter(cours__enseignant=request.user).order_by('date')
    return render(request, 'seances/liste_seances.html', {'seances': seances})

@login_required
def planifier_seance(request, cours_id=None):
    cours = None
    if cours_id:
        cours = get_object_or_404(Cours, id=cours_id)
        # Vérifier que l'utilisateur est l'enseignant du cours
        if request.user != cours.enseignant and not request.user.is_superuser:
            messages.error(request, "Vous n'êtes pas autorisé à planifier des séances pour ce cours.")
            return redirect('liste_cours')
    
    if request.method == 'POST':
        form = SeanceForm(request.POST, user=request.user)
        if form.is_valid():
            seance = form.save(commit=False)
            # Calculer la durée automatiquement
            from datetime import datetime
            debut = datetime.combine(seance.date, seance.heure_debut)
            fin = datetime.combine(seance.date, seance.heure_fin)
            duree = (fin - debut).seconds // 3600
            seance.duree = duree
            seance.save()
            
            messages.success(request, 'Séance planifiée avec succès!')
            return redirect('detail_cours', cours_id=seance.cours.id)
    else:
        initial = {}
        if cours:
            initial['cours'] = cours
        form = SeanceForm(user=request.user, initial=initial)
    
    return render(request, 'seances/planifier_seance.html', {
        'form': form,
        'cours': cours
    })