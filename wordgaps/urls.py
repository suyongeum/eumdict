from django.conf.urls import url

from wordgaps.view.IndexView import IndexView

urlpatterns = [

    url(r'^$', IndexView.as_view()),
]
