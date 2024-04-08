from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # на главной странице отображаем метод index из views/index
    path('result', views.result, name='result')  # отображаем метод about из views/about
]