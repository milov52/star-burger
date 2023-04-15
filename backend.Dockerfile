FROM --platform=linux/amd64  python:3.9-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt .
RUN  pip3 install -r /app/requirements.txt --no-cache-dir

COPY . .
RUN python ./manage.py collectstatic --noinput


