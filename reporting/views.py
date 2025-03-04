# views.py (reporting)
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Count, Sum, Avg
from cours.models import Cours
from seances.models import Seance, Presence
from formations.models import Formation, Module
from django.http import HttpResponse
from django.template.loader import render_to_string
import weasyprint
from accounts.decorators import directeur_adjoint_required

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

@directeur_adjoint_required
def rapport_enseignant(request, enseignant_id):
    cours = Cours.objects.filter(enseignant_id=enseignant_id)
    seances = Seance.objects.filter(cours__in=cours)
    
    html = render_to_string('reporting/rapport_enseignant.html', {
        'cours': cours,
        'seances': seances,
    })
    
    pdf = weasyprint.HTML(string=html).write_pdf()
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="rapport_enseignant_{enseignant_id}.pdf"'
    return response

@login_required
def bilan_formation(request, formation_id):
    from formations.models import Formation
    formation = Formation.objects.get(id=formation_id)
    cours = Cours.objects.filter(module__formation=formation)
    
    html = render_to_string('reporting/bilan_formation.html', {
        'formation': formation,
        'cours': cours,
    })
    
    pdf = weasyprint.HTML(string=html).write_pdf()
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="bilan_formation_{formation_id}.pdf"'
    return response