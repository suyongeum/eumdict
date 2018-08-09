import logging

import re
from django.db.models.functions import Length
from django.db.models import Count
from django.views.generic import TemplateView
from django.views.decorators.cache import never_cache
from django.http import HttpResponse
from django.http import JsonResponse

from core.contentapi.ContentApi import ContentApi
from core.models import Definitions, Word


logger = logging.getLogger(__name__)


class DefinitionView(TemplateView):

    difficulty_limit = 1

    @never_cache
    def get(self, request, *args, **kwargs):
        corrected_sentence = request.GET.get('corrected_sentence')

        inss = re.findall(r'<ins>(.*?)</ins>', corrected_sentence)

        words = []
        for ins in inss:
            words.extend(ins.split())

        difficult_words = []
        for word in words:
            dbword = Word.objects.filter(word=word).first()
            if dbword is None or (dbword is not None and dbword.difficulty >= self.difficulty_limit):
                difficult_words.append(word)
        difficult_words = list(set(difficult_words))

        definitions = []

        for word in difficult_words:
            definition = Definitions.objects.filter(word=word)\
                                    .annotate(text_len=Length('definition'))\
                                    .order_by('-text_len').first()
            if definition is not None:
                definitions.append({
                    'word': definition.word,
                    'definition': definition.definition,
                    'type': definition.wordtype
                })

        response = {
            'definitions': definitions
        }
        return JsonResponse(response)

