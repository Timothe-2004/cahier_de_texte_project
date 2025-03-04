# views.py (formations)
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from .models import Formation, Cours
from .forms import FormationForm, CoursForm
from accounts.decorators import direction_required

@login_required
def liste_formations(request):
    """Liste toutes les formations."""
    formations = Formation.objects.all()
    return render(request, 'formations/liste_formations.html', {'formations': formations})

@login_required
def detail_formation(request, pk):
    """Affiche les détails d'une formation et ses cours."""
    formation = get_object_or_404(Formation, pk=pk)
    cours_list = formation.cours.all().order_by('code')
    return render(request, 'formations/detail_formation.html', {
        'formation': formation,
        'cours_list': cours_list
    })

@direction_required
def creer_formation(request):
    """Crée une nouvelle formation."""
    if request.method == 'POST':
        form = FormationForm(request.POST)
        if form.is_valid():
            formation = form.save(commit=False)
            formation.responsable = request.user
            formation.save()
            messages.success(request, 'Formation créée avec succès.')
            return redirect('formations:detail_formation', pk=formation.pk)
    else:
        form = FormationForm()
    return render(request, 'formations/form.html', {
        'form': form,
        'titre': 'Nouvelle formation'
    })

@direction_required
def modifier_formation(request, pk):
    """Modifie une formation existante."""
    formation = get_object_or_404(Formation, pk=pk)
    if request.method == 'POST':
        form = FormationForm(request.POST, instance=formation)
        if form.is_valid():
            form.save()
            messages.success(request, 'Formation modifiée avec succès.')
            return redirect('formations:detail_formation', pk=pk)
    else:
        form = FormationForm(instance=formation)
    return render(request, 'formations/form.html', {
        'form': form,
        'titre': 'Modifier la formation'
    })

@direction_required
def supprimer_formation(request, pk):
    """Supprime une formation."""
    formation = get_object_or_404(Formation, pk=pk)
    if request.method == 'POST':
        formation.delete()
        messages.success(request, 'Formation supprimée avec succès.')
        return redirect('formations:liste_formations')
    return render(request, 'formations/confirmer_suppression.html', {
        'objet': formation,
        'titre': 'Supprimer la formation'
    })

@direction_required
def soumettre_formation(request, pk):
    """Soumet une formation pour validation."""
    formation = get_object_or_404(Formation, pk=pk)
    if formation.statut == 'brouillon':
        formation.statut = 'soumis'
        formation.save()
        messages.success(request, 'Formation soumise pour validation.')
    return redirect('formations:detail_formation', pk=pk)

@direction_required
def valider_formation(request, pk):
    """Valide une formation soumise."""
    formation = get_object_or_404(Formation, pk=pk)
    if formation.statut == 'soumis':
        formation.statut = 'valide'
        formation.save()
        messages.success(request, 'Formation validée avec succès.')
    return redirect('formations:detail_formation', pk=pk)

@direction_required
def rejeter_formation(request, pk):
    """Rejette une formation soumise."""
    formation = get_object_or_404(Formation, pk=pk)
    if formation.statut == 'soumis':
        formation.statut = 'rejete'
        formation.save()
        messages.success(request, 'Formation rejetée.')
    return redirect('formations:detail_formation', pk=pk)

@direction_required
def ajouter_cours(request, formation_pk):
    """Ajoute un nouveau cours à une formation."""
    formation = get_object_or_404(Formation, pk=formation_pk)
    if request.method == 'POST':
        form = CoursForm(request.POST)
        if form.is_valid():
            cours = form.save(commit=False)
            cours.formation = formation
            cours.save()
            messages.success(request, 'Cours ajouté avec succès.')
            return redirect('formations:detail_formation', pk=formation_pk)
    else:
        form = CoursForm()
    return render(request, 'formations/form_cours.html', {
        'form': form,
        'titre': 'Ajouter un cours',
        'formation': formation
    })

@login_required
def detail_cours(request, formation_pk, pk):
    """Affiche les détails d'un cours."""
    formation = get_object_or_404(Formation, pk=formation_pk)
    cours = get_object_or_404(Cours, pk=pk, formation=formation)
    return render(request, 'formations/detail_cours.html', {
        'cours': cours,
        'formation': formation
    })

@direction_required
def modifier_cours(request, formation_pk, pk):
    """Modifie un cours existant."""
    formation = get_object_or_404(Formation, pk=formation_pk)
    cours = get_object_or_404(Cours, pk=pk, formation=formation)
    if request.method == 'POST':
        form = CoursForm(request.POST, instance=cours)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cours modifié avec succès.')
            return redirect('formations:detail_formation', pk=formation_pk)
    else:
        form = CoursForm(instance=cours)
    return render(request, 'formations/form_cours.html', {
        'form': form,
        'titre': 'Modifier le cours',
        'formation': formation
    })

@direction_required
def supprimer_cours(request, formation_pk, pk):
    """Supprime un cours."""
    formation = get_object_or_404(Formation, pk=formation_pk)
    cours = get_object_or_404(Cours, pk=pk, formation=formation)
    if request.method == 'POST':
        cours.delete()
        messages.success(request, 'Cours supprimé avec succès.')
        return redirect('formations:detail_formation', pk=formation_pk)
    return render(request, 'formations/confirmer_suppression.html', {
        'objet': cours,
        'formation': formation
    })
