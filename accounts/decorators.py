from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied
from functools import wraps

def admin_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_admin():
            return view_func(request, *args, **kwargs)
        raise PermissionDenied
    return wrapper

def direction_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and (
            request.user.is_directeur_adjoint() or 
            request.user.is_chef_departement() or 
            request.user.is_admin()
        ):
            return view_func(request, *args, **kwargs)
        raise PermissionDenied
    return wrapper

def chef_departement_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and (
            request.user.is_chef_departement() or 
            request.user.is_directeur_adjoint() or 
            request.user.is_admin()
        ):
            return view_func(request, *args, **kwargs)
        raise PermissionDenied
    return wrapper

def enseignant_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_enseignant():
            return view_func(request, *args, **kwargs)
        raise PermissionDenied
    return wrapper

def responsable_classe_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_responsable_classe():
            return view_func(request, *args, **kwargs)
        raise PermissionDenied
    return wrapper 