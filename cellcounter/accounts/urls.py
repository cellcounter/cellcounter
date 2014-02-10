from django.conf.urls import patterns, url

from .views import RegistrationView, PasswordChangeView, password_reset_sent, password_reset_done, LicenseDetailView


urlpatterns = patterns('',
    url('^new/$', RegistrationView.as_view(), name='register'),
    url('^password/reset/$', 'django.contrib.auth.views.password_reset', {
        'template_name': 'accounts/reset_form.html',
        'email_template_name': 'accounts/reset_email.txt',
        'subject_template_name': 'accounts/reset_subject.txt',
        'current_app': 'cellcounter.accounts',
        'post_reset_redirect': 'password-reset-sent',
        },
        name='password-reset'),
    url('^password/reset/sent/$', password_reset_sent, name='password-reset-sent'),
    url('^password/reset/done/$', password_reset_done, name='password-reset-done'),
    url('^password/reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[\d\w\-]+)/$',
        'django.contrib.auth.views.password_reset_confirm', {
            'template_name': 'accounts/reset_confirm.html',
            'post_reset_redirect': 'password-reset-done',
            },
        name='password-reset-confirm'),
    url('^password/change/$', PasswordChangeView.as_view(), name='change-password'),
    url('^license/$', LicenseDetailView.as_view(), name='license')
)