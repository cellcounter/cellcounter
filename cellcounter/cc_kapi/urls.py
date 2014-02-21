from django.conf.urls import patterns, url

from .views import KeyboardView

urlpatterns = patterns('',
    url('^$', KeyboardView.as_view(),
        name='keyboard'),
    url('^(?P<keyboard_id>\d+)/$', KeyboardView.as_view(),
        name='keyboard-detail'),
)
