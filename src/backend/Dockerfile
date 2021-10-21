FROM python:3.9-slim-buster

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    # compiler for Python C modules
    g++ make libc6-dev

RUN python3.9 -m pip install pipenv

WORKDIR /code
COPY /src/backend /code/backend
COPY /.docker /code/.docker
COPY /Pipfile ../.env[t] /code/
COPY /Pipfile.lock /code/

EXPOSE 8000

RUN pipenv install

RUN chmod +x .docker/docker-entrypoint.sh
ENTRYPOINT [".docker/docker-entrypoint.sh"]