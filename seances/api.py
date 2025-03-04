from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Seance, Presence, Objectif
from .serializers import SeanceSerializer, PresenceSerializer, ObjectifSerializer
from accounts.permissions import IsDirectionOrReadOnly, IsEnseignantOrReadOnly

class SeanceViewSet(viewsets.ModelViewSet):
    queryset = Seance.objects.all()
    serializer_class = SeanceSerializer
    permission_classes = [permissions.IsAuthenticated, IsDirectionOrReadOnly]

    def get_queryset(self):
        queryset = Seance.objects.all()
        cours_id = self.request.query_params.get('cours', None)
        if cours_id is not None:
            queryset = queryset.filter(cours_id=cours_id)
        
        # Filtrer par date
        date_debut = self.request.query_params.get('date_debut', None)
        date_fin = self.request.query_params.get('date_fin', None)
        if date_debut is not None:
            queryset = queryset.filter(date__gte=date_debut)
        if date_fin is not None:
            queryset = queryset.filter(date__lte=date_fin)
        
        return queryset.order_by('date', 'heure_debut')

    def perform_create(self, serializer):
        serializer.save(enseignant=self.request.user)

class PresenceViewSet(viewsets.ModelViewSet):
    queryset = Presence.objects.all()
    serializer_class = PresenceSerializer
    permission_classes = [permissions.IsAuthenticated, IsEnseignantOrReadOnly]

    def get_queryset(self):
        queryset = Presence.objects.all()
        seance_id = self.request.query_params.get('seance', None)
        if seance_id is not None:
            queryset = queryset.filter(seance_id=seance_id)
        return queryset

    @action(detail=False, methods=['post'])
    def marquer_presences(self, request):
        presences_data = request.data
        if not isinstance(presences_data, list):
            return Response(
                {'error': 'Les données doivent être une liste de présences'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        created_presences = []
        for presence_data in presences_data:
            serializer = self.get_serializer(data=presence_data)
            if serializer.is_valid():
                serializer.save()
                created_presences.append(serializer.data)
            else:
                return Response(
                    serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        return Response(created_presences, status=status.HTTP_201_CREATED)

class ObjectifViewSet(viewsets.ModelViewSet):
    queryset = Objectif.objects.all()
    serializer_class = ObjectifSerializer
    permission_classes = [permissions.IsAuthenticated, IsEnseignantOrReadOnly]

    def get_queryset(self):
        queryset = Objectif.objects.all()
        seance_id = self.request.query_params.get('seance', None)
        if seance_id is not None:
            queryset = queryset.filter(seance_id=seance_id)
        return queryset 