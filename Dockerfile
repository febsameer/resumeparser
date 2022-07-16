FROM python:3.7.9-slim

RUN mkdir -p /usr/src/app

WORKDIR /usr/src/app

COPY . /usr/src/app

RUN pip install -r /usr/src/app/requirements.txt

RUN python /usr/src/app/pre_requisites.py

RUN python /usr/src/app/app.py