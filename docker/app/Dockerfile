# syntax=docker/dockerfile:1
FROM python:3.9.6-slim AS builder

# set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Create a group and user to run the app
ARG APP_USER=cellcountr
RUN groupadd -r ${APP_USER} && useradd --no-log-init -r -g ${APP_USER} ${APP_USER}

# install run dependencies
RUN set -ex \
    && RUN_DEPS=" \
    libpcre3 \
    mime-support \
    postgresql-client \
    " \
    && seq 1 8 | xargs -I{} mkdir -p /usr/share/man/man{} \
    && apt-get update && apt-get install -y --no-install-recommends $RUN_DEPS \
    && rm -rf /var/lib/apt/lists/*

# copy in requirements file
COPY requirements.txt /requirements.txt

# Install build deps, then run `pip install`, then remove unneeded build deps all in a single step.
# Correct the path to your production requirements file, if needed.
RUN set -ex \
    && BUILD_DEPS=" \
    build-essential \
    libpcre3-dev \
    libpq-dev \
    libmemcached-dev \
    zlib1g-dev \
    " \
    && apt-get update && apt-get install -y --no-install-recommends $BUILD_DEPS \
    && pip install --upgrade pip \
    && pip install --no-cache-dir -r /requirements.txt

# set work directory and copy project
ENV HOME=/usr/src/cellcounter
RUN mkdir $HOME
WORKDIR $HOME
COPY . $HOME


FROM builder AS prod

ARG APP_USER=cellcountr

# remove extraneous packages
RUN set -ex \
    && BUILD_DEPS=" \
    build-essential \
    libpcre3-dev \
    libpq-dev \
    libmemcached-dev \
    zlib1g-dev \
    " \
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false $BUILD_DEPS \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir $HOME/static
RUN chown ${APP_USER}:${APP_USER} $HOME/static

# Change to a non-root user
USER ${APP_USER}:${APP_USER}

ENTRYPOINT ["/usr/src/cellcounter/entrypoint.sh"]


FROM builder AS test

# copy in requirements file
COPY test-requirements.txt /test-requirements.txt

RUN set -ex \
    && pip install --no-cache-dir -r /test-requirements.txt

ENV TEST=True

ENTRYPOINT ["/usr/src/cellcounter/test-entrypoint.sh"]

