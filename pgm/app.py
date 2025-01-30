import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import datapack, dataquality, gapanalysis  # Import des modules pour chaque onglet

app = dash.Dash(__name__, suppress_callback_exceptions=True)

# 🔹 Layout principal avec onglets
app.layout = html.Div([
    dcc.Tabs(id="tabs", value="datapack", children=[
        dcc.Tab(label="📦 Datapack", value="datapack"),
        dcc.Tab(label="📊 Data Quality", value="dataquality"),
        dcc.Tab(label="📉 Gap Analysis", value="gapanalysis"),
    ]),
    html.Div(id="tabs-content")
])

# 🔹 Callback pour afficher le bon contenu en fonction de l'onglet sélectionné
@app.callback(
    Output("tabs-content", "children"),
    Input("tabs", "value")
)
def render_tab_content(tab):
    if tab == "datapack":
        return datapack.layout
    elif tab == "dataquality":
        return dataquality.layout
    elif tab == "gapanalysis":
        return gapanalysis.layout

if __name__ == "__main__":
    app.run_server(debug=True)
