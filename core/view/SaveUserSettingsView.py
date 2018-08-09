import logging

from django.views.generic import TemplateView
from django.views.decorators.cache import never_cache
from django.http import HttpResponse

from core.models import UserSetting

logger = logging.getLogger(__name__)

class SaveUserSettingsView(TemplateView):

    @never_cache
    def post(self, request, *args, **kwargs):
        try:
            current_user_id = request.auth['id']
        except (AttributeError, KeyError):
            return HttpResponse('Please log in.', status=400)

        try:
            number_of_repetitions = request.POST['number_of_repetitions']
            delay_between_repetitions = request.POST['delay_between_repetitions']
        except KeyError:
            return HttpResponse('Fill in all fields', status=400)

        current_user_settings = UserSetting.objects.filter(user_id=current_user_id)

        number_of_repetitions_settings = list(filter(lambda x: x.setting_id == 1, current_user_settings))
        if len(number_of_repetitions_settings) == 0:
            number_of_repetitions_setting = UserSetting(setting_id=1, user_id=current_user_id,
                                                        value=number_of_repetitions)
            number_of_repetitions_setting.save()
        else:
            if len(number_of_repetitions_settings) > 1:
                logger.error('More then one value found for number_of_repetitions_setting')
                return HttpResponse(status=500)
            number_of_repetitions_setting = number_of_repetitions_settings[0]
            number_of_repetitions_setting.value = number_of_repetitions
            number_of_repetitions_setting.save()

        delay_between_repetitions_settings = list(filter(lambda x: x.setting_id == 2, current_user_settings))
        if len(delay_between_repetitions_settings) == 0:
            delay_between_repetitions_setting = UserSetting(setting_id=2, user_id=current_user_id,
                                                            value=delay_between_repetitions)
            delay_between_repetitions_setting.save()
        else:
            if len(delay_between_repetitions_settings) > 1:
                logger.error('More then one value found for delay_between_repetitions_setting')
                return HttpResponse(status=500)
            delay_between_repetitions_setting = delay_between_repetitions_settings[0]
            delay_between_repetitions_setting.value = delay_between_repetitions
            delay_between_repetitions_setting.save()
        return HttpResponse(status=200)
