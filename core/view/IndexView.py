from django.views.generic import TemplateView
from django.shortcuts import render
from django.views.decorators.cache import never_cache


class IndexView(TemplateView):
    @never_cache
    def get(self, request, *args, **kwargs):

        current_user_name = ''
        current_user_email = ''
        try:
            current_user_name = request.auth['name']
            current_user_email = request.auth['email']
            authenticated = True
        except AttributeError:
            authenticated = False

        context = {
            'authenticated': authenticated,
            'name': current_user_name,
            'email': current_user_email
        }

        return render(request, 'core/index.html', context)
