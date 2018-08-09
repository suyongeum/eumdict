import logging

from django.db.models import Count
from django.views.generic import TemplateView
from django.views.decorators.cache import never_cache
from django.http import HttpResponse
from django.http import JsonResponse

from core.models import Error


logger = logging.getLogger(__name__)


class LastAttemptView(TemplateView):

    @never_cache
    def get(self, request, *args, **kwargs):
        content_id = request.GET.get('content_id')
        line_id = request.GET.get('line_id')

        try:
            current_user_id = request.auth['id']
        except (AttributeError, KeyError):
            return HttpResponse('Please log in.', status=400)

        try:
            last_error = Error.objects.filter(user_id=current_user_id, content_id=content_id, line=line_id).latest()
            last_errors = Error.objects.filter(request_id=last_error.request_id)

            tries = Error.objects.filter(user_id=current_user_id, content_id=content_id, line=line_id) \
                .values('request_id', 'datetime').annotate(total=Count('request_id'))

        except Error.DoesNotExist:
            response = {
                'tries': 0
            }
            return JsonResponse(response)

        datetime = last_error.datetime
        amount = len(last_errors)
        words = ''
        for error in last_errors:
            words += error.correct + ' '

        response = {
            'tries': len(tries),
            'datetime': datetime,
            'amount': amount,
            'words': words
        }
        return JsonResponse(response)

