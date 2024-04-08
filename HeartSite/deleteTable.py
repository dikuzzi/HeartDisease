import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'HeartSite.settings')
from django import setup
setup()

from django.db import connection
from heartPredictionApp.models import HeartData

HeartData.objects.all().delete()

# Сброс данных в базе данных SQLite
from django.db import connection
with connection.cursor() as cursor:
    cursor.execute("VACUUM;")