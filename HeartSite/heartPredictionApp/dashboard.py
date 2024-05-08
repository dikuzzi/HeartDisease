import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
import hvplot.pandas
import sqlite3
import numpy as np
import panel as pn
import plotly.express as px

body_style = {
    'font-family': 'system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", "Noto Sans", "Liberation Sans", Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol", "Noto Color Emoji"',
}

# Стили для заголовка h1
h1_style = {
    #'font-family': 'system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", "Noto Sans",
    # "Liberation Sans", Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol", "Noto Color Emoji"',
    'color': '#0d6efd',  # Цвет текста
    'font-size': '36px',  # Размер шрифта
    'text-align': 'center',  # Выравнивание текста
    'margin-top': '20px',  # Отступ сверху
    'margin-bottom': '20px'  # Отступ снизу
}

flexBoxMain_style = {
    'display': 'flex',
    'width': '100%',
}

leftBox_style = {
    'min-width': '400px',
}

description = {
    'position': 'fixed',
    'padding-left': '20px',
    'top': '60px',
    'width': '380px',
}

description_title = {
    # 'position': 'fixed',
    'font-size': '24px',

}

description_text = {
    # 'position': 'fixed',
    'font-size': '16px',
}

slider_title = {
    'font-size': '20px',
    'padding-left': '20px',
    'top': '440px',
    'position': 'fixed',
}

slider_style = {
    'position': 'fixed',
    'width': '400px',
    'top': '500px',
}

rightBox_style = {
    'width': '1500px',
}

flexGraph_style = {
    'display': 'flex',
    'max-width': '200px',
    'display': 'flex',
}

flexGraph2_style = {
    'display': 'flex',
}

# читаем данные из файла
data = pd.read_csv('heart2_MedianChol.csv', sep=';', header=0)

expanded_data = pd.concat([pd.DataFrame({'Age': range(row['Age'], row['Age'] + 1), **row.drop('Age')})
                           for _, row in data.iterrows()], ignore_index=True)


def update_age_graph(min_age, max_age, sex):
    if (sex == 'M'):
        sexName = 'мужчин'
    else:
        sexName = 'женщин'
    filtered_data = data[(data['Age'] >= min_age) & (data['Age'] <= max_age) & (data['Sex'] == sex)]
    fig = px.histogram(filtered_data, x="Age", color="HeartDisease", barmode="overlay",
                       title=f"Распределение возраста среди {sexName} с/без сердечного заболевания")
    return fig

# Создание функции для обновления графика по типам болей в груди
def update_chest_pain_graph(min_age, max_age, sex):
    if (sex == 'M'):
        sexName = 'мужчин'
    else:
        sexName = 'женщин'

    filtered_data = data[(data['Age'] >= min_age) & (data['Age'] <= max_age) & (data['Sex'] == sex)]
    chest_pain_counts = filtered_data.groupby('ChestPainType').size().reset_index(name='Count')
    fig = px.bar(chest_pain_counts, x='ChestPainType', y='Count',
                 title=f"Количество людей с разными типами болей в груди среди {sexName}")
    return fig

app = dash.Dash(__name__)

app.layout = html.Div(children=[
    html.H1('Дашборд', style=h1_style),

    html.Div(children=[
        html.Div(children=[
            html.Div(children=[
                html.H2('Сердечно-сосудистые заболевания', style=description_title),

                html.P('Сердечно-сосудистые заболевания (ССЗ) являются причиной смерти номер 1 во всем мире, ежегодно унося, по оценкам, 17,9 миллиона жизней, что составляет 31% всех смертей во всем мире. Сердечная недостаточность - распространенное явление, вызываемое ССЗ. Люди с сердечно-сосудистыми заболеваниями или с высоким сердечно-сосудистым риском (из-за наличия одного или нескольких факторов риска, таких как гипертония, диабет, гиперлипидемия или уже выявленное заболевание) нуждаются в раннем выявлении и лечении, в чем модель машинного обучения может оказать большую помощь.',
                   style=description_text),
            ], style=description),



            html.H3('Возраст', style=slider_title),

            html.Div(children=[
                dcc.RangeSlider(
                    id='age-slider',
                    min=data['Age'].min(),
                    max=data['Age'].max(),
                    value=[data['Age'].min(), data['Age'].max()],
                    marks={i: str(i) for i in range(data['Age'].min(), data['Age'].max() + 1, 2)},
                    step=1
                ),
            ], style=slider_style),

            # dcc.RangeSlider(
            #     id='age-slider',
            #     min=data['Age'].min(),
            #     max=data['Age'].max(),
            #     value=[data['Age'].min(), data['Age'].max()],
            #     marks={i: str(i) for i in range(data['Age'].min(), data['Age'].max() + 1, 2)},
            #     step=1
            # ),
        ], style=leftBox_style),

        html.Div(children=[
            dcc.RadioItems(  # Добавляем радиокнопку
                id='sex-radio',
                options=[
                    {'label': 'Мужчины', 'value': 'M'},
                    {'label': 'Женщины', 'value': 'F'}
                ],
                value='M',  # Устанавливаем значение по умолчанию
                labelStyle={'display': 'inline-block'}  # Размещаем кнопки в строку
            ),

            html.Div(children=[
                dcc.Graph(
                    id='age-graph'
                ),

                dcc.Graph(
                    id='chest-pain-graph'
                ),
            ], style=flexGraph_style),

            html.Div(children=[
                # dcc.Graph(
                #     id='age-hr-graph'
                # ),
                dcc.Graph(id='maxhr-oldpeak-scatter'),

                dcc.Graph(id='gender-pie-chart'),
            ], style=flexGraph2_style),


        ], style=rightBox_style),
    ], style=flexBoxMain_style),



    #html.Br(),


], style=body_style)

@app.callback(
    Output('age-graph', 'figure'),
    [Input('age-slider', 'value'),
     Input('sex-radio', 'value')]
)

def update_age_output(age_value, sex_value):
    return update_age_graph(age_value[0], age_value[1], sex_value)

@app.callback(
    Output('chest-pain-graph', 'figure'),
    [Input('age-slider', 'value'),
     Input('sex-radio', 'value')]
)

def update_chest_pain_output(age_value, sex_value):
    return update_chest_pain_graph(age_value[0], age_value[1], sex_value)



@app.callback(
    Output('gender-pie-chart', 'figure'),
    [Input('age-slider', 'value')]
)
def update_gender_pie_chart(age_value):
    filtered_data = data[(data['Age'] >= age_value[0]) & (data['Age'] <= age_value[1])]
    gender_counts = filtered_data['Sex'].value_counts()
    fig = px.pie(names=gender_counts.index, values=gender_counts.values, title=f'Половое распределение (возраст {age_value[0]}-{age_value[1]} лет)')
    return fig


@app.callback(
    Output('maxhr-oldpeak-scatter', 'figure'),
    [Input('age-slider', 'value')]
)
def update_maxhr_oldpeak_scatter(age_value):
    filtered_data = data[(data['Age'] >= age_value[0]) & (data['Age'] <= age_value[1])]

    # Преобразуем столбец 'Oldpeak' к числовому типу данных
    filtered_data['Oldpeak'] = pd.to_numeric(filtered_data['Oldpeak'], errors='coerce')

    # Сортируем отрицательные значения Oldpeak в обратном порядке
    filtered_data_neg = filtered_data[filtered_data['Oldpeak'] < 0].sort_values(by='Oldpeak', ascending=False)

    # Сортируем положительные значения Oldpeak в обычном порядке
    filtered_data_pos = filtered_data[filtered_data['Oldpeak'] >= 0].sort_values(by='Oldpeak')

    # Объединяем отсортированные данные
    sorted_data = pd.concat([filtered_data_neg, filtered_data_pos])

    fig = px.scatter(sorted_data, x='MaxHR', y='Oldpeak',
                     title=f'Зависимость Oldpeak от MaxHR ({age_value[0]}-{age_value[1]} лет)',
                     labels={'MaxHR': 'Максимальный пульс', 'Oldpeak': 'Oldpeak'},
                     color=sorted_data['HeartDisease'],)  # Окраска точек в зависимости от HeartDisease
                     #color_discrete_map={0: 'blue', 1: 'red'},
                     # Задаем цвета для каждого значения HeartDisease
                     #color_continuous_scale=False)  # Отключаем использование цветовой палитры
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)