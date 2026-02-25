FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 10000

CMD ["sh", "-c", "
python manage.py migrate &&
python manage.py collectstatic --noinput &&
python manage.py shell -c \"\
from django.contrib.auth import get_user_model; \
User = get_user_model(); \
import os; \
username=os.getenv('DJANGO_SUPERUSER_USERNAME'); \
email=os.getenv('DJANGO_SUPERUSER_EMAIL'); \
password=os.getenv('DJANGO_SUPERUSER_PASSWORD'); \
if username and not User.objects.filter(username=username).exists(): \
    User.objects.create_superuser(username, email, password)\" &&
gunicorn myproject.wsgi:application --bind 0.0.0.0:10000
"]