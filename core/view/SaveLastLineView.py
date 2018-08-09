import logging
from datetime import datetime #, timezone

from django.views.generic import TemplateView
from django.views.decorators.cache import never_cache
from django.http import HttpResponse

from core.models import UserLastLine

logger = logging.getLogger(__name__)

class SaveLastLineView(TemplateView):

    @never_cache
    def post(self, request, *args, **kwargs):
        try:
            current_user_id = request.auth['id']
        except (AttributeError, KeyError):
            return HttpResponse('Please log in.', status=400)

        try:
            content_id = request.POST['content_id']
            line = request.POST['line']
        except KeyError:
            return HttpResponse('Fill in all fields', status=400)

        request_datetime = datetime.now(timezone.utc)

        current_user_last_lines = UserLastLine.objects.filter(user_id=current_user_id)

        if len(current_user_last_lines) == 0:
            current_user_last_line = UserLastLine(user_id=current_user_id,
                                                  content_id=content_id,
                                                  line=line,
                                                  datetime=request_datetime)
            current_user_last_line.save()
        else:
            if len(current_user_last_lines) > 1:
                logger.error('More then one value found for current_user_last_line')
                return HttpResponse(status=500)
            current_user_last_line = current_user_last_lines[0]
            current_user_last_line.line = line
            current_user_last_line.content_id = content_id
            current_user_last_line.datetime = request_datetime
            current_user_last_line.save()

        return HttpResponse(status=200)
