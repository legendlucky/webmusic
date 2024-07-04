from functools import wraps
from django.http import HttpResponseForbidden

def internal_only(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        # Check for a custom header that indicates an internal request
        if request.META.get('HTTP_INTERNAL_REQUEST') == 'true':
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseForbidden("Forbidden: Direct access is not allowed.")
    return _wrapped_view
