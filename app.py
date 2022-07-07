import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from preprocessing import preprocessing
import plotly.express as px
import pandas as pd

app = dash.Dash(
    __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}]
)
data = preprocessing()
server = app.server

'''app.layout = html.Div([
    html.Div(children=[
        html.Label('항목'),
        dcc.Dropdown(
            ['승률', '픽률', '평균 킬', '평균 순위'],
            '평균 킬'),
        html.Br(),
        html.Label('게임 유형'),
        dcc.Dropdown(
            ['솔로', '듀오', '스쿼드'],
            ['솔로'], multi=True)
    ], style={'padding': 10, 'flex': 1})
], style={'padding': 10, 'flex': 1})
'''
app = dash.Dash(__name__)
app.layout = html.Div(
    children=[
        # Error Message
        html.Div(id="error-message"),

        # Top Banner
        html.Div(
            className="er-stat-banner row",
            children=[
                html.H2(className="h2-title", children="ER STAT BROWSER"),
                #html.Div(
                #    className="div-logo",
                #    children=html.Img(
                #        className="logo", src=app.get_asset_url("dash-logo-new.png")
                #    ),
                #),
                #html.H2(className="h2-title-mobile", children="ER STAT BROWSER"),
            ],
        ),
        
        # Body of the App
        html.Div(
            className="row app-body",
            children=[
                # User Controls
                html.Div(
                    className="four columns card",
                    children=[
                        html.Div(
                            className="bg-white user-control",
                            children=[
                                html.Div(
                                    className="padding-top-bot",
                                    children=[
                                        html.H6("카테고리"),
                                        dcc.Dropdown(id="cat-dropdown",
                                                     options=[{'label': '승률',
                                                               'value': '승률'},
                                                              {'label': '픽률',
                                                              'value': '픽률'},
                                                              {'label': '평균 킬',
                                                              'value': '평균 킬'},
                                                              {'label':'평균 순위',
                                                              'value': '평균 순위'}],
                                                     value='승률'),
                                    ],
                                ),
                                html.Div(
                                    className="padding-top-bot",
                                    children=[
                                        html.H6("게임 유형"),
                                        dcc.RadioItems(
                                            id="chart-type",
                                            options=[
                                                {"label": "솔로", "value": "솔로"},
                                                {
                                                    "label": "듀오",
                                                    "value": "듀오",
                                                },
                                                {'label': '스쿼드',
                                                 'value': '스쿼드'}
                                            ],
                                            value="solo",
                                            labelStyle={
                                                "display": "inline-block",
                                                "padding": "12px 12px 12px 0px",
                                            },
                                        ),
                                    ],
                                ),
                            ],
                        )
                    ],
                ),
                # Graph
                html.Div(
                    className="eight columns card-left",
                    children=[
                        html.Div(
                            className="bg-white",
                            children=[
                                html.H5("stat plot"),
                                dcc.Graph(id="plot"),
                            ],
                        )
                    ],
                ),
                dcc.Store(id="error", storage_type="memory"),
            ],
        ),
    ]
)

@app.callback(
    Output('plot', 'figure'),
    Input('cat-dropdown', 'value')
)
def update_figure(category):
    df = pd.concat([data[category].iloc[:,0], data['캐릭터-무기']], axis=1)
    fig = px.bar(df, x='캐릭터-무기', y=category)
    fig.update_layout(transition_duration=500)
    return fig
    

if __name__ == "__main__":
    app.run_server(debug=True)