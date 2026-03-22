# syntax=docker/dockerfile:1
FROM ubuntu:20.04

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    TZ='BE' \
    LC_ALL='fr_BE.utf8' \
    DEBIAN_FRONTEND=noninteractive \
    CPLUS_INCLUDE_PATH=/usr/include/gdal \
    C_INCLUDE_PATH=/usr/include/gdal

RUN apt-get update && \
    apt-get install -y --no-install-recommends locales tzdata wget gnupg2 ca-certificates && \
    echo $TZ > /etc/timezone && \
    rm /etc/localtime && \
    ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && \
    dpkg-reconfigure -f noninteractive tzdata && \
    locale-gen $LC_ALL && \
    wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add - && \
    echo "deb http://apt-archive.postgresql.org/pub/repos/apt/ focal-pgdg main" > /etc/apt/sources.list.d/pgdg.list && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        cron \
        python3-pip \
        python3-dev \
        build-essential \
        libpq-dev \
        libgdal-dev \
        tesseract-ocr \
        libtesseract-dev \
        postgresql-client-14 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN cd /usr/bin && \
    ln -s python3 python

WORKDIR /code
RUN mkdir -p /code/mediafiles /static /code/backups

COPY requirements.txt /code/
RUN pip install --no-cache-dir "setuptools<58.0.0"
RUN pip install --no-cache-dir --default-timeout=1000 -r requirements.txt

RUN echo "*/5 * * * * cd /code && /usr/bin/python3 manage.py runcrons >> /code/cron.log 2>&1" > /etc/cron.d/django-cron && \
    chmod 0644 /etc/cron.d/django-cron && \
    crontab /etc/cron.d/django-cron

COPY . /code/

CMD cron && python manage.py makemigrations && python manage.py migrate && python manage.py collectstatic --noinput && python manage.py runserver 0.0.0.0:8000