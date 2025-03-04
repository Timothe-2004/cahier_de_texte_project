# views.py (seances)
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from accounts.decorators import enseignant_required, responsable_classe_required
from .models import Seance, Presence, Objectif
from .forms import SeanceForm, PresenceFormSet, ObjectifFormSet, CahierTexteForm
from formations.models import Cours as FormationCours
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from datetime import datetime, timedelta
import io
from django.utils import timezone

@login_required
def liste_seances(request):
    if request.user.is_responsable_classe():
        # Pour le responsable, montrer les séances passées sans notes
        seances = Seance.objects.filter(
            date__lte=timezone.now().date()
        ).order_by('-date', '-heure_debut')
    elif request.user.is_enseignant():
        # Pour l'enseignant, montrer ses séances
        seances = Seance.objects.filter(
            cours__enseignant=request.user
        ).order_by('-date', '-heure_debut')
    else:
        messages.error(request, "Vous n'avez pas accès à cette page.")
        return redirect('accounts:dashboard')
    
    return render(request, 'seances/liste_seances.html', {'seances': seances})

@responsable_classe_required
def planifier_seance(request, cours_id=None):
    cours = None
    if cours_id:
        cours = get_object_or_404(FormationCours, id=cours_id)
    
    if request.method == 'POST':
        form = SeanceForm(request.POST)
        if form.is_valid():
            seance = form.save(commit=False)
            if cours:
                seance.cours = cours
            
            # Vérifier la disponibilité de la salle
            conflit = Seance.objects.filter(
                date=seance.date,
                salle=seance.salle
            ).filter(
                heure_debut__lt=seance.heure_fin,
                heure_fin__gt=seance.heure_debut
            ).exists()
            
            if conflit:
                messages.error(request, 'La salle est déjà occupée sur ce créneau.')
                return render(request, 'seances/planifier_seance.html', {'form': form, 'cours': cours})
            
            seance.save()
            messages.success(request, 'Séance planifiée avec succès!')
            return redirect('seances:liste_seances')
    else:
        initial = {}
        if cours:
            initial = {
                'cours': cours,
                'description': cours.description  # Utiliser la description du cours comme base
            }
        form = SeanceForm(initial=initial)
    
    return render(request, 'seances/planifier_seance.html', {
        'form': form,
        'cours': cours
    })

@enseignant_required
def creer_seance(request):
    if request.method == 'POST':
        form = SeanceForm(request.POST, user=request.user)
        if form.is_valid():
            seance = form.save()
            messages.success(request, 'Séance créée avec succès')
            return redirect('seances:detail_seance', seance_id=seance.id)
    else:
        form = SeanceForm(user=request.user)
    return render(request, 'seances/form_seance.html', {'form': form})

@responsable_classe_required
def marquer_presence(request, seance_id):
    seance = get_object_or_404(Seance, id=seance_id)
    if request.method == 'POST':
        formset = PresenceFormSet(request.POST, instance=seance)
        if formset.is_valid():
            formset.save()
            messages.success(request, 'Présences enregistrées')
            return redirect('seances:detail_seance', seance_id=seance.id)
    else:
        formset = PresenceFormSet(instance=seance)
    return render(request, 'seances/presences.html', {'formset': formset, 'seance': seance})

@login_required
def detail_seance(request, seance_id):
    seance = get_object_or_404(Seance, id=seance_id)
    
    if not (request.user.is_responsable_classe() or request.user == seance.cours.enseignant):
        messages.error(request, "Vous n'avez pas accès à cette séance.")
        return redirect('seances:liste_seances')
    
    return render(request, 'seances/detail_seance.html', {'seance': seance})

@responsable_classe_required
def modifier_seance(request, seance_id):
    seance = get_object_or_404(Seance, id=seance_id)
    
    if seance.est_passee:
        messages.error(request, "Impossible de modifier une séance passée.")
        return redirect('seances:detail_seance', seance_id=seance.id)
    
    if request.method == 'POST':
        form = SeanceForm(request.POST, instance=seance)
        if form.is_valid():
            form.save()
            messages.success(request, 'Séance modifiée avec succès!')
            return redirect('seances:detail_seance', seance_id=seance.id)
    else:
        form = SeanceForm(instance=seance)
    
    return render(request, 'seances/modifier_seance.html', {'form': form, 'seance': seance})

@responsable_classe_required
def supprimer_seance(request, seance_id):
    seance = get_object_or_404(Seance, id=seance_id)
    
    if seance.est_passee:
        messages.error(request, "Impossible de supprimer une séance passée.")
        return redirect('seances:detail_seance', seance_id=seance.id)
    
    if request.method == 'POST':
        seance.delete()
        messages.success(request, 'Séance supprimée avec succès!')
        return redirect('seances:liste_seances')
    
    return redirect('seances:detail_seance', seance_id=seance.id)

@responsable_classe_required
def imprimer_planning(request):
    # Créer un buffer pour le PDF
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # Titre
    p.setFont("Helvetica-Bold", 16)
    p.drawString(2*cm, height-2*cm, "Planning des Séances")
    p.setFont("Helvetica", 10)
    p.drawString(2*cm, height-2.7*cm, f"Généré le {datetime.now().strftime('%d/%m/%Y')}")

    # En-tête du tableau
    headers = ["Date", "Horaire", "Cours", "Enseignant", "Salle"]
    x_positions = [2*cm, 5*cm, 8*cm, 13*cm, 17*cm]
    y = height - 4*cm

    p.setFont("Helvetica-Bold", 10)
    for header, x in zip(headers, x_positions):
        p.drawString(x, y, header)

    # Lignes du tableau
    p.setFont("Helvetica", 10)
    y -= 0.7*cm
    
    seances = Seance.objects.filter(
        date__gte=datetime.now().date()
    ).order_by('date', 'heure_debut')

    for seance in seances:
        # Vérifier si on a besoin d'une nouvelle page
        if y < 2*cm:
            p.showPage()
            y = height - 4*cm
            # Répéter l'en-tête
            p.setFont("Helvetica-Bold", 10)
            for header, x in zip(headers, x_positions):
                p.drawString(x, y, header)
            p.setFont("Helvetica", 10)
            y -= 0.7*cm

        p.drawString(x_positions[0], y, seance.date.strftime('%d/%m/%Y'))
        p.drawString(x_positions[1], y, f"{seance.heure_debut.strftime('%H:%M')} - {seance.heure_fin.strftime('%H:%M')}")
        p.drawString(x_positions[2], y, seance.cours.titre[:25])
        p.drawString(x_positions[3], y, seance.cours.enseignant.get_full_name())
        p.drawString(x_positions[4], y, seance.salle)
        
        y -= 0.5*cm

    p.showPage()
    p.save()

    buffer.seek(0)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="planning_seances_{datetime.now().strftime("%Y%m%d")}.pdf"'
    response.write(buffer.getvalue())
    buffer.close()

    return response

@responsable_classe_required
def remplir_cahier(request, seance_id=None):
    seance = None if seance_id is None else get_object_or_404(Seance, id=seance_id)
    
    if request.method == 'POST':
        form = CahierTexteForm(request.POST, instance=seance)
        if form.is_valid():
            # Récupérer l'enseignant sélectionné
            enseignant = form.cleaned_data['enseignant']
            
            # Créer ou mettre à jour la séance
            seance = form.save(commit=False)
            
            # Mettre à jour le cours avec l'enseignant sélectionné
            cours = seance.cours
            cours.enseignant = enseignant
            cours.save()
            
            seance.save()
            messages.success(request, 'Cahier de texte rempli avec succès!')
            return redirect('seances:liste_seances')
    else:
        form = CahierTexteForm(instance=seance)
    
    return render(request, 'seances/remplir_cahier.html', {
        'form': form,
        'seance': seance
    })