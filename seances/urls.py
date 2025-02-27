# urls.py (seances)
from django.urls import path
from . import views

urlpatterns = [
    path('', views.liste_seances, name='liste_seances'),
    path('planifier/', views.planifier_seance, name='planifier_seance'),
    path('planifier/<int:cours_id>/', views.planifier_seance, name='planifier_seance_cours'),
]
