from django.conf.urls import patterns, url
from django.core.urlresolvers import reverse

from .views import RegistrationView, PasswordChangeView, password_reset_done


urlpatterns = patterns('',
    url('^new/$', RegistrationView.as_view(), name='register'),
    url('^password/reset/$', 'django.contrib.auth.views.password_reset', {
        'template_name': 'accounts/reset_form.html',
        'email_template_name': 'accounts/reset_email.txt',
        'subject_template_name': 'accounts/reset_subject.txt',
        'current_app': 'cellcounter.accounts',
        'post_reset_redirect': '/',
        },
        name='reset-request'),
    url('^password/reset/confirm/(?P<uidb64>\d+)/(?P<token>[\d\w-]+)/$',
        'django.contrib.auth.views.password_reset_confirm', {
            'template_name': 'accounts/reset_confirm.html',
            'post_reset_redirect': password_reset_done,
            },
        name='password-reset-confirm'),
    url('^password/change/$', PasswordChangeView.as_view(), name='change-password'),
)