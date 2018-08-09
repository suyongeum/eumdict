from django.views.generic import TemplateView
from django.views.decorators.cache import never_cache
from django.http import JsonResponse
from django.http import HttpResponse
from django.db.models import Count

from core.contentapi.ContentApi import ContentApi
from core.models import Error


class LineStatisticsAllView(TemplateView):

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

        total_words_in_line = self.content_api.get_amount_of_words_in_line(content_id, line_id)

        requests = []
        if personalize:
            e = Error.objects.filter(content_id=content_id, line=line_id, user_id=current_user_id) \
                .values('request_id', 'datetime').annotate(total=Count('request_id'))
        else:
            e = Error.objects.filter(content_id=content_id, line=line_id) \
                .values('request_id', 'datetime').annotate(total=Count('request_id'))

        for error in e:
            accuracy = 1 - (error['total'] / total_words_in_line)
            requests.append(accuracy)

        total_accuracy = 0
        if len(requests) != 0:
            for r in requests:
                total_accuracy += r
            total_accuracy /= len(requests)

        response = {
            'data': total_accuracy
        }
        return JsonResponse(response)