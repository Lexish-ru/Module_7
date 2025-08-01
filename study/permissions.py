from rest_framework import permissions


class IsModerator(permissions.BasePermission):
    """
    Доступ только для модераторов.
    """
    def has_permission(self, request, view):
        return request.user and request.user.groups.filter(name='moderators').exists()


class IsOwnerOrModerator(permissions.BasePermission):
    """
    Доступ только владельцу объекта или модератору.
    """
    def has_object_permission(self, request, view, obj):
        return (obj.owner == request.user) or request.user.groups.filter(name='moderators').exists()
