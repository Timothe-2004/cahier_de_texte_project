# urls.py (formations)
from django.urls import path
from . import views

app_name = 'formations'

urlpatterns = [
    path('', views.liste_formations, name='liste_formations'),
    path('creer/', views.creer_formation, name='creer_formation'),
    path('<int:pk>/', views.detail_formation, name='detail_formation'),
    path('<int:pk>/modifier/', views.modifier_formation, name='modifier_formation'),
    path('<int:pk>/supprimer/', views.supprimer_formation, name='supprimer_formation'),
    path('<int:pk>/soumettre/', views.soumettre_formation, name='soumettre_formation'),
    path('<int:pk>/valider/', views.valider_formation, name='valider_formation'),
    path('<int:pk>/rejeter/', views.rejeter_formation, name='rejeter_formation'),
    
    # URLs pour les cours
    path('<int:formation_pk>/cours/ajouter/', views.ajouter_cours, name='ajouter_cours'),
    path('<int:formation_pk>/cours/<int:pk>/', views.detail_cours, name='detail_cours'),
    path('<int:formation_pk>/cours/<int:pk>/modifier/', views.modifier_cours, name='modifier_cours'),
    path('<int:formation_pk>/cours/<int:pk>/supprimer/', views.supprimer_cours, name='supprimer_cours'),
]