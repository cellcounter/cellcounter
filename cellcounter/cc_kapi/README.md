# Cellcounter Keyboard API v2 

# Setup

As part of the pain Cellcounter project, the below is already done, but as a note on functionality:

cc_kapi is listed in the INSTALLED_APPS in settings.py:
    INSTALLED_APPS = (...
                      'cellcounter.cc_kapi',
                     )

In urls.py we have a declaration to point the keyboard api related requests to the cc_kapi urls.py

    urlpatterns = patterns('',
                           url(r'^api/keyboards', include('cellcounter.cc_kapi.urls')),
                           )

Finally, in deployment, we'll need to run ```collectstatic``` in order to pull the Javascript into the main static directory.

    python manage.py collectstatic


# Usage

Access through api/keyboards/

api/keyboards/
    GET: lists all available keyboards, including builtin and user keyboards for both desktop and mobile

api/keyboards/desktop/
    GET: lists all available desktop keyboards, including builtin and user keyboards
    POST: adds a new desktop keyboard

api/keyboards/desktop/<id>/
    GET: gets the desktop keyboard with identifier <id> (<id>: db_key | 'builtin' | 'default')
    PUT: updates the specified desktop keyboard
    DELETE: deletes the specified desktop keyboard

api/keyboards/desktop/<id>/set_default
    POST: sets the specified desktop keyboard as the default desktop keyboard

api/keyboards/mobile/
    GET: lists all available mobile keyboards, including builtin and user keyboards
    POST: adds a new mobile keyboard

api/keyboards/mobile/<id>/
    GET: gets the mobile keyboard with identifier <id> (<id>: db_key | 'builtin' | 'default')
    PUT: updates the specified mobile keyboard
    DELETE: deletes the specified mobile keyboard

api/keyboards/mobile/<id>/set_default
    POST: sets the specified mobile keyboard as the default mobile keyboard

