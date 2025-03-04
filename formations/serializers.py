from rest_framework import serializers
from .models import Formation, Cours
from accounts.serializers import UserSerializer

class CoursSerializer(serializers.ModelSerializer):
    enseignant = UserSerializer(read_only=True)
    enseignant_id = serializers.IntegerField(write_only=True, required=False)
    
    class Meta:
        model = Cours
        fields = ['id', 'code', 'titre', 'description', 'formation', 'enseignant', 
                 'enseignant_id', 'volume_horaire', 'created_at', 'updated_at']

class FormationSerializer(serializers.ModelSerializer):
    cours = CoursSerializer(many=True, read_only=True)
    responsable = UserSerializer(read_only=True)
    
    class Meta:
        model = Formation
        fields = ['id', 'code', 'titre', 'description', 'niveau', 'departement',
                 'responsable', 'cours', 'statut', 'created_at', 'updated_at']
        read_only_fields = ['statut'] 