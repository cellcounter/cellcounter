from rest_framework.routers import Route, SimpleRouter

from .models import Keyboard

class KeyboardAPIRouter(SimpleRouter):
    """
    A router for the keyboard API, which splits desktop and mobile.
    """

    routes = [
        Route(
            url=r'^{prefix}/$',
            mapping={'get': 'list'},
            name='{basename}-list',
            detail=False,
            initkwargs={'suffix': 'List'}
        ),
        Route(
            url=r'^{prefix}/desktop/$',
            mapping={'get': 'list',
                     'post': 'create'},
            name='{basename}-desktop-list',
            detail=False,
            initkwargs={'suffix': 'Desktop List',
                        'device_type' : Keyboard.DESKTOP}
        ),
        Route(
            url=r'^{prefix}/desktop/{lookup}/$',
            mapping={'get': 'retrieve',
                     'put': 'update',
                     'delete': 'destroy'},
            name='{basename}-desktop-detail',
            detail=True,
            initkwargs={'suffix': 'Desktop Detail',
                        'device_type' : Keyboard.DESKTOP}
        ),
        Route(
            url=r'^{prefix}/desktop/{lookup}/set_default$',
            mapping={'put': 'set_default'},
            name='{basename}-desktop-set_default',
            detail=True,
            initkwargs={'suffix': 'Desktop Set Default',
                        'device_type' : Keyboard.DESKTOP}
        ),
        Route(
            url=r'^{prefix}/mobile/$',
            mapping={'get': 'list',
                     'post': 'create'},
            name='{basename}-mobile-list',
            detail=False,
            initkwargs={'suffix': 'Mobile List',
                        'device_type' : Keyboard.MOBILE}
        ),
        Route(
            url=r'^{prefix}/mobile/{lookup}/$',
            mapping={'get': 'retrieve',
                     'put': 'update',
                     'delete': 'destroy'},
            name='{basename}-mobile-detail',
            detail=True,
            initkwargs={'suffix': 'Mobile Detail',
                        'device_type' : Keyboard.MOBILE}
        ),
        Route(
            url=r'^{prefix}/mobile/{lookup}/set_default$',
            mapping={'put': 'set_default'},
            name='{basename}-mobile-set_default',
            detail=True,
            initkwargs={'suffix': 'Mobile Set Default',
                        'device_type' : Keyboard.MOBILE}
        ),
    ]
