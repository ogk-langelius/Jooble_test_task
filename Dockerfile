FROM python:3.9-alpine
RUN apk update
RUN apk add postgresql-dev gcc python3-dev musl-dev

COPY requirements.txt api/requirements.txt

WORKDIR /api

RUN pip install -r requirements.txt

COPY . /api

