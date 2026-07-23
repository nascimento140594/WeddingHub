from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    """
    Permite acesso apenas ao proprietário do recurso.
    """

    def has_object_permission(self, request, view, obj):
        if hasattr(obj, "user"):
            return obj.user == request.user

        if hasattr(obj, "wedding"):
            return obj.wedding.user == request.user

        if hasattr(obj, "gift"):
            return obj.gift.wedding.user == request.user

        return False
