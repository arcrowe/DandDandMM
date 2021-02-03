import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
from django_plotly_dash import DjangoDash
from datetime import datetime
import pandas_datareader.data as web
import os
# print(f" IEX KEY {os.environ.get('IEXCLOUD_KEY')}")
IEX_KEY = os.environ.get('IEXCLOUD_KEY')
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = DjangoDash('SimpleExample', external_stylesheets=external_stylesheets)

company_symbol = ['SPY', 'VPMAX', 'CVX', 'VDADX', 'GOOG', 'VBTLX', 'VFSUX', 'VTABX', 'VTAPX']
company_name = ['S & P 500', 'Vanguard PrimeCap', 'Chevron', 'Vanguard Dividend Appreciation', 'Google',
                'Vanguard Total Bond', 'Vanguard Short-Term', 'Vanguard Intl Bond',
                'Vanguard TIPS'
                ]

selection_co = [{'label': name + ' : ' + sym, 'value': sym} for sym, name in zip(company_symbol, company_name)]

#
app.layout = html.Div([
    html.Div([
        html.H1('Stock Ticker Dashboard')
    ], className='title'),
    html.Div([
        html.H3('Choose a stock symbol: '),
        dcc.Dropdown(id='select_co', options=selection_co, value=['SPY'], className='dropdown',
                     multi=True),
    ], className='selectors'),
    html.Div([
        html.H3('Choose a start and end date: '),
        dcc.DatePickerRange(
            id='my-date-picker-range',
            min_date_allowed=datetime(1995, 8, 5),
            max_date_allowed=datetime.today(),
            start_date=datetime(2017, 1, 21),
            end_date=datetime.today()
        ),
    ], className='selectors'),
    html.Div([
        html.Button(id='submit-button', n_clicks=0, children='Submit', className='mybutton'),
    ], className='selectors selectors2'),
    html.H1(id='my_output'),
    dcc.Graph(id='my_graph')

])


@app.callback(
    Output('my_graph', 'figure'),
    [Input('submit-button', 'n_clicks')],
    [State('my-date-picker-range', 'start_date'),
     State('my-date-picker-range', 'end_date'),
     State(component_id='select_co', component_property='value')])
def graph(n_clicks, start_date, end_date, companies):
    start = datetime.strptime(start_date[:10], '%Y-%m-%d')
    end = datetime.strptime(end_date[:10], '%Y-%m-%d')
    traces = []
    for company in companies:
        df = web.DataReader(company, 'iex', start, end, api_key=IEX_KEY)
        data = go.Scatter(
            x=df.index, y=df.close, name=company,
            mode='lines')
        traces.append(data)
    fig = {
        'data': traces,
        'layout': {'title': ', '.join(companies) + ' Closing Prices'}
    }
    return fig
