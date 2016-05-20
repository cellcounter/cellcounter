# Cellcounter Keyboard API v2 

# Setup

As part of the pain Cellcounter project, the below is already done, but as a note on functionality:

cc_kapi is listed in the INSTALLED_APPS in settings.py:
    INSTALLED_APPS = (...
                      'cellcounter.cc_kapi',
                     )

In urls.py we have a declaration to point the keyboard api related requests to the cc_kapi urls.py

    urlpatterns = patterns('',
                           url(r'^api/keyboard/', include('cellcounter.cc_kapi.urls')),
                           )

Finally, in deployment, we'll need to run ```collectstatic``` in order to pull the Javascript into the main static directory.

    python manage.py collectstatic


# Usage

Access through api/keyboards

