from rest_framework import permissions

class IsAuthenticatedAdvocate(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.advocate_set.exists()
