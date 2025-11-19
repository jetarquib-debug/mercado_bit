from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """Object-level permission to only allow owners of an object to edit it.

    Assumes the model instance has an `usuario` or `owner` attribute pointing to a user.
    """

    def has_permission(self, request, view):
        # Allow read-only methods for any request
        if request.method in permissions.SAFE_METHODS:
            return True
        # For unsafe methods, the view-level check will allow and object-level will enforce
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True

        user = request.user
        # try sensible owner fields
        owner = getattr(obj, 'usuario', None) or getattr(obj, 'owner', None) or getattr(obj, 'usuario_propietario', None)
        if owner is None:
            # fallback: allow only staff to modify if no owner field
            return user and user.is_staff
        return owner == user or (user and user.is_staff)


class IsAuthenticatedOrReadOnly(permissions.IsAuthenticatedOrReadOnly):
    """Alias to keep naming consistent; uses DRF's implementation."""
    pass


class DjangoModelPermissionsOrAnonReadOnly(permissions.DjangoModelPermissions):
    """Like DjangoModelPermissions but allow anonymous read-only access.

    This keeps standard model perms for unsafe methods.
    """

    def has_permission(self, request, view):
        # Allow read-only requests for any user (including anonymous)
        if request.method in permissions.SAFE_METHODS:
            return True
        return super().has_permission(request, view)
