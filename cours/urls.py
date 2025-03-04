from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from . import api

app_name = 'cours'

router = DefaultRouter()
router.register(r'api/cours', api.CoursViewSet, basename='cours-api')

urlpatterns = [
    path('', views.liste_cours, name='liste_cours'),
    path('<int:pk>/', views.detail_cours, name='detail_cours'),
    path('ajouter/', views.ajouter_cours, name='ajouter_cours'),
    path('mes-cours/', views.mes_cours, name='mes_cours'),
    path('<int:cours_id>/affecter/', views.affecter_cours, name='affecter_cours'),
    path('<int:cours_id>/cahier-texte/', views.cahier_texte, name='cahier_texte'),
    path('creer/', views.creer_cours, name='creer_cours'),
    path('<int:cours_id>/ressource/ajouter/', views.ajouter_ressource, name='ajouter_ressource'),
    path('recapitulatif/', views.recapitulatif_cours, name='recapitulatif_cours'),
    path('', include(router.urls)),
]