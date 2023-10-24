FROM python:3.11-slim-buster

# set work directory
WORKDIR /project/

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
COPY Pipfile Pipfile.lock /project/

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        gcc \
        python3-dev \
        musl-dev \
        libffi-dev \
        postgresql-client \
        libpq-dev \
        libjpeg-dev \
        zlib1g-dev \
        git \
        libpq-dev && \
    pip install --upgrade pip && \
    pip install  -U  pipenv

# install project dependencies
RUN pipenv install --system --dev

# copy project
COPY . /project/
RUN ls
