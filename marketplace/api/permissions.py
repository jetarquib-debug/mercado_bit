from rest_framework import permissions


class IsObjectOwnerOrReadOnly(permissions.BasePermission):
    """Permiso de objeto genérico: solo el propietario puede modificar, otros solo lectura.

    Intenta resolver el usuario propietario revisando atributos comunes:
    - `usuario`, `user`, `owner` (cuando apuntan a la instancia de usuario)
    - `tienda` -> su atributo `usuario`
    - `carrito` -> su atributo `usuario`
    """

    def has_permission(self, request, view):
        # Permitir acceso de lista/creación si está autenticado (o lectura para anónimos)
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Lectura siempre permitida
        if request.method in permissions.SAFE_METHODS:
            return True

        # Superusers pueden todo
        if request.user and request.user.is_superuser:
            return True

        owner = self._resolve_owner_user(obj)
        if owner is None:
            return False
        try:
            return bool(request.user and owner.pk == request.user.pk)
        except Exception:
            return False

    def _resolve_owner_user(self, obj):
        # Revisa atributos comunes
        for attr in ('usuario', 'user', 'owner'):
            if hasattr(obj, attr):
                candidate = getattr(obj, attr)
                if candidate is not None:
                    return candidate

        # Si el objeto tiene tienda, tomar tienda.usuario
        if hasattr(obj, 'tienda'):
            tienda = getattr(obj, 'tienda')
            if tienda is not None and hasattr(tienda, 'usuario'):
                return getattr(tienda, 'usuario')

        # Si el objeto tiene carrito, tomar carrito.usuario
        if hasattr(obj, 'carrito'):
            carrito = getattr(obj, 'carrito')
            if carrito is not None and hasattr(carrito, 'usuario'):
                return getattr(carrito, 'usuario')

        return None
