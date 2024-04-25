from django.contrib import admin
from django.urls import path
# from django_dash.urls import urlpatterns as django_dash_urls
from . import views
from .views import admin_panel_redirect
# from .views import dashboard_view


urlpatterns = [
    path('admin/', admin_panel_redirect, name='admin_panel'),
    path('', views.index, name='index'),  # на главной странице отображаем метод index из views/index
    path('result', views.result, name='result'),  # отображаем метод about из views/about
    path('data', views.heart_data_list, name='heart_data_list'),
    path('dashboard/', views.dashboard, name='dashboard'),
]