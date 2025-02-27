# urls.py (formations)
from django.urls import path
from . import views

urlpatterns = [
    path('', views.liste_formations, name='liste_formations'),
    path('<int:formation_id>/', views.detail_formation, name='detail_formation'),
    path('ajouter/', views.ajouter_formation, name='ajouter_formation'),
]