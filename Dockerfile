FROM python:2.7
MAINTAINER James Clemence

RUN apt-get update && apt-get install -y libmemcached-dev && rm -rf /var/lib/apt/lists/*
COPY ./requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt

RUN mkdir /app
WORKDIR /app
RUN useradd -rU wedding

ADD . /app/
COPY ./entrypoint.sh /usr/bin/entrypoint.sh
RUN python manage.py collectstatic --noinput
RUN python manage.py compress
RUN python -m whitenoise.compress /static

USER wedding

ENTRYPOINT ["/usr/bin/entrypoint.sh"]
