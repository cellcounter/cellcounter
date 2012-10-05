from django.conf.urls import patterns, include, url
from django.views.generic.simple import direct_to_template
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django.contrib import admin
from django.contrib.auth.views import login, logout

from cellcounter.main.views import new_count, view_count, edit_count

admin.autodiscover()

urlpatterns = patterns('',

    url(r'^$', direct_to_template, {'template': 'main/index.html'},
            name="index"),

    url(r'^count/$', new_count, name="count_home"),
    url(r'^count/new/$', new_count, name="new_count"),
    url(r'^count/(?P<pk>\d+)/$', view_count, name="view_count"),
    url(r'^count/(?P<pk>\d+)/edit/$', edit_count, name="edit_count"),

    (r'^login/$', login, {'template_name': 'main/login.html'}),
    (r'^logout/$', logout),
    
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += staticfiles_urlpatterns()
