from django.conf.urls import patterns, url

from cellcounter.accounts import views

urlpatterns = patterns('',
    url('^new/$', views.RegistrationView.as_view(), name='register'),
    url('^(?P<pk>[0-9]+)/$', views.UserDetailView.as_view(), name='user-detail'),
    url('^(?P<pk>[0-9]+)/delete/$', views.UserDeleteView.as_view(), name='user-delete'),
    url('^(?P<pk>[0-9]+)/edit/$', views.UserUpdateView.as_view(), name='user-update'),
    url('^password/reset/$', views.PasswordResetView.as_view(),
        name='password-reset'),
    url('^password/reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.PasswordResetConfirmView.as_view(),
        name='password-reset-confirm'),
    url('^password/change/$', views.PasswordChangeView.as_view(), name='change-password'),
)