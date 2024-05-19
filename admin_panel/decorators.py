from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseForbidden

def admin_required(function):
    """
    Custom decorator to restrict access to admin users only.
    """
    def wrap(request, *args, **kwargs):
        if not request.user.is_superuser:
            return HttpResponseForbidden("You are not authorized to access this page.")
        return function(request, *args, **kwargs)
    return wrap
