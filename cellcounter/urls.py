from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import TemplateView

from django.contrib import admin
from django.contrib.auth.views import login, logout

from cellcounter.main.views import new_count, images_by_cell_type, ListCellTypesView, similar_images, thumbnail, page

from cellcounter.logs.views import index, host_access, page_access, referrer_access, date_access

admin.autodiscover()

urlpatterns = patterns('',

    url(r'^$', new_count, name="new_count"),

    url(r'^discover/$', TemplateView.as_view(template_name="main/discover.html"), name="discover"),
    url(r'^about/$', TemplateView.as_view(template_name="main/about.html"), name="about"),
    url(r'^help/$', TemplateView.as_view(template_name="main/help.html"), name="help"),

    url(r'^images/celltype/(?P<cell_type>\w+)/$', images_by_cell_type, name="images_by_cell_type"),
    url(r'^images/similar/(?P<cell_image_pk>\d+)/$', similar_images, name="images_by_similar_cell"),
    url(r'^images/thumbnail/(?P<cell_image_pk>\d+)/$', thumbnail, name="thumbnail"),
    url(r'^images/page/(?P<cell_image_pk>\d+)/$', page, name="page"),


    url(r'^api/cell_types/$', ListCellTypesView.as_view(), name="cell_types"),

    url(r'^login/$', login, {'template_name': 'main/login.html'}, name='login'),
    url(r'^logout/$', logout, {'next_page': '/'}, name='logout'),

    url(r'^api/keyboard/', include('cellcounter.keyboardapi.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^terms$', TemplateView.as_view(template_name="main/terms.html"),
            name="terms"),
    url(r'^privacy$', TemplateView.as_view(template_name="main/privacy.html"),
            name="privacy"),
    
    url(r'^logs/$', index, name="logs"),
    url(r'^logs/hosts/$', host_access, name="log_hosts"),
    url(r'^logs/pages/$', page_access, name="log_pages"),
    url(r'^logs/referrers/$', referrer_access, name="log_referrers"),
    url(r'^logs/dates/$', date_access, name="log_dates"),
)

urlpatterns += staticfiles_urlpatterns()
urlpatterns += url(r'^%s(?P<path>.*)$' % settings.MEDIA_URL.strip("/"), 'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT}),
urlpatterns += url(r'^%s(?P<path>.*)$' % settings.STATIC_URL.strip("/"), 'django.views.static.serve',
        {'document_root': settings.STATIC_ROOT}),

