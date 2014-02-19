from django.conf.urls import patterns, url

from .views import KeyboardView, KeyboardRenameView

urlpatterns = patterns('',
    url('^$', KeyboardView.as_view(),
        name='keyboard'),
    url('^(?P<keyboard_id>\d+)/$', KeyboardView.as_view(),
        name='keyboard-detail'),
    url('^(?P<pk>\d+)/update/$', KeyboardRenameView.as_view(),
        name='rename-keyboard'),
)