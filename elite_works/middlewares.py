from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponseRedirect
from django.urls import resolve, reverse


class login_register_middleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        url_name = resolve(request.path_info).url_name
        if (url_name == 'login') and request.user.is_authenticated:
            response = HttpResponseRedirect('/')
        else:
            response = self.get_response(request)

        return response


def login_required_middleware(get_response):
    """
        Require user to be logged in for all views. 
    """
    exceptions = {'/login/'}

    def middleware(request):
        if request.path in exceptions:
            return get_response(request)
        return login_required(get_response, login_url=reverse('login'))(request)
    return middleware
