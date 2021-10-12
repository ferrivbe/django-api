#!/usr/bin/env bash

cd /code/backend

# image can run in multiple modes
if [[ "${1}" == "shell" ]]; then
    exec /bin/bash
elif [[ "${1}" == "migrate-noinput" ]]; then
    exec pipenv run python3.9 manage.py migrate --noinput
elif [[ "${1}" == "collectstatic" ]]; then
    exec pipenv run python3.9 manage.py collectstatic --noinput
elif [[ "${1}" == "runserver" ]]; then
    exec pipenv run python3.9 manage.py makemigrations \
        & pipenv run python3.9 manage.py migrate \
        & pipenv run gunicorn backend.wsgi:application --bind 0.0.0.0:8000
elif [[ "${1}" == "migrate" ]]; then
    exec pipenv run python3.9 manage.py migrate
elif [[ "${1}" == "makemigrations" ]]; then
    exec pipenv run python3.9 manage.py makemigrations
else
    exec gunicorn --config=gunicorn_config.py server.wsgi
fi