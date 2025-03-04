from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from formations.models import Cours
from .serializers import CoursSerializer
from django.shortcuts import get_object_or_404
from accounts.models import User

class IsDirecteurOrChefDepartement(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_directeur_adjoint() or 
            request.user.is_chef_departement()
        )

class CoursViewSet(viewsets.ModelViewSet):
    serializer_class = CoursSerializer
    
    def get_queryset(self):
        user = self.request.user
        if user.is_directeur_adjoint() or user.is_chef_departement():
            return Cours.objects.all()
        elif user.is_enseignant():
            return Cours.objects.filter(enseignant=user)
        return Cours.objects.none()

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsDirecteurOrChefDepartement]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    @action(detail=True, methods=['post'])
    def affecter_enseignant(self, request, pk=None):
        cours = self.get_object()
        enseignant_id = request.data.get('enseignant_id')
        
        if not enseignant_id:
            return Response({'error': 'ID enseignant requis'}, status=400)
            
        enseignant = get_object_or_404(User, id=enseignant_id, role='enseignant')
        cours.enseignant = enseignant
        cours.save()
        
        return Response({'message': f'Cours affecté à {enseignant.get_full_name()}'})

    @action(detail=False, methods=['get'])
    def recapitulatif(self, request):
        if not (request.user.is_directeur_adjoint() or request.user.is_chef_departement()):
            return Response({'error': 'Permission refusée'}, status=403)
            
        enseignants = User.objects.filter(role='enseignant')
        data = []
        
        for enseignant in enseignants:
            cours = Cours.objects.filter(enseignant=enseignant)
            data.append({
                'enseignant': {
                    'id': enseignant.id,
                    'nom': enseignant.get_full_name(),
                },
                'cours': CoursSerializer(cours, many=True).data
            })
            
        return Response(data) 