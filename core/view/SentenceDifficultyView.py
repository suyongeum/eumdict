import logging

from django.views.generic import TemplateView
from django.views.decorators.cache import never_cache
from django.http import JsonResponse

from core.contentapi.ContentApi import ContentApi


logger = logging.getLogger(__name__)


class SentenceDifficultyView(TemplateView):

    def __init__(self):
        self.content_api = ContentApi()

    @never_cache
    def get(self, request, *args, **kwargs):
        content_id = request.GET.get('content_id')
        line_id = int(request.GET.get('line_id'))
        difficulty = self.content_api.get_line_difficulty(content_id, line_id)
        response = {
            'difficulty': round(difficulty, 2)
        }
        return JsonResponse(response)

