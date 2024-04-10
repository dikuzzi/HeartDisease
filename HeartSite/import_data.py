import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'HeartSite.settings')
from django import setup
setup()

import csv
from heartPredictionApp.models import HeartData



# with open('heartPredictionApp/heart2.csv', 'r') as csvfile:
#     reader = csv.DictReader(csvfile)
#     for row in reader:
#         obj = HeartData(
#             Age=row['Age'],  # Подставьте имя столбца из CSV файла
#             Sex=row['Sex'],
#             ChestPainType=row['ChestPainType'],
#             RestingBP=row['RestingBP'],
#             Cholesterol=row['Cholesterol'],
#             FastingBS=row['FastingBS'],
#             RestingECG=row['RestingECG'],
#             MaxHR=row['MaxHR'],
#             ExerciseAngina=row['ExerciseAngina'],
#             Oldpeak=row['Oldpeak'],
#             ST_Slope=row['ST_Slope'],
#             HeartDisease=row['HeartDisease'],
#         )
#         obj.save()

with open('heartPredictionApp/heart2_MedianChol.csv', 'r') as txtfile:
    # Читаем первую строку для получения названий колонок
    columns = txtfile.readline().strip().split(';')

    # Проходим по остальным строкам файла
    for line in txtfile:
        # Разделяем строку на данные, используя точку с запятой в качестве разделителя
        data = line.strip().split(';')

        data = [value.replace(',', '.') if ',' in value else value for value in data]

        # Создаем словарь, в котором ключи - это названия колонок, а значения - данные из строки
        row_data = dict(zip(columns, data))

        # Создаем объект модели и сохраняем его в базе данных
        obj = HeartData(**row_data)
        obj.save()

