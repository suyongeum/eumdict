import logging

from django.views.generic import TemplateView
from django.views.decorators.cache import never_cache
from django.http import HttpResponse
from django.http import JsonResponse

from core.models import UserLastLine


logger = logging.getLogger(__name__)


class LastLineView(TemplateView):

    @never_cache
    def get(self, request, *args, **kwargs):
        try:
            current_user_id = request.auth['id']
        except (AttributeError, KeyError):
            return HttpResponse('Please log in.', status=400)

        current_user_last_lines = UserLastLine.objects.filter(user_id=current_user_id)

        line = -1
        content_id = -1

        if len(current_user_last_lines) > 0:
            if len(current_user_last_lines) > 1:
                logger.error('More then one value found for current_user_last_line')
                return HttpResponse(status=500)
            current_user_last_line = current_user_last_lines[0]
            line = current_user_last_line.line
            content_id = current_user_last_line.content_id

        response = {
            'line': line,
            'content_id': content_id
        }
        return JsonResponse(response)
