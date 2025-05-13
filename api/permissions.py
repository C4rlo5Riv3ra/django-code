from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Permiso que permite solo a administradores editar.
    Los usuarios no autenticados o no administradores solo pueden ver.
    """
    def has_permission(self, request, view):
        # Permitir peticiones GET, HEAD, OPTIONS a cualquiera
        if request.method in permissions.SAFE_METHODS:
            return True
        # Solo permitir escritura si el usuario es staff/admin
        return request.user and request.user.is_staff

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Permiso que permite solo a propietarios de un objeto editarlo.
    """
    def has_object_permission(self, request, view, obj):
    # Permitir peticiones de solo lectura a cualquiera
        if request.method in permissions.SAFE_METHODS:
            return True
        # permitir edición al propietario del objeto
        # Ajustar según el modelo (aquí suponemos que tiene campo creado_por)
        return obj.creado_por == request.user