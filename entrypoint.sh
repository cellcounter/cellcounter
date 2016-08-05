#!/bin/bash
set -e

# Docker entrypoint script expects the following environment variables installed:
# DATABASE_URL - url in dj_database_url format for finding database

if [ "$1" = 'manage.py' ]; then
    exec python manage.py "${@:2}"
fi

exec uwsgi --ini /app/conf/uwsgi.ini
