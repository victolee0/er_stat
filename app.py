import dash
import dash_core_components as dcc
import dash_html_components as html
from preprocessing import preprocessing
import plotly.express as px

app = dash.Dash(
    __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}]
)

app.layout = html.Div([
    html.Div(children=[
        html.Label('항목'),
        dcc.Dropdown(
            id='category',
            options=['승률', '픽률', '평균 킬', '평균 순위'],
            value = '평균 킬'),
        html.Br(),
        html.Label('게임 유형'),
        dcc.Dropdown(
            id='type',
            options=['솔로', '듀오', '스쿼드'],
            value= ['솔로'], multi=True)
    ], style={'padding': 10, 'flex': 1})
], style={'padding': 10, 'flex': 1})

if __name__ == "__main__":
    app.run_server(debug=True)