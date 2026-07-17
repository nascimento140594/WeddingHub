from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    """
    Permite acesso apenas ao próprio usuário.
    """

    def has_object_permission(self, request, view, obj):
        return obj == request.user
