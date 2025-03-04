from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Formation, Cours
from .serializers import FormationSerializer, CoursSerializer
from accounts.permissions import IsDirectionOrReadOnly

class FormationViewSet(viewsets.ModelViewSet):
    queryset = Formation.objects.all()
    serializer_class = FormationSerializer
    permission_classes = [permissions.IsAuthenticated, IsDirectionOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(responsable=self.request.user)

    @action(detail=True, methods=['post'])
    def soumettre(self, request, pk=None):
        formation = self.get_object()
        if formation.statut == 'brouillon':
            formation.statut = 'soumis'
            formation.save()
            return Response({'status': 'formation soumise'})
        return Response(
            {'error': 'La formation ne peut pas être soumise'},
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(detail=True, methods=['post'])
    def valider(self, request, pk=None):
        formation = self.get_object()
        if formation.statut == 'soumis':
            formation.statut = 'valide'
            formation.save()
            return Response({'status': 'formation validée'})
        return Response(
            {'error': 'La formation ne peut pas être validée'},
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(detail=True, methods=['post'])
    def rejeter(self, request, pk=None):
        formation = self.get_object()
        if formation.statut == 'soumis':
            formation.statut = 'rejete'
            formation.save()
            return Response({'status': 'formation rejetée'})
        return Response(
            {'error': 'La formation ne peut pas être rejetée'},
            status=status.HTTP_400_BAD_REQUEST
        )

class CoursViewSet(viewsets.ModelViewSet):
    queryset = Cours.objects.all()
    serializer_class = CoursSerializer
    permission_classes = [permissions.IsAuthenticated, IsDirectionOrReadOnly]

    def get_queryset(self):
        queryset = Cours.objects.all()
        formation_id = self.request.query_params.get('formation', None)
        if formation_id is not None:
            queryset = queryset.filter(formation_id=formation_id)
        return queryset

    @action(detail=True, methods=['post'])
    def affecter_enseignant(self, request, pk=None):
        cours = self.get_object()
        enseignant_id = request.data.get('enseignant_id')
        if not enseignant_id:
            return Response(
                {'error': 'enseignant_id est requis'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            cours.enseignant_id = enseignant_id
            cours.save()
            serializer = self.get_serializer(cours)
            return Response(serializer.data)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            ) 