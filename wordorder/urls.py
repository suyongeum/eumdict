from django.conf.urls import url

from wordorder.view.IndexView import IndexView

urlpatterns = [

    url(r'^$', IndexView.as_view()),
]
