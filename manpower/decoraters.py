from django.http import HttpResponse
from django.shortcuts import redirect, HttpResponseRedirect


def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):

            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name

            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponseRedirect('/uaaccess/')
        return wrapper_func
    return decorator


def admin_only(view_func):
    def wrapper_func(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name
        if group == 'supervisor':
            return redirect('super_dashboard')
        if group == 'admin':
            return view_func(request, *args, **kwargs)
        if group == 'master':
            return view_func(request, *args, **kwargs)
    return wrapper_func
