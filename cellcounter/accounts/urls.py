from django.conf.urls import patterns 
from django.contrib.auth.decorators import login_required

from cellcounter.accounts.views import KeyboardLayoutView

urlpatterns = patterns('',
    (r'^keyboard/$', KeyboardLayoutView.as_view()),
)
