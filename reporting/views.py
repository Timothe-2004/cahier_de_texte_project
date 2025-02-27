# views.py (reporting)
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Count, Sum, Avg
from cours.models import Cours
from seances.models import Seance, Presence
from formations.models import Formation, Module

def is_admin_or_chef(user):
    return user.is_superuser or hasattr(user, 'departement_dirige')

@login_required
@user_passes_test(is_admin_or_chef)
def statistiques(request):
    # Statistiques générales
    total_formations = Formation.objects.count()
    total_modules = Module.objects.count()
    total_cours = Cours.objects.count()
    total_seances = Seance.objects.count()
    
    # Statistiques de progression
    cours_stats = Cours.objects.annotate(
        nb_seances=Count('seances'),
        heures_realisees=Sum('seances__duree')
    )
    
    # Taux de présence
    presences = Presence.objects.filter(present=True).count()
    total_presences = Presence.objects.count()
    taux_presence = (presences / total_presences * 100) if total_presences > 0 else 0
    
    # Formations par département
    formations_par_departement = Formation.objects.values('departement__nom').annotate(
        count=Count('id')
    ).order_by('departement__nom')
    
    context = {
        'total_formations': total_formations,
        'total_modules': total_modules,
        'total_cours': total_cours,
        'total_seances': total_seances,
        'cours_stats': cours_stats,
        'taux_presence': taux_presence,
        'formations_par_departement': formations_par_departement,
    }
    
    return render(request, 'reporting/statistiques.html', context)