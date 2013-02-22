from django.conf.urls import patterns, include, url
from django.conf import settings
from django.views.generic.simple import direct_to_template
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django.contrib import admin
from django.contrib.auth.views import login, logout

from cellcounter.main.views import new_count

admin.autodiscover()

urlpatterns = patterns('',

    url(r'^$', direct_to_template, {'template': 'main/index.html'},
            name="index"),

    url(r'^count/$', new_count, name="count_home"),
    url(r'^count/new/$', new_count, name="new_count"),
    url(r'^discover/$', direct_to_template, {'template': 'main/discover.html'}, name="discover"),
    url(r'^about/$', direct_to_template, {'template': 'main/about.html'}, name="about"),

    url(r'^login/$', login, {'template_name': 'main/login.html'}, name='login'),
    url(r'^logout/$', logout, {'next_page': '/'}, name='logout'),

    url(r'^accounts/', include('cellcounter.accounts.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^terms$', direct_to_template, {'template': 'main/terms.html'},
            name="terms"),
    url(r'^privacy$', direct_to_template, {'template': 'main/privacy.html'},
            name="privacy"),
)

urlpatterns += staticfiles_urlpatterns()
urlpatterns += url(r'^%s(?P<path>.*)$' % settings.MEDIA_URL.strip("/"), 'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT}),
urlpatterns += url(r'^%s(?P<path>.*)$' % settings.STATIC_URL.strip("/"), 'django.views.static.serve',
        {'document_root': settings.STATIC_ROOT}),

