from django.urls import path
from . import views

app_name = 'seances'

urlpatterns = [
    path('', views.liste_seances, name='liste_seances'),
    path('<int:seance_id>/', views.detail_seance, name='detail_seance'),
    path('<int:seance_id>/remplir-cahier/', views.remplir_cahier, name='remplir_cahier'),
    path('planifier/', views.planifier_seance, name='planifier_seance'),
    path('planifier/<int:cours_id>/', views.planifier_seance, name='planifier_seance_cours'),
    path('<int:seance_id>/modifier/', views.modifier_seance, name='modifier_seance'),
    path('<int:seance_id>/supprimer/', views.supprimer_seance, name='supprimer_seance'),
    path('imprimer-planning/', views.imprimer_planning, name='imprimer_planning'),
]