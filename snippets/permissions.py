# snippets/permissions.py
from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Allow read-only access for everyone,
    but write access only for the owner.
    """

    def has_object_permission(self, request, view, obj):

        # ყველას შეუძლია read request
        if request.method in permissions.SAFE_METHODS:
            return True

        # write მხოლოდ owner-ს
        return getattr(obj, "owner", None) == request.user