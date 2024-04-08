from django.contrib import admin
from .models import HeartData

@admin.register(HeartData)
class MyModelAdmin(admin.ModelAdmin):
    pass
