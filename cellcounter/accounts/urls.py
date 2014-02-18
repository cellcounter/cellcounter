from django.conf.urls import patterns, url

from cellcounter.accounts import views

urlpatterns = patterns('',
    url('^new/$', views.RegistrationView.as_view(), name='register'),
    url('^(?P<pk>[0-9]+)/$', views.UserDetailView.as_view(), name='user-detail'),
    url('^(?P<pk>[0-9]+)/delete/$', views.UserDeleteView.as_view(), name='user-delete'),
    url('^password/reset/$', 'django.contrib.auth.views.password_reset', {
        'template_name': 'accounts/reset_form.html',
        'email_template_name': 'accounts/reset_email.txt',
        'subject_template_name': 'accounts/reset_subject.txt',
        'current_app': 'cellcounter.accounts',
        'post_reset_redirect': 'password-reset-sent',
        },
        name='password-reset'),
    url('^password/reset/sent/$', views.password_reset_sent, name='password-reset-sent'),
    url('^password/reset/done/$', views.password_reset_done, name='password-reset-done'),
    url('^password/reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[\d\w\-]+)/$',
        'django.contrib.auth.views.password_reset_confirm', {
            'template_name': 'accounts/reset_confirm.html',
            'post_reset_redirect': 'password-reset-done',
            },
        name='password-reset-confirm'),
    url('^password/change/$', views.PasswordChangeView.as_view(), name='change-password'),
    url('^license/$', views.LatestLicenseDetailView.as_view(), name='latest-license'),
    url('^license/(?P<pk>[0-9]+)/$', views.LicenseDetailView.as_view(), name='license-detail'),
)