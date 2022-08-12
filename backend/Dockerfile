# syntax=docker/dockerfile:1
FROM python:3.9

RUN apt-get update

COPY requirements.txt requirements.txt
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .

WORKDIR /app