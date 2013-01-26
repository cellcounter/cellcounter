from django.conf.urls import patterns, include, url
from django.views.generic.simple import direct_to_template
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django.contrib import admin
from django.contrib.auth.views import login, logout

from cellcounter.main.views import home, new_count, view_count, edit_count, ListMyCountsView, UserDetailView

admin.autodiscover()

urlpatterns = patterns('',

    url(r'^$', direct_to_template, {'template': 'main/index.html'},
            name="index"),

    url(r'^count/$', new_count, name="count_home"),
    url(r'^count/new/$', new_count, name="new_count"),
    url(r'^count/(?P<count_id>\d+)/$', view_count, name="view_count"),
    url(r'^count/(?P<count_id>\d+)/edit/$', edit_count, name="edit_count"),

    url(r'^user/home/$', home),
    url(r'^user/(?P<pk>\d+)/$', UserDetailView.as_view(), name="user_home"),
    url(r'^user/(?P<pk>\d+)/counts/$', ListMyCountsView.as_view(), name="my_counts"),

    url(r'^login/$', login, {'template_name': 'main/login.html'}, name='login'),
    url(r'^logout/$', logout, {'next_page': '/'}, name='logout'),

    url(r'^accounts/', include('cellcounter.accounts.urls')),
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += staticfiles_urlpatterns()
