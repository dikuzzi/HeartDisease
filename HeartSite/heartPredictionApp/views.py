from django.shortcuts import render
from django.http import HttpResponse
from .models import HeartData
import csv

import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, roc_auc_score, precision_score, recall_score, f1_score, \
    RocCurveDisplay
from sklearn.model_selection import train_test_split, RepeatedStratifiedKFold, cross_val_score

pd.options.display.float_format = '{:.2f}'.format
import warnings

warnings.filterwarnings('ignore')
import joblib
from sklearn.preprocessing import MinMaxScaler, StandardScaler
import pickle


def index(request):
    return render(request, 'heartPredictionApp/index.html')  # передаем наш html файл из папки templates



def result(request):
    if request.method == 'POST':
        # num1 = float(request.POST['num1'])
        # num2 = float(request.POST['num2'])

        all_data = HeartData.objects.all() # загрузка данных из БД
        data = pd.DataFrame(list(all_data.values())) # преобразование в датафрейм

        # data = pd.read_csv('HeartSite/heartPredictionApp/heart.csv') # загружаю данные из файла

        mms = MinMaxScaler()  # Normalization
        ss = StandardScaler()  # Standardization

        df1 = data.copy(deep=True)

        sex_mapping = {'M': 0, 'F': 1}
        ChestPainType_mapping = {'ATA': 0, 'NAP': 1, 'ASY': 2, 'TA': 3}
        RestingECG_mapping = {'Normal': 0, 'ST': 1, 'LVH': 2}
        ExerciseAngina_mapping = {'N': 0, 'Y': 1}
        ST_Slope_mapping = {'Up': 0, 'Flat': 1, 'Down': 2}

        df1['Sex'] = df1['Sex'].map(sex_mapping)
        df1['ChestPainType'] = df1['ChestPainType'].map(ChestPainType_mapping)
        df1['ExerciseAngina'] = df1['ExerciseAngina'].map(ExerciseAngina_mapping)
        df1['ST_Slope'] = df1['ST_Slope'].map(ST_Slope_mapping)

        df1['Oldpeak'] = mms.fit_transform(df1[['Oldpeak']])
        df1['Age'] = ss.fit_transform(df1[['Age']])
        df1['Cholesterol'] = ss.fit_transform(df1[['Cholesterol']])
        df1['MaxHR'] = ss.fit_transform(df1[['MaxHR']])

        features = df1[df1.columns.drop(['HeartDisease', 'RestingBP', 'RestingECG', 'id'])].values
        target = df1['HeartDisease'].values
        x_train, x_test, y_train, y_test = train_test_split(features, target, test_size=0.20, random_state=2)

        def model(classifier):

            classifier.fit(x_train, y_train)
            prediction = classifier.predict(x_test)
            cv = RepeatedStratifiedKFold(n_splits=10, n_repeats=3, random_state=1)

        classifier_lr = LogisticRegression(random_state=0, C=1, penalty='l2')
        model(classifier_lr)

        in_Age = request.POST['num1']
        in_Sex = request.POST['num2']
        in_ChestPainType = request.POST['num3']
        in_Cholesterol = request.POST['num4']
        in_FastingBS = request.POST['num5']
        in_MaxHR = request.POST['num6']
        in_ExerciseAngina = request.POST['num7']
        in_Oldpeak = request.POST['num8']
        in_ST_Slope = request.POST['num9']

        newDict = {"Age": in_Age, "Sex": in_Sex, "ChestPainType": in_ChestPainType,
                   "Cholesterol": in_Cholesterol, "FastingBS": in_FastingBS, "MaxHR": in_MaxHR,
                   "ExerciseAngina": in_ExerciseAngina, "Oldpeak": in_Oldpeak,
                   "ST_Slope": in_ST_Slope}  # новая строка

        df2 = data.copy(deep=True)
        columns_to_drop = ['HeartDisease', 'RestingBP', 'RestingECG', 'id']
        df2.drop(columns=columns_to_drop, axis=1, inplace=True)

        # df2 = df4[df4.columns.drop(['HeartDisease', 'RestingBP', 'RestingECG'])].values
        df2 = df2._append(newDict, ignore_index=True)

        df2['Sex'] = df2['Sex'].map(sex_mapping)
        df2['ChestPainType'] = df2['ChestPainType'].map(ChestPainType_mapping)
        df2['ExerciseAngina'] = df2['ExerciseAngina'].map(ExerciseAngina_mapping)
        df2['ST_Slope'] = df2['ST_Slope'].map(ST_Slope_mapping)

        df2['Oldpeak'] = mms.fit_transform(df2[['Oldpeak']])
        df2['Age'] = ss.fit_transform(df2[['Age']])
        df2['Cholesterol'] = ss.fit_transform(df2[['Cholesterol']])
        df2['MaxHR'] = ss.fit_transform(df2[['MaxHR']])

        last_row = df2.tail(1)
        df2 = last_row

        predicted_output = classifier_lr.predict(df2)

        result2 = "error"
        if predicted_output[0] == 0:
            result2 = 'Нет ишемической болезни сердца'
            color = 'green'
        elif predicted_output[0] == 1:
            color = 'red'
            result2 = 'Есть ишемическая болезнь сердца'

        return render(request, 'heartPredictionApp/result.html', {'result': result2, 'color': color})
    return HttpResponse('Method Not Allowed')


# def result(request):
#     if request.method == 'POST':
#         # num1 = float(request.POST['num1'])
#         # num2 = float(request.POST['num2'])
#
#         mms = MinMaxScaler()  # Normalization
#         ss = StandardScaler()  # Standardization
#
#         sex_mapping = {'M': 0, 'F': 1}
#         ChestPainType_mapping = {'ATA': 0, 'NAP': 1, 'ASY': 2, 'TA': 3}
#         RestingECG_mapping = {'Normal': 0, 'ST': 1, 'LVH': 2}
#         ExerciseAngina_mapping = {'N': 0, 'Y': 1}
#         ST_Slope_mapping = {'Up': 0, 'Flat': 1, 'Down': 2}
#
#         classifier_lr = joblib.load('HeartSite/heartPredictionApp/my_model1.joblib')
#
#         newData = pd.DataFrame({'Age': [28, 77], 'Sex': ["M", "M"],
#                                 'ChestPainType': ['ASY', 'ASY'], 'Cholesterol': [0, 603], 'FastingBS': [0, 1],
#                                 'MaxHR': [60, 202], 'ExerciseAngina': ['Y', 'Y'], 'Oldpeak': [-2.6, 6.2],
#                                 'ST_Slope': ['Flat', 'Flat']})
#
#         in_Age = request.POST['num1']
#         in_Sex = request.POST['num2']
#         in_ChestPainType = request.POST['num3']
#         in_Cholesterol = request.POST['num4']
#         in_FastingBS = request.POST['num5']
#         in_MaxHR = request.POST['num6']
#         in_ExerciseAngina = request.POST['num7']
#         in_Oldpeak = request.POST['num8']
#         in_ST_Slope = request.POST['num9']
#
#         newDict = {"Age": in_Age, "Sex": in_Sex, "ChestPainType": in_ChestPainType,
#                    "Cholesterol": in_Cholesterol, "FastingBS": in_FastingBS, "MaxHR": in_MaxHR,
#                    "ExerciseAngina": in_ExerciseAngina, "Oldpeak": in_Oldpeak,
#                    "ST_Slope": in_ST_Slope}  # новая строка
#         newData = newData._append(newDict, ignore_index=True)
#
#         dfNew = newData.copy(deep=True)
#
#         dfNew['Sex'] = dfNew['Sex'].map(sex_mapping)
#         dfNew['ChestPainType'] = dfNew['ChestPainType'].map(ChestPainType_mapping)
#         dfNew['ExerciseAngina'] = dfNew['ExerciseAngina'].map(ExerciseAngina_mapping)
#         dfNew['ST_Slope'] = dfNew['ST_Slope'].map(ST_Slope_mapping)
#         dfNew['Oldpeak'] = mms.fit_transform(dfNew[['Oldpeak']])
#         dfNew['Age'] = ss.fit_transform(dfNew[['Age']])
#         dfNew['Cholesterol'] = ss.fit_transform(dfNew[['Cholesterol']])
#         dfNew['MaxHR'] = ss.fit_transform(dfNew[['MaxHR']])
#
#         dfNew.drop(1, inplace=True)
#         dfNew.drop(0, inplace=True)
#
#         predicted_output = classifier_lr.predict(dfNew)
#
#         result2 = "error"
#         if predicted_output[0] == 0:
#             result2 = 'Нет ишемической болезни сердца'
#             color = 'green'
#         elif predicted_output[0] == 1:
#             color = 'red'
#             result2 = 'Есть ишемическая болезнь сердца'
#
#         return render(request, 'heartPredictionApp/result.html', {'result': result2, 'color': color})
#     return HttpResponse('Method Not Allowed')

