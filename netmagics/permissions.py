

def can_impersonate(request, user_id):
    if request.user.netmagicsadmin_set.exists():
        print('')
        return True
    return False