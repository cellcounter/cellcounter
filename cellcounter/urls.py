from django.conf.urls import patterns, include, url
from django.views.generic.simple import direct_to_template
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django.contrib.auth.views import login, logout

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',

    url(r'^$', direct_to_template, {'template': 'main/index.html'},
            name="index"),

    

    url(r'^admin/', include(admin.site.urls)),
    (r'^login/$', login, {'template_name': 'main/login.html'}),
    (r'^logout/$', logout),
)

urlpatterns += staticfiles_urlpatterns()
