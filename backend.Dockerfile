FROM python:3.9-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt .
RUN  pip3 install -r /app/requirements.txt --no-cache-dir

COPY . .

RUN python3 manage.py collectstatic --noinput
CMD ["gunicorn", "star_burger.wsgi:application", "--bind", "0:8000" ]
