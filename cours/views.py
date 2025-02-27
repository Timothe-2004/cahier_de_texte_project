from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Cours, Ressource
from .forms import CoursForm, RessourceForm
from seances.models import Seance

@login_required
def liste_cours(request):
    cours = Cours.objects.filter(enseignant=request.user)
    return render(request, 'cours/liste_cours.html', {'cours': cours})

@login_required
def detail_cours(request, cours_id):
    cours = get_object_or_404(Cours, id=cours_id)
    ressources = cours.ressources.all()
    seances = cours.seances.all().order_by('date')

    if request.user != cours.enseignant and not request.user.is_superuser:
        messages.error(request, "Vous n'avez pas accès à ce cours.")
        return redirect('liste_cours')

    return render(request, 'cours/detail_cours.html', {
        'cours': cours,
        'ressources': ressources,
        'seances': seances
    })

@login_required
def cahier_texte(request, cours_id):
    cours = get_object_or_404(Cours, id=cours_id)
    seances = cours.seances.all().order_by('date')

    if request.user != cours.enseignant and not request.user.is_superuser:
        messages.error(request, "Vous n'avez pas accès à ce cahier de texte.")
        return redirect('liste_cours')

    return render(request, 'cours/cahier_texte.html', {
        'cours': cours,
        'seances': seances
    })

@login_required
def ajouter_cours(request):
    if request.method == 'POST':
        form = CoursForm(request.POST)
        if form.is_valid():
            cours = form.save(commit=False)
            cours.enseignant = request.user
            cours.save()
            messages.success(request, 'Cours créé avec succès!')
            return redirect('detail_cours', cours_id=cours.id)
    else:
        form = CoursForm()

    return render(request, 'cours/ajouter_cours.html', {'form': form})
