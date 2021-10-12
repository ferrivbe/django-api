FROM python:3.9-slim-buster

RUN python3.9 -m pip install pipenv

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    # compiler for Python C modules
    g++ make libc6-dev \
    gunicorn

WORKDIR /code
COPY ./src/backend /code/backend
COPY ../.docker /code/.docker
COPY ../Pipfile /code/
COPY ../Pipfile.lock /code/

EXPOSE 8000

RUN pipenv install
ENTRYPOINT ["/code/.docker/docker-entrypoint.sh"]