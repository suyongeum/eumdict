from django.conf.urls import url

from core.view.WordsView import WordsView
from core.view.CheckWordGapsView import CheckWordGapsView
from core.view.IndexView import IndexView
from core.view.ScriptView import ScriptView
from core.view.LineNumberView import LineNumberView
from core.view.LineStatisticsView import LineStatisticsView
from core.view.LineStatisticsAllView import LineStatisticsAllView
from core.view.CheckView import CheckView
from core.view.AudioView import AudioView
from core.view.RegisterView import RegisterView
from core.view.LogoutView import LogoutView
from core.view.AuthenticateView import AuthenticateView
from core.view.LoginInfoView import LoginInfoView
from core.view.SettingsListView import SettingsListView
from core.view.UserSettingsView import UserSettingsView
from core.view.SaveUserSettingsView import SaveUserSettingsView
from core.view.LastLineView import LastLineView
from core.view.SaveLastLineView import SaveLastLineView
from core.view.LastAttemptView import LastAttemptView
from core.view.SentenceDifficultyView import SentenceDifficultyView
from core.view.TopMistakesView import TopMistakesView
from core.view.DefinitionView import DefinitionView
from core.view.WordGapsView import WordGapsView
from core.view.ContentView import ContentView

urlpatterns = [
    url(r'^content$', ContentView.as_view()),
    url(r'^words$', WordsView.as_view()),
    url(r'^checkwordgaps$', CheckWordGapsView.as_view()),
    url(r'^wordgaps$', WordGapsView.as_view()),
    url(r'^definitions', DefinitionView.as_view()),
    url(r'^top_mistakes', TopMistakesView.as_view()),
    url(r'^sentence_difficulty', SentenceDifficultyView.as_view()),
    url(r'^last_attempt', LastAttemptView.as_view()),
    #TODO: change to LastLine.post
    url(r'^save_last_line', SaveLastLineView.as_view()),
    url(r'^last_line', LastLineView.as_view()),
    #TODO: change to user_settings.post
    url(r'^save_user_settings', SaveUserSettingsView.as_view()),
    url(r'^user_settings', UserSettingsView.as_view()),
    url(r'^settings_list', SettingsListView.as_view()),
    url(r'^login_info', LoginInfoView.as_view()),
    url(r'^authenticate$', AuthenticateView.as_view()),
    url(r'^logout', LogoutView.as_view()),
    url(r'^register', RegisterView.as_view()),
    #  TODO: change url to just audio
    url(r'^get_audio', AudioView.as_view()),
    url(r'^check$', CheckView.as_view()),
    url(r'^line_statistics_all', LineStatisticsAllView.as_view()),
    url(r'^line_statistics$', LineStatisticsView.as_view()),
    url(r'^line_number$', LineNumberView.as_view()),
    url(r'^script$', ScriptView.as_view()),
    url(r'^$', IndexView.as_view()),
]
