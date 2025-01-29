from dash import Dash, dcc, html
import dash_bootstrap_components as dbc
from datapack import layout as datapack_layout
from dataquality import layout as dataquality_layout
from gapanalysis import layout as gapanalyse_layout

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([
    html.Div(
        html.H1("Titrisation", style={"color": "white", "textAlign": "center", "padding": "10px"}),
        style={"backgroundColor": "rgb(233, 4, 30)"}
    ),
    dcc.Tabs(
        id="tabs",
        value="tab-datapack",
        children=[
            dcc.Tab(label="Datapack", value="tab-datapack", children=datapack_layout),
            dcc.Tab(label="Data Quality", value="tab-dataquality", children=dataquality_layout),
            dcc.Tab(label="Gap Analyse", value="tab-gapanalyse", children=gapanalyse_layout),
        ]
    )
])

if __name__ == "__main__":
    app.run_server(debug=True)
