"""API app permissions"""
from rest_framework import permissions


class IsAdminUserOrReadOnly(permissions.BasePermission):
    """Admin rights or readonly."""

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.is_admin_or_super_user
            or request.method in permissions.SAFE_METHODS
        )


class IsAdminOrModeratorOrAuthor(permissions.BasePermission):
    """"Проверка прав для отзывов и комментариев."""
    message = 'Нужны права администратора, модератора или автора'

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user == obj.author
            or request.user.is_moderator
            or request.user.is_admin_or_super_user
        )


class CustomUserIsAdminBasePermission(permissions.BasePermission):
    """Allow access only to admin user or superuser."""
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.is_admin_or_super_user
