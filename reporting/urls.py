# urls.py (reporting)
from django.urls import path
from . import views

urlpatterns = [
    path('statistiques/', views.statistiques, name='statistiques'),
]
