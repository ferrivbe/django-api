#!/usr/bin/env bash

cd /opt/django-api/backend

# image can run in multiple modes
if [[ "${1}" == "shell" ]]; then
    exec /bin/bash
elif [[ "${1}" == "migrate-noinput" ]]; then
    exec python manage.py migrate --noinput
elif [[ "${1}" == "collectstatic" ]]; then
    exec python manage.py collectstatic --noinput
elif [[ "${1}" == "runserver" ]]; then
    exec python manage.py makemigrations \
        & python manage.py migrate \
        & gunicorn server.wsgi:application --bind 0.0.0.0:8000
elif [[ "${1}" == "migrate" ]]; then
    exec python manage.py migrate
elif [[ "${1}" == "makemigrations" ]]; then
    exec python manage.py makemigrations
else
    exec gunicorn --config=gunicorn_config.py server.wsgi
fi