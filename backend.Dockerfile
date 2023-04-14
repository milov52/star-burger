FROM --platform=linux/amd64 python:3.9-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /opt/backend

COPY requirements.txt .
RUN  pip3 install -r /opt/backend/requirements.txt --no-cache-dir

COPY . .

RUN python3 manage.py collectstatic --noinput
CMD ["gunicorn", "star_burger.wsgi:application", "--bind", "0:8000" ]
