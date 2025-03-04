from rest_framework import permissions

class IsDirectionOrReadOnly(permissions.BasePermission):
    """
    Permission personnalisée pour permettre uniquement à la direction de modifier.
    """

    def has_permission(self, request, view):
        # Autoriser les requêtes en lecture pour tous les utilisateurs authentifiés
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated
        
        # Autoriser l'écriture uniquement pour la direction
        return request.user and (
            request.user.is_directeur_adjoint() or 
            request.user.is_chef_departement() or 
            request.user.is_admin()
        )

class IsEnseignantOrReadOnly(permissions.BasePermission):
    """
    Permission personnalisée pour permettre uniquement aux enseignants de modifier.
    """

    def has_permission(self, request, view):
        # Autoriser les requêtes en lecture pour tous les utilisateurs authentifiés
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated
        
        # Autoriser l'écriture uniquement pour les enseignants
        return request.user and (
            request.user.is_enseignant() or 
            request.user.is_directeur_adjoint() or 
            request.user.is_chef_departement() or 
            request.user.is_admin()
        )

    def has_object_permission(self, request, view, obj):
        # Autoriser les requêtes en lecture pour tous les utilisateurs authentifiés
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Autoriser l'écriture uniquement pour l'enseignant associé à l'objet
        # ou pour la direction
        return (
            request.user == obj.enseignant or
            request.user.is_directeur_adjoint() or 
            request.user.is_chef_departement() or 
            request.user.is_admin()
        ) 