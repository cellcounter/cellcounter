"""
WSGI config for cellcounter project.

This module contains the WSGI application used by Django's development server
and any production WSGI deployments. It should expose a module-level variable
named ``application``. Django's ``runserver`` and ``runfcgi`` commands discover
this application via the ``WSGI_APPLICATION`` setting.

Usually you will have the standard Django WSGI application here, but it also
might make sense to replace the whole Django WSGI application with a custom one
that later delegates to the Django one. For example, you could introduce WSGI
middleware here, or combine a Django application with an application of another
framework.

"""
import os
import site
from distutils.sysconfig import get_python_lib

#ensure the venv is being loaded correctly
site.addsitedir(get_python_lib())

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cellcounter.settings")

#import the DATABASE_URL from an Apache environment variable
#this allows per-vhost database configuration to be passed in
import django.core.handlers.wsgi
_application = django.core.handlers.wsgi.WSGIHandler()

def application(environ, start_response):
  os.environ['DATABASE_URL'] = environ.get('DATABASE_URL', '')
  return _application(environ, start_response)

# Apply WSGI middleware here.
# from helloworld.wsgi import HelloWorldApplication
# application = HelloWorldApplication(application)
