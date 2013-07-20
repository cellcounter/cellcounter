from django.conf.urls import patterns, url

from cellcounter.keyboardapi.views import KeyboardAPIView

urlpatterns = patterns('',
    url(r'^$', KeyboardAPIView.as_view(), name="base_keyboard"),
    url(r'^(?P<pk>\d+)/$', KeyboardAPIView.as_view(), name="select_keyboard"),
)