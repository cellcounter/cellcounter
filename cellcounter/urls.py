from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import login, logout
from django.views.generic import TemplateView

from cellcounter.main import views

admin.autodiscover()

urlpatterns = [
                  url(r'^$', views.NewCountTemplateView.as_view(), name="new_count"),
                  url(r'^discover/$', TemplateView.as_view(template_name="main/discover.html"), name="discover"),
                  url(r'^about/$', TemplateView.as_view(template_name="main/about.html"), name="about"),
                  url(r'^help/$', TemplateView.as_view(template_name="main/help.html"), name="help"),
                  url(r'^images/celltype/(?P<cell_type>\w+)/$', views.CellImageListView.as_view(),
                      name="images_by_cell_type"),
                  url(r'^images/similar/(?P<cell_image_pk>\d+)/$', views.similar_images, name="images_by_similar_cell"),
                  url(r'^images/thumbnail/(?P<cell_image_pk>\d+)/$', views.thumbnail, name="thumbnail"),
                  url(r'^images/page/(?P<cell_image_pk>\d+)/$', views.CellImageDetailView.as_view(), name="page"),
                  url(r'^api/cell_types/$', views.CellTypesListView.as_view(), name="cell_types"),
                  url(r'^api/stats/$', include('cellcounter.statistics.urls')),
                  url(r'^login/$', login, {'template_name': 'main/login.html'}, name='login'),
                  url(r'^logout/$', logout, {'next_page': '/'}, name='logout'),
                  url(r'^api/keyboards/', include('cellcounter.cc_kapi.urls')),
                  url(r'^accounts/', include('cellcounter.accounts.urls')),
                  url(r'^admin/', include(admin.site.urls)),
                  url(r'^terms$', TemplateView.as_view(template_name="main/terms.html"), name="terms"),
                  url(r'^privacy$', TemplateView.as_view(template_name="main/privacy.html"), name="privacy")
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
