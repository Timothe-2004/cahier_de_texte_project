"""
URL configuration for cahier_de_texte project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# urls.py (principal)
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework.routers import DefaultRouter
from formations.api import FormationViewSet, CoursViewSet
from seances.api import SeanceViewSet, PresenceViewSet, ObjectifViewSet

# Création du routeur pour l'API
router = DefaultRouter()
router.register(r'api/formations', FormationViewSet)
router.register(r'api/cours', CoursViewSet)
router.register(r'api/seances', SeanceViewSet)
router.register(r'api/presences', PresenceViewSet)
router.register(r'api/objectifs', ObjectifViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='home.html'), name='accueil'),
    path('accounts/', include('accounts.urls')),
    path('formations/', include('formations.urls', namespace='formations')),
    path('cours/', include('cours.urls', namespace='cours')),
    path('seances/', include('seances.urls', namespace='seances')),
    # Temporairement désactivé en attendant la configuration de WeasyPrint
    # path('reporting/', include('reporting.urls')),
    # URLs de l'API
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
]
