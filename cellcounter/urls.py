from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import TemplateView

from cellcounter.main.views import (
    NewCountTemplateView,
    CellImageListView,
    CellTypesListView,
    CellImageDetailView,
    similar_images,
    thumbnail,
)

admin.autodiscover()

urlpatterns = [
    url(r"^$", NewCountTemplateView.as_view(), name="new_count"),
    url(
        r"^discover/$",
        TemplateView.as_view(template_name="main/discover.html"),
        name="discover",
    ),
    url(
        r"^about/$", TemplateView.as_view(template_name="main/about.html"), name="about"
    ),
    url(r"^help/$", TemplateView.as_view(template_name="main/help.html"), name="help"),
    url(
        r"^images/celltype/(?P<cell_type>\w+)/$",
        CellImageListView.as_view(),
        name="images_by_cell_type",
    ),
    url(
        r"^images/similar/(?P<cell_image_pk>\d+)/$",
        similar_images,
        name="images_by_similar_cell",
    ),
    url(r"^images/thumbnail/(?P<cell_image_pk>\d+)/$", thumbnail, name="thumbnail"),
    url(
        r"^images/page/(?P<cell_image_pk>\d+)/$",
        CellImageDetailView.as_view(),
        name="page",
    ),
    url(r"^api/cell_types/$", CellTypesListView.as_view(), name="cell_types"),
    url(r"^api/stats/", include("cellcounter.statistics.urls")),
    url(r"^login/$", LoginView.as_view(template_name="main/login.html"), name="login"),
    url(r"^logout/$", LogoutView.as_view(next_page="/"), name="logout"),
    url(r"^api/keyboards/", include("cellcounter.cc_kapi.urls")),
    url(r"^accounts/", include("cellcounter.accounts.urls")),
    url(r"^admin/", admin.site.urls),
    url(
        r"^terms$", TemplateView.as_view(template_name="main/terms.html"), name="terms"
    ),
    url(
        r"^privacy$",
        TemplateView.as_view(template_name="main/privacy.html"),
        name="privacy",
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
