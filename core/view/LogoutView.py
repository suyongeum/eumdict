from datetime import datetime

from django.views.generic import TemplateView
from django.views.decorators.cache import never_cache
from django.http import HttpResponse

from core.security.CookieManager import CookieManager


class LogoutView(TemplateView):

    def __init__(self):
        self.cookieManager = CookieManager()  # TODO: move to settings
        self.auth_token_cookie_name = 'auth_token'

    @never_cache
    def get(self, request, *args, **kwargs):
        now = str(datetime.now())
        response = HttpResponse(now, status=200)
        self.cookieManager.delete_cookie(response, self.auth_token_cookie_name)
        return response


