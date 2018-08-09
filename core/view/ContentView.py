
import logging

from django.http import JsonResponse
from django.views.decorators.cache import never_cache
from django.views.generic import TemplateView

from core.models import Content

logger = logging.getLogger(__name__)


class ContentView(TemplateView):

    @never_cache
    def get(self, request, *args, **kwargs):

        db_contents = Content.objects.all()

        contents = []
        for content in db_contents:
            contents.append({
                'id': content.id,
                'name': content.name.split('_', 1)[-1]
            })

        response = {
            'contents': contents
        }
        return JsonResponse(response)

