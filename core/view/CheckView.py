import uuid
import re
from datetime import datetime, timezone

from django.views.generic import TemplateView
from django.views.decorators.cache import never_cache
from django.http import JsonResponse
from django.http import HttpResponse

from core.contentapi.ContentApi import ContentApi
from core.models import Error


class CheckView(TemplateView):

    def __init__(self):
        self.content_api = ContentApi()

    @never_cache
    def get(self, request, *args, **kwargs):
        content_id = request.GET.get('content_id')
        line_id = request.GET.get('line_id')
        text = request.GET.get('text')
        request_id = str(uuid.uuid4())
        request_datetime = datetime.now(timezone.utc)

        current_user_id = None
        try:
            current_user_id = request.auth['id']
        except (AttributeError, KeyError):
            pass

        verified = self.content_api.verify_line(content_id, line_id, text)

        dels = re.findall(r'<del>(.*?)</del>', verified)
        inss = re.findall(r'<ins>(.*?)</ins>', verified)
        if len(dels) != len(inss):
            return HttpResponse('Incorrect response from app server', status=502)

        for i in range(len(dels)):
            error = Error(content_id=content_id,
                          line=line_id,
                          correct=inss[i].strip(),
                          wrong=dels[i].strip(),
                          request_id=request_id,
                          datetime=request_datetime,
                          user_id=current_user_id)
            error.save()

        response = {'result': verified}
        return JsonResponse(response)
