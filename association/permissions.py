from rest_framework import permissions

# class IsAuthenticatedUserOrNetmagicsAdmin(permissions.BasePermission):
#     def has_permission(self, request, view):
#         if request.user and request.user.is_authenticated:
#             return True
#         return hasattr(request.user, 'netmagicsadmin')


class IsAuthenticatedNetmagicsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        print("Net magics admin")
        if not request.user.is_authenticated:
            print('not autheticated')
            return False
        if  request.user.netmagicsadmin_set.exists():
            print('admin exists')
            return True
        else:
            print('admin is not exists')
            return False
    
    

class IsAuthenticatedAssociationAdmin(permissions.BasePermission):
    def  has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        # return hasattr(request.user, "associationsuperadmin") 
        return request.user.associationsuperadmin_set.exists()



class IsAuthenticatedRegistrar(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.registrar_set.exists()


class DeleteIsAuthenticatedNetmagicsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        # return hasattr(request.user, "netmagicsadmin") and request.user.netmagicsadmin.is_owner
        return request.user.netmagicsadmin_set.filter(is_owner=True).exists()


class DeleteIsAuthenticatedAssociationAdmin(permissions.BasePermission):
    def  has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.associationsuperadmin_set.filter(is_owner = True).exists()



