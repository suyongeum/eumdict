import urllib

from django.http import HttpResponse
from django.views.decorators.cache import never_cache
from django.views.generic import TemplateView
from django.conf import settings

class AudioView(TemplateView):

    @never_cache
    def get(self, request, *args, **kwargs):
        content_id = request.GET.get('content_id')
        line_id = request.GET.get('line_id')
        url = settings.URL_DATA + str(content_id) + '/mp3/' + str(line_id) + '.mp3'

        req = urllib.request.Request(url)
        with urllib.request.urlopen(req) as response:
            file = response.read()

        return HttpResponse(file, content_type='audio/mp3')
