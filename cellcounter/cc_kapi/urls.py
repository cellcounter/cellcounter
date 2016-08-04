from django.conf.urls import url

from .views import KeyboardsListCreateView, KeyboardGetUpdateDestroyView, DefaultKeyboardView

urlpatterns = [
    url('^$', KeyboardsListCreateView.as_view(), name='keyboards'),
    url('^default/$', DefaultKeyboardView.as_view(), name='default-keyboard'),
    url('^(?P<keyboard_id>\d+)/$', KeyboardGetUpdateDestroyView.as_view(), name='keyboard-detail'),
]
