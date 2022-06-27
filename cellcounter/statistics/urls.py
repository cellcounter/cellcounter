from django.conf.urls import url

from .views import ListCreateCountInstanceAPI

urlpatterns = [
    url("^$", ListCreateCountInstanceAPI.as_view(), name="create-count-instance"),
]
