from django.contrib import admin
from django.urls import path
from . import views
from .views import admin_panel_redirect


urlpatterns = [
    path('admin/', admin_panel_redirect, name='admin_panel'),
    path('', views.index, name='index'),  # на главной странице отображаем метод index из views/index
    path('result', views.result, name='result'),
    path('data', views.heart_data_list, name='heart_data_list'),
    path('dashboard/', views.dashboard, name='dashboard'),
]