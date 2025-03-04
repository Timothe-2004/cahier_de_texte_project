from rest_framework import serializers
from .models import Seance, Presence, Objectif
from formations.serializers import CoursSerializer
from accounts.serializers import UserSerializer

class ObjectifSerializer(serializers.ModelSerializer):
    class Meta:
        model = Objectif
        fields = ['id', 'description', 'atteint']

class PresenceSerializer(serializers.ModelSerializer):
    etudiant = UserSerializer(read_only=True)
    etudiant_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = Presence
        fields = ['id', 'etudiant', 'etudiant_id', 'present', 'justification']

class SeanceSerializer(serializers.ModelSerializer):
    cours = CoursSerializer(read_only=True)
    cours_id = serializers.IntegerField(write_only=True)
    enseignant = UserSerializer(read_only=True)
    presences = PresenceSerializer(many=True, read_only=True)
    objectifs = ObjectifSerializer(many=True, read_only=True)
    
    class Meta:
        model = Seance
        fields = ['id', 'cours', 'cours_id', 'description', 'date', 'heure_debut',
                 'heure_fin', 'salle', 'enseignant', 'presences', 'objectifs']
        read_only_fields = ['enseignant']

    def validate(self, data):
        """
        Vérifier que l'heure de fin est après l'heure de début
        """
        if data['heure_debut'] >= data['heure_fin']:
            raise serializers.ValidationError(
                "L'heure de fin doit être après l'heure de début"
            )
        return data 