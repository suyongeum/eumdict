from datetime import datetime

from django.views.generic import TemplateView
from django.views.decorators.cache import never_cache
from django.http import HttpResponse

from core.models import User
from core.security.AuthenicationManager import AuthenticationManager

class AuthenticateView(TemplateView):

    def __init__(self):
        self.authenticationManager = AuthenticationManager()

    @never_cache
    def get(self, request, *args, **kwargs):
        email = request.GET.get('email')
        password = request.GET.get('password')

        current_user = User.objects.filter(email=email)

        if len(current_user) == 0:
            return HttpResponse('Incorrect email or password', status=401)

        user = current_user[0]

        password_hash = self.authenticationManager.hash_password(password)

        if password_hash != user.password:
            return HttpResponse('Incorrect email or password', status=401)

        response = HttpResponse(status=200)

        self.authenticationManager.authenticate_response(response, user)

        return response
