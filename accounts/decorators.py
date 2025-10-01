from django.core.exceptions import PermissionDenied
from functools import wraps

def role_required(allowed_roles=[]):
    """
    Decorator that checks if a user has one of the allowed roles.
    If the user is not authenticated or does not have the required role,
    it raises a PermissionDenied exception (403 Forbidden).
    
    Usage: @role_required(allowed_roles=['SEEKER'])
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            # Ensure the user is authenticated first
            if not request.user.is_authenticated:
                raise PermissionDenied

            # Check if the user's role is in the allowed list
            if request.user.role not in allowed_roles:
                raise PermissionDenied
            
            # If all checks pass, execute the original view function
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator

# Create specific decorators from the factory for easy use
seeker_required = role_required(allowed_roles=['SEEKER'])
recruiter_required = role_required(allowed_roles=['RECRUITER'])
