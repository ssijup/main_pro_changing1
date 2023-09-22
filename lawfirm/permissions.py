from rest_framework import permissions

class IsAuthenticatedLawfirmAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user and not request.user.is_authenticated:
            return False
        # return hasattr(request.user, "lawfirmadmin")
        return request.user.lawfirmadmin_set.exists()
