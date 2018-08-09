
import logging
import random

from django.http import JsonResponse
from django.views.decorators.cache import never_cache
from django.views.generic import TemplateView

from core.models import LineWord

logger = logging.getLogger(__name__)


class WordGapsView(TemplateView):

    number_of_gaps = 3

    @never_cache
    def get(self, request, *args, **kwargs):
        content_id = int(request.GET.get('content_id'))
        line_id = int(request.GET.get('line_id'))
        difficulty = int(request.GET.get('difficulty'))

        line_words = LineWord.objects.filter(content_id=content_id, line_id=line_id).order_by('order')

        line_length = len(line_words)
        gaps = []
        if line_length <= self.number_of_gaps:
            gaps = range(1, line_length + 1)
        else:
            current_difficulty = difficulty
            going_down = True
            while True:
                current_difficulty_words = [w for w in line_words if w.difficulty == current_difficulty]
                for __ in range(len(current_difficulty_words)):
                    if len(gaps) == self.number_of_gaps:
                        break
                    i = random.randint(0, len(current_difficulty_words) - 1)
                    gaps.append(current_difficulty_words[i].order)
                    del current_difficulty_words[i]

                if len(gaps) < self.number_of_gaps:
                    if going_down:
                        current_difficulty -= 1
                    else:
                        current_difficulty += 1
                else:
                    break

                if current_difficulty == 0:
                    current_difficulty = difficulty + 1
                    going_down = False

        words = []

        for w in line_words:
            word = {
                'difficulty': w.difficulty,
                'order': w.order,
                'definition': w.definition
            }
            if w.order in gaps:
                word['is_gap'] = True
                word['word'] = w.original
            else:
                word['is_gap'] = False
                word['word'] = w.original
            words.append(word)

        response = {
            'words': words
        }
        return JsonResponse(response)

