from django.conf.urls import patterns

from cellcounter.accounts.views import KeyboardLayoutView

urlpatterns = patterns('',
    (r'^keyboard/$', KeyboardLayoutView.as_view()),
)
