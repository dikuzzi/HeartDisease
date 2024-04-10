import pandas as pd

# Загрузка данных из CSV файла
df = pd.read_csv('heartPredictionApp/heart2.csv', sep=';')

# Вычисление медианного значения для столбца "холестерин", исключая нулевые значения
median_chol = df[df['Cholesterol'] != 0]['Cholesterol'].median()

# Замена нулевых значений на медианное значение
df.loc[df['Cholesterol'] == 0, 'Cholesterol'] = median_chol

# Сохранение данных обратно в CSV файл
df.to_csv('heartPredictionApp/heart2_MedianChol.csv', sep=';', index=False)