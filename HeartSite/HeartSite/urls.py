from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('heartPredictionApp.urls')),  # смотрим на файл urls в приложении
]
