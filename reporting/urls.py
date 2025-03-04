from django.urls import path
from . import views

app_name = 'reporting'

urlpatterns = [
    path('statistiques/', views.statistiques, name='statistiques'),
    path('enseignant/<int:enseignant_id>/', views.rapport_enseignant, name='rapport_enseignant'),
    path('formation/<int:formation_id>/', views.bilan_formation, name='bilan_formation'),
]