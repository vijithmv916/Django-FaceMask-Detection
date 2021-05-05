from django.http import HttpResponse 
from django.shortcuts import redirect

def allowed_users(allowed_roles=[]):
    def decorator(viewfunc):
        def wrapperfunc(request, *args, **kwargs):

            group = None
            
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            if group in allowed_roles:
                return viewfunc(request, *args, **kwargs)
            else :
                return HttpResponse('you are not authority')

        return wrapperfunc
    return decorator