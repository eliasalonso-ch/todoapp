#!/bin/sh

python manage.py migrate
python manage.py collectstatic --noinput

python manage.py shell << END
from django.contrib.auth import get_user_model
import os

User = get_user_model()
username = os.getenv("DJANGO_SUPERUSER_USERNAME")
email = os.getenv("DJANGO_SUPERUSER_EMAIL")
password = os.getenv("DJANGO_SUPERUSER_PASSWORD")

if username and not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username, email, password)
END

gunicorn myproject.wsgi:application --bind 0.0.0.0:10000