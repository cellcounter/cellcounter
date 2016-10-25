from .views import KeyboardViewSet

from rest_framework import routers
from .routers import KeyboardAPIRouter

router = KeyboardAPIRouter()
router.register(r'', KeyboardViewSet, base_name='keyboards')
urlpatterns = router.urls

