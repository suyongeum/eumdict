
import logging
import random

from django.http import JsonResponse
from django.views.decorators.cache import never_cache
from django.views.generic import TemplateView

from core.models import LineWord

logger = logging.getLogger(__name__)


class WordsView(TemplateView):

    @never_cache
    def get(self, request, *args, **kwargs):
        content_id = int(request.GET.get('content_id'))
        line_id = int(request.GET.get('line_id'))

        line_words = LineWord.objects.filter(content_id=content_id, line_id=line_id).order_by('order')

        words = []

        for w in line_words:
            word = {
                'order': w.order,
                'definition': w.definition,
                'original': w.original
            }
            words.append(word)

        response = {
            'words': words
        }
        return JsonResponse(response)

