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

data = pd.read_csv('heart2_MedianChol.csv', sep=';', header=0)

def update_graph(min_age, max_age, sex):
    if (sex == 'M'):
        sexName = 'мужчин'
    else:
        sexName = 'женщин'
    filtered_data = data[(data['Age'] >= min_age) & (data['Age'] <= max_age) & (data['Sex'] == sex)]
    fig = px.histogram(filtered_data, x="Age", color="HeartDisease", barmode="overlay",
                       title=f"Распределение возраста среди {sexName} с/без сердечного заболевания (возраст {min_age}-{max_age} лет)")
    return fig

app = dash.Dash(__name__)

app.layout = html.Div(children=[
    html.H1('Мой дашборд'),

    dcc.RangeSlider(
        id='age-slider',
        min=data['Age'].min(),
        max=data['Age'].max(),
        value=[data['Age'].min(), data['Age'].max()],
        marks={i: str(i) for i in range(data['Age'].min(), data['Age'].max() + 1)},
        step=1
    ),

    html.Br(),  # Добавляем разрыв строки

    dcc.RadioItems(  # Добавляем радиокнопку
        id='sex-radio',
        options=[
            {'label': 'Мужчина', 'value': 'M'},
            {'label': 'Женщина', 'value': 'F'}
        ],
        value='M',  # Устанавливаем значение по умолчанию
        labelStyle={'display': 'inline-block'}  # Размещаем кнопки в строку
    ),

    dcc.Graph(
        id='example-graph'
    ),
])

@app.callback(
    Output('example-graph', 'figure'),
    [Input('age-slider', 'value'),
     Input('sex-radio', 'value')]
)
def update_output(age_value, sex_value):
    return update_graph(age_value[0], age_value[1], sex_value)

if __name__ == '__main__':
    app.run_server(debug=True)