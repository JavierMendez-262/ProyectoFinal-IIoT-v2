import dash
from dash.dependencies import Output, Input
import dash_core_components as dcc
import dash_html_components as html
import dash_table as dt
import plotly
from database import Database
import pandas as pd


def generate_html_table(max_rows=10):
    df = update_alerts()
    return html.Div(
        [
            html.Div(
                html.Table(
                    # Header
                    [html.Tr(
                        [
                            html.Th('ID'),
                            html.Th('Tipo de Sensor'),
                            html.Th('Temperatura'),
                            html.Th('Humedad'),
                            html.Th('Fecha y Hora'),
                        ]
                    )]
                    +
                    # Body
                    [
                        html.Tr(
                            [
                                html.Td(df.iloc[i]['id']),
                                html.Td(df.iloc[i]['sensor_type']),
                                html.Td(df.iloc[i]['temperature']),
                                html.Td(df.iloc[i]['humidity']),
                                html.Td(df.iloc[i]['datetime'])

                            ]
                        )
                        for i in range(min(len(df), max_rows))
                    ]
                ),
                style={'height': '150px', 'overflowY': 'scroll'},
            ),
        ],
        style={'height': '100%'},
    )

def update_alerts():
    db = Database()
    data = db.get_dict('alertsdata', 5)
    df = pd.DataFrame(data)
    if not df.empty:
        df = pd.DataFrame(df[['id', 'sensor_type', 'temperature', 'humidity', 'datetime']])
    return df


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H1(children='Dashboard', style={'textAlign': 'center'}),
    html.Div([
        html.Div([
            html.Div(
                children=[
                    html.H4('Últimas Lecturas del Sensor'),
                    dcc.Graph(id='live-update-graph-bar')
                ],
                className='six columns'
            )
        ]),
        html.Div([
            html.Div(
                children=[
                    html.H4('Últimas Alertas Registradas'),
                    html.Br(),html.Br(),html.Br(),html.Br(),
                    dt.DataTable(
                    id='live-update-table',
                    columns=[
                        {'name': 'ID', 'id': 'id'},
                        {'name': 'Tipo de Sensor', 'id': 'sensor_type'},
                        {'name': 'Temperatura', 'id': 'temperature'},
                        {'name': 'Humedad', 'id': 'humidity'},
                        {'name': 'Fecha y Hora', 'id': 'datetime'}
                    ],
                    data=[],
                    style_header= {'textAlign': 'center'}
                )],
                className='six columns'
            ),
        ]),
        dcc.Interval(
            id='interval-component',
            interval=1 * 1 * 1000,
            n_intervals=0
        )
    ])
])

@app.callback(Output('live-update-graph-bar', 'figure'), [Input('interval-component', 'n_intervals')])
def update_graph_bar(self):
    traces = list()

    db = Database()
    x_hours = db.get_datetime_dataset('01', quantity=24)
    y_humidity = db.get_sensor_dataset(id='01', is_temperature=False, quantity=24)
    y_temperature = db.get_sensor_dataset(id='01', is_temperature=True, quantity=24)

    y_humidity.reverse()
    y_temperature.reverse()
    x_hours.reverse()

    traces.append(plotly.graph_objs.Bar(
        x=x_hours,
        y=y_humidity,
        name='Humedad'
    ))
    traces.append(plotly.graph_objs.Bar(
        x=x_hours,
        y=y_temperature,
        name='Temperatura'
    ))
    layout = plotly.graph_objs.Layout(
        barmode='group'
    )
    return {'data': traces, 'layout': layout}

@app.callback(Output('live-update-table', 'data'), [Input('interval-component', 'n_intervals')])
def update_table(n_intervals):
    db = Database()
    data = db.get_dict('alertsdata', 5)
    df = pd.DataFrame(data)
    if not df.empty:
        df = pd.DataFrame(df[['id', 'sensor_type', 'temperature', 'humidity', 'datetime']])
    return df.to_dict('records')


if __name__ == '__main__':
    app.run_server(debug=True)