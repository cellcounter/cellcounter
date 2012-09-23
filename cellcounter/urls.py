from django.conf.urls import patterns, include, url
from django.views.generic.simple import direct_to_template
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django.contrib import admin
from django.contrib.auth.views import login, logout

from cellcounter.main.views import submit 

admin.autodiscover()

urlpatterns = patterns('',

    url(r'^$', direct_to_template, {'template': 'main/index.html'},
            name="index"),

    url(r'^submit/$', submit, name="submit"),    

    url(r'^admin/', include(admin.site.urls)),
    (r'^login/$', login, {'template_name': 'main/login.html'}),
    (r'^logout/$', logout),
)

urlpatterns += staticfiles_urlpatterns()
