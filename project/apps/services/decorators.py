# =========================================
# Created by Ridwan Renaldi, S.Kom. (rr867)
# =========================================
from django.shortcuts import redirect
from django.contrib import messages

def group_required(*groups):

    def decorator(function):
        def wrapper(request, *args, **kwargs):
            if request.user.groups.filter(name__in=groups).exists() | request.user.is_superuser :
                return function(request, *args, **kwargs)
            else:
                messages.warning(request, 'You Don\'t Have Permission')
                return redirect('authentication:signout')
                
        return wrapper
    return decorator


def isloggedin(url):

    def decorator(function):
        def wrapper(request, *args, **kwargs):
            if request.user.is_authenticated:
                return redirect(url)
            else:
                return function(request, *args, **kwargs)
                
        return wrapper
    return decorator