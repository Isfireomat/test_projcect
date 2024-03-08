from rest_framework.exceptions import AuthenticationFailed
from rest_framework.views import exception_handler
from django.shortcuts import redirect
from rest_framework.authentication import exceptions as auth_exceptions
from typing import Union

def redirect_to_log(exec:Exception, data:dict) -> Union[redirect, None]:
    if isinstance(exec, AuthenticationFailed) or isinstance(exec, auth_exceptions.NotAuthenticated): return redirect('login')
    if auth_exceptions.bad_request: return redirect('register')
    return exception_handler(exec, data)