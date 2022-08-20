# syntax=docker/dockerfile:1
FROM ubuntu:20.04
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Timezone & locale configuration required for GDAL
# https://github.com/thinkWhere/GDAL-Docker/blob/develop/3.8-ubuntu/Dockerfile
ENV TZ 'BE'
ENV LC_ALL='fr_BE.utf8'
RUN apt-get update && \
    apt-get install -y locales tzdata && \
    echo $TZ > /etc/timezone && \
    rm /etc/localtime && \
    ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && \
    dpkg-reconfigure -f noninteractive tzdata && \
    locale-gen $LC_ALL

RUN apt-get update && \
    apt-get install -y python3-pip libgdal-dev

RUN cd /usr/bin && \
    ln -s python3 python

ENV CPLUS_INCLUDE_PATH=/usr/include/gdal
ENV C_INCLUDE_PATH=/usr/include/gdal

WORKDIR /code
RUN mkdir /code/mediafiles
COPY requirements.txt /code/
RUN pip install -r requirements.txt

COPY . /code/
CMD python manage.py makemigrations && python manage.py migrate && python manage.py runserver 0.0.0.0:8000