from django.views.generic import TemplateView
from django.views.decorators.cache import never_cache
from django.http import JsonResponse

from core.contentapi.ContentApi import ContentApi


class LineNumberView(TemplateView):

    def __init__(self):
        self.content_api = ContentApi()

    @never_cache
    def get(self, request, *args, **kwargs):
        content_id = request.GET.get('content_id')
        # TODO: check for positive number
        lines = self.content_api.get_number_of_lines(content_id)
        # TODO: check response - array os strings
        response = {'lines': lines}
        return JsonResponse(response)
