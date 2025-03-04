from rest_framework import serializers
from formations.models import Cours
from accounts.models import User

class EnseignantSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']

class CoursSerializer(serializers.ModelSerializer):
    enseignant = EnseignantSerializer(read_only=True)
    formation_titre = serializers.CharField(source='formation.titre', read_only=True)
    
    class Meta:
        model = Cours
        fields = ['id', 'titre', 'code', 'description', 'credits', 
                 'volume_horaire', 'enseignant', 'formation', 'formation_titre']
        
    def validate_formation(self, value):
        user = self.context['request'].user
        if not (user.is_directeur_adjoint() or user.is_chef_departement()):
            raise serializers.ValidationError("Vous n'avez pas la permission de modifier la formation.")
        return value 