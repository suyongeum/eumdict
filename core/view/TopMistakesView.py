from django.views.generic import TemplateView
from django.views.decorators.cache import never_cache
from django.http import JsonResponse
from django.http import HttpResponse
from django.db.models import Count

from core.contentapi.ContentApi import ContentApi
from core.models import Error


class TopMistakesView(TemplateView):

    def __init__(self):
        self.content_api = ContentApi()

    @never_cache
    def get(self, request, *args, **kwargs):
        content_id = int(request.GET.get('content_id'))
        line_id = int(request.GET.get('line_id'))

        errors = []

        e = Error.objects.filter(content_id=content_id, line=line_id) \
            .values('correct').annotate(total=Count('correct')).order_by('-correct')[:5]

        for error in e:
            errors.append(error['correct'])

        response = {
            'errors': errors
        }
        return JsonResponse(response)