from django.views.generic import TemplateView
from django.views.decorators.cache import never_cache
from django.http import JsonResponse


class LoginInfoView(TemplateView):

    @never_cache
    def get(self, request, *args, **kwargs):
        current_user_name = ''
        try:
            current_user_name = request.auth['name']
            authenticated = True
        except (AttributeError, KeyError):
            authenticated = False

        response = {
            'isAuthenticated': authenticated,
            'name': current_user_name
        }
        return JsonResponse(response)

