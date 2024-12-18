FROM python:3.13

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=softech.settings

WORKDIR /app

COPY req.txt /app/

RUN pip install -r req.txt

COPY . /app/

CMD python manage.py migrate && \
    python manage.py collectstatic --noinput && \
    python manage.py runserver 0.0.0.0:8002