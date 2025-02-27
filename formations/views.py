# views.py (formations)
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Formation, Module, Departement
from .forms import FormationForm, ModuleForm

def is_admin_or_chef(user):
    return user.is_superuser or hasattr(user, 'departement_dirige')

@login_required
def liste_formations(request):
    formations = Formation.objects.all()
    return render(request, 'formations/liste_formations.html', {'formations': formations})

@login_required
def detail_formation(request, formation_id):
    formation = get_object_or_404(Formation, id=formation_id)
    modules = formation.modules.all()
    return render(request, 'formations/detail_formation.html', {
        'formation': formation,
        'modules': modules
    })

@login_required
@user_passes_test(is_admin_or_chef)
def ajouter_formation(request):
    if request.method == 'POST':
        form = FormationForm(request.POST)
        if form.is_valid():
            formation = form.save(commit=False)
            formation.responsable = request.user
            formation.save()
            messages.success(request, 'Formation créée avec succès!')
            return redirect('detail_formation', formation_id=formation.id)
    else:
        form = FormationForm()
    
    return render(request, 'formations/ajouter_formation.html', {'form': form})
