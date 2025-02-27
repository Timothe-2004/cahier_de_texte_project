# cours/urls.py
from django.urls import path
from . import views  # Assurez-vous que views est importé correctement

urlpatterns = [
    path('', views.liste_cours, name='liste_cours'),
    path('<int:cours_id>/', views.detail_cours, name='detail_cours'),
    path('<int:cours_id>/cahier-texte/', views.cahier_texte, name='cahier_texte'),
    path('ajouter/', views.ajouter_cours, name='ajouter_cours'),  # Vérifiez cette ligne
]
