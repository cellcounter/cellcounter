from django.http import HttpResponseForbidden
from django.contrib.auth.models import User


def user_is_owner(function):
    def _wrapped_view(request, *args, **kwargs):
        try:
            user = User.objects.get(id=kwargs['pk'])
        except User.DoesNotExist:
            return HttpResponseForbidden()
        if request.user != user:
            return HttpResponseForbidden() 

        return function(request, *args, **kwargs)
    
    return _wrapped_view
