from django.views.generic import TemplateView
from django.views.decorators.cache import never_cache
from django.http import JsonResponse

from core.models import Setting


class SettingsListView(TemplateView):

    @never_cache
    def get(self, request, *args, **kwargs):
        number_of_repetitions_setting = Setting.objects.filter(setting_name='number_of_repetitions')[0]
        delay_between_repetitions_setting = Setting.objects.filter(setting_name='delay_between_repetitions')[0]

        # settings_json = serializers.serialize('json', all_settings)
        # return HttpResponse(settings_json, content_type="application/json")

        response = {
            'number_of_repetitions': {
                'id': number_of_repetitions_setting.id,
                'default_value': number_of_repetitions_setting.default_value
            },
            'delay_between_repetitions': {
                'id': delay_between_repetitions_setting.id,
                'default_value': delay_between_repetitions_setting.default_value
            },
        }
        return JsonResponse(response)
