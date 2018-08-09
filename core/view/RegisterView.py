import re

from django.views.generic import TemplateView
from django.views.decorators.cache import never_cache
from django.http import HttpResponse

from core.models import User
from core.security.AuthenicationManager import AuthenticationManager


class RegisterView(TemplateView):

    def __init__(self):
        self.authenticationManager = AuthenticationManager()

    @never_cache
    def post(self, request, *args, **kwargs):
        if request.method != 'POST':
            return HttpResponse('Use POST method', status=400)

        try:
            name = request.POST['name']
            password = request.POST['password']
            email = request.POST['email']
        except KeyError:
            return HttpResponse('Fill in all fields', status=400)

        if name == '' or password == '' or email == '':
            return HttpResponse('Fill in all fields', status=400)
        if len(password) < 5:
            return HttpResponse('Password should be longer than 5 symbols', status=400)
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return HttpResponse('Email is not valid', status=400)

        same_email_user_amount = User.objects.filter(email=email).count()
        if same_email_user_amount > 0:
            return HttpResponse('User with this email already exists', status=400)

        password_hash = self.authenticationManager.hash_password(password)

        new_user = User(name=name,
                        password=password_hash,
                        email=email)
        new_user.save()

        response = HttpResponse(status=200)

        self.authenticationManager.authenticate_response(response, new_user)

        return response



