from django.views.generic import TemplateView
from django.shortcuts import render
from django.views.decorators.cache import never_cache

from core.contentapi.ContentApi import ContentApi


class ScriptView(TemplateView):

    def __init__(self):
        self.content_api = ContentApi()

    @never_cache
    def get(self, request, *args, **kwargs):
        content_id = request.GET.get('content_id')
        lines = self.content_api.get_content_script(content_id)
        context = {
            'lines': lines,
            'range': range(len(lines))
        }
        return render(request, 'core/script.html', context)
