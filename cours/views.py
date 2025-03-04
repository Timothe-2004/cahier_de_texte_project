from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from accounts.decorators import direction_required, enseignant_required
from formations.models import Cours, Formation
from .models import Ressource
from .forms import RessourceForm, CoursForm
from seances.models import Seance
from django.contrib.auth import get_user_model
from django.http import HttpResponse
import csv
from datetime import datetime

User = get_user_model()

@login_required
def liste_cours(request):
    if request.user.is_directeur_adjoint() or request.user.is_chef_departement():
        cours = Cours.objects.all()
    elif request.user.is_enseignant():
        cours = Cours.objects.filter(enseignant=request.user)
    else:
        messages.error(request, "Vous n'avez pas accès à cette page.")
        return redirect('accounts:dashboard')
    
    return render(request, 'cours/liste_cours.html', {'cours': cours})

@login_required
def detail_cours(request, pk):
    cours = get_object_or_404(Cours, pk=pk)
    ressources = Ressource.objects.filter(seance__cours=cours)
    seances = cours.seances.all().order_by('date')

    if not (request.user == cours.enseignant or request.user.is_superuser or 
            request.user.is_directeur_adjoint() or request.user.is_chef_departement()):
        messages.error(request, "Vous n'avez pas accès à ce cours.")
        return redirect('cours:liste_cours')

    return render(request, 'cours/detail_cours.html', {
        'cours': cours,
        'ressources': ressources,
        'seances': seances
    })

@login_required
def cahier_texte(request, cours_id):
    cours = get_object_or_404(Cours, id=cours_id)
    seances = cours.seances.all().order_by('date')

    if not (request.user == cours.enseignant or request.user.is_superuser or 
            request.user.is_directeur_adjoint() or request.user.is_chef_departement()):
        messages.error(request, "Vous n'avez pas accès à ce cahier de texte.")
        return redirect('cours:liste_cours')

    return render(request, 'cours/cahier_texte.html', {
        'cours': cours,
        'seances': seances
    })

@direction_required
def ajouter_cours(request):
    if request.method == 'POST':
        form = CoursForm(request.POST)
        if form.is_valid():
            cours = form.save(commit=False)
            cours.enseignant = request.user
            cours.save()
            messages.success(request, 'Cours créé avec succès!')
            return redirect('cours:detail_cours', pk=cours.id)
    else:
        form = CoursForm()

    return render(request, 'cours/ajouter_cours.html', {'form': form})

@enseignant_required
def mes_cours(request):
    cours = Cours.objects.filter(enseignant=request.user)
    return render(request, 'cours/liste_cours.html', {'cours': cours})

@direction_required
def affecter_cours(request, cours_id):
    cours = get_object_or_404(Cours, id=cours_id)
    if request.method == 'POST':
        enseignant_id = request.POST.get('enseignant')
        if enseignant_id:
            enseignant = get_object_or_404(User, id=enseignant_id, role='enseignant')
            cours.enseignant = enseignant
            cours.save()
            messages.success(request, f'Le cours {cours.titre} a été affecté à {enseignant.get_full_name()}')
        return redirect('cours:liste_cours')
    
    enseignants = User.objects.filter(role='enseignant')
    return render(request, 'cours/affecter_cours.html', {
        'cours': cours,
        'enseignants': enseignants
    })

@direction_required
def creer_cours(request):
    if request.method == 'POST':
        form = CoursForm(request.POST)
        if form.is_valid():
            cours = form.save()
            messages.success(request, 'Cours créé avec succès')
            return redirect('cours:detail_cours', pk=cours.id)
    else:
        form = CoursForm()
    return render(request, 'cours/form_cours.html', {'form': form})

@login_required
def ajouter_ressource(request, cours_id):
    cours = get_object_or_404(Cours, id=cours_id)
    
    if not (request.user == cours.enseignant or request.user.is_superuser or 
            request.user.is_directeur_adjoint() or request.user.is_chef_departement()):
        messages.error(request, "Vous n'avez pas l'autorisation d'ajouter des ressources à ce cours.")
        return redirect('cours:detail_cours', pk=cours.id)
    
    if request.method == 'POST':
        form = RessourceForm(request.POST, request.FILES)
        if form.is_valid():
            ressource = form.save(commit=False)
            ressource.seance = cours.seances.first()  # À adapter selon vos besoins
            ressource.save()
            messages.success(request, 'Ressource ajoutée avec succès')
            return redirect('cours:detail_cours', pk=cours.id)
    else:
        form = RessourceForm()
    
    return render(request, 'cours/ajouter_ressource.html', {
        'form': form,
        'cours': cours
    })

@direction_required
def recapitulatif_cours(request):
    enseignants = User.objects.filter(role='enseignant')
    data = []
    for enseignant in enseignants:
        cours = Cours.objects.filter(enseignant=enseignant)
        volume_total = sum(c.volume_horaire for c in cours)
        data.append({
            'user': enseignant,
            'cours': cours,
            'volume_total': volume_total
        })
    
    context = {
        'enseignants': data
    }
    return render(request, 'cours/recapitulatif.html', context)
