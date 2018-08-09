from datetime import datetime, timezone

from django.views.generic import TemplateView
from django.views.decorators.cache import never_cache
from django.http import JsonResponse
from django.http import HttpResponse
from django.db.models import Count

from core.contentapi.ContentApi import ContentApi
from core.models import Error


class LineStatisticsView(TemplateView):

    def __init__(self):
        self.content_api = ContentApi()

    @never_cache
    def get(self, request, *args, **kwargs):
        content_id = int(request.GET.get('content_id'))
        line_id = int(request.GET.get('line_id'))
        personalize = request.GET.get('personalize') in ['true', 'True']

        current_user_id = -1
        if personalize:
            try:
                current_user_id = request.auth['id']
            except (AttributeError, KeyError):
                return HttpResponse('Unable to personalize. Please log in.', status=400)

        now = datetime.now(timezone.utc)
        number_of_days = 7

        total_words_in_line = self.content_api.get_amount_of_words_in_line(content_id, line_id)

        # get errors from db
        errors_by_days = []
        for i in range(number_of_days + 1):
            errors_by_days.append(1)

        e = []
        if personalize:
            e = Error.objects.filter(content_id=content_id, line=line_id, user_id=current_user_id) \
                .values('request_id', 'datetime').annotate(total=Count('request_id'))
        else:
            e = Error.objects.filter(content_id=content_id, line=line_id) \
                .values('request_id', 'datetime').annotate(total=Count('request_id'))

        requests_by_days = {}
        for i in range(number_of_days + 1):
            requests_by_days[i] = []

        for error in e:
            days_passed = (now - error['datetime']).days
            if error['datetime'] > now or days_passed > number_of_days:
                continue
            accuracy = 1 - (error['total'] / total_words_in_line)
            requests_by_days[days_passed].append(accuracy)

        for i in range(number_of_days + 1):
            if len(requests_by_days[i]) == 0:
                continue
            total_accuracy = 0
            for r in requests_by_days[i]:
                total_accuracy += r
            errors_by_days[i] = total_accuracy / len(requests_by_days[i])

        response = {
            'data': errors_by_days
        }
        return JsonResponse(response)
