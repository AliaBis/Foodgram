from rest_framework import permissions


class IsAdminAuthorOrReadOnly(permissions.BasePermission):
    """Доступ для админа и для неавтор.пользователей."""

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and (
            request.user.is_admin
            or obj.author == request.user
        )


class IsAdmin(permissions.BasePermission):
    """Доступ только для админа."""

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and request.user.is_admin
        )


class IsAdminOrReadOnly(permissions.BasePermission):
    """Доступ только для адмиа или на чтение
    для неавторизованных пользователей."""

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or (request.user.is_authenticated
                    and request.user.is_admin))
