import json
import logging
import uuid

from datetime import datetime, timezone
from django.http import JsonResponse
from django.views.decorators.cache import never_cache
from django.views.generic import TemplateView

from core.models import LineWord
from wordgaps.models import Error

logger = logging.getLogger(__name__)


class CheckWordGapsView(TemplateView):

    @never_cache
    def post(self, request, *args, **kwargs):
        body_unicode = request.body.decode('utf-8')
        json_data = json.loads(body_unicode)
        content_id = json_data.get('content_id')
        line_id = json_data.get('line_id')
        gaps = json_data.get('gaps')
        request_datetime = datetime.now(timezone.utc)
        request_id = str(uuid.uuid4())

        current_user_id = None
        try:
            current_user_id = request.auth['id']
        except (AttributeError, KeyError):
            pass

        for gap in gaps:
            answer = gap.get('answer')
            order = gap.get('order')
            line_word = LineWord.objects.get(content_id=content_id, line_id=line_id, order=order)
            gap['original'] = line_word.original
            is_correct = line_word.original.lower() == answer.strip().lower()
            gap['correct'] = is_correct
            if not is_correct:
                error = Error()
                error.content_id = content_id
                error.line_id = line_id
                error.order = order
                error.correct = line_word.original
                error.wrong = answer
                error.datetime = request_datetime
                error.request_id = request_id
                error.user_id = current_user_id
                error.save()

        response = {
            'gaps': gaps
        }
        return JsonResponse(response)

