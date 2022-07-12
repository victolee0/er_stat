import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from preprocessing import preprocessing
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from crawl import crawl
app = dash.Dash(
    __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}]
)

crawl_data = crawl()
print("Load data success.")
server = app.server
print("Define flask server")


app.layout = html.Div(
    children=[
        html.Title(children="ER-STAT"),
        # Top Banner
        html.Div(
            className="er-stat-banner row",
            children=[
                html.H2(className="h2-title", children="ER STAT"),
                #html.Div(
                #    className="div-logo",
                #    children=html.Img(
                #        className="logo", src=app.get_asset_url("dash-logo-new.png")
                #    ),
                #),
                html.H2(className="h2-title-mobile", children="ER STAT"),
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
                                        html.H4("카테고리"),
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
                                        html.H4("게임 유형"),
                                        dcc.RadioItems(
                                            id="game-type",
                                            options=[
                                                {"label": "솔로", "value": "솔로"},
                                                {
                                                    "label": "듀오",
                                                    "value": "듀오",
                                                },
                                                {'label': '스쿼드',
                                                 'value': '스쿼드'}
                                            ],
                                            value="솔로",
                                            labelStyle={
                                                "display": "inline-block",
                                                "padding": "12px 12px 12px 0px",
                                            },
                                        ),
                                    ],
                                ),
                                 html.Div(
                                    className="padding-top-bot",
                                    children=[
                                        html.H4("랭크 유형"),
                                        dcc.RadioItems(
                                            id="rank-type",
                                            options=[
                                                {"label": "전체", "value": "all"},
                                                {"label": "탑1000", "value": "top",}
                                            ],
                                            value="all",
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
                            className="bg-white-plot",
                            children=[
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
    [Input('cat-dropdown', 'value'),
     Input('game-type', 'value'),
     Input('rank-type', 'value')]
)

#todo: page title, footer
def update_figure(category, gametype, ranktype):
    type_dict = {'솔로': 0,
                 '듀오': 1,
                 '스쿼드': 2}
    
    date, data = preprocessing(crawl_data, ranktype)
    print("data preprocessing success")
    df = pd.concat([data[category].iloc[:,type_dict[gametype]], data['캐릭터-무기']], axis=1)
    if category in ['승률', '픽률']:
        df[category] = df[category].apply(lambda x: float(x.split('%')[0]))
        df = df.sort_values(by=[category])
        df[category] = df[category].apply(lambda x: str(x) + '%')
    else:
        df = df.sort_values(by=[category])
    colors = df['캐릭터-무기'].apply(lambda x: '#F0C522' if x == '평균' else '#636efa')
    

    fig = px.bar(df, y='캐릭터-무기', x=category, orientation='h', text=category,
                 title=date, height=1500)
    
    fig.update_layout(transition_duration=500)
    fig.update_xaxes(showticklabels=False)
    fig.update_traces(textposition = 'outside', marker_color=colors)
    print('update plot')
    return fig


if __name__ == "__main__":
    app.run_server(debug=True)