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

    (r'^login/$', login, {'template_name': 'main/login.html'}),
    (r'^logout/$', logout),

    # Examples:
    # url(r'^$', 'cellcounter.views.home', name='home'),
    # url(r'^cellcounter/', include('cellcounter.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += staticfiles_urlpatterns()
