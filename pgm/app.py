import dash
from dash import dcc, html, Input, Output, ctx
import dash_bootstrap_components as dbc
from threading import Thread
from main import start_process, get_progress

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([
    html.H1("Titrisation", style={"background-color": "red", "color": "white", "padding": "10px"}),

    dcc.Tabs(id="tabs", value="datapack", children=[
        dcc.Tab(label="Datapack", value="datapack"),
        dcc.Tab(label="Data Quality", value="dataquality"),
        dcc.Tab(label="Gap Analysis", value="gapanalysis"),
    ]),

    html.Div(id="tab-content", style={"padding": "20px"}),

    html.Button("Lancer le traitement", id="btn-start",
                style={"background-color": "black", "color": "white", "margin-top": "20px"}),

    dbc.Progress(id="progress-bar", value=0, max=100, striped=True, animated=True,
                 style={"margin-top": "20px"}),

    html.Div(id="log-output", style={"margin-top": "10px", "font-size": "16px", "color": "blue"}),

    dcc.Interval(id="interval", interval=1000, n_intervals=0, disabled=True),
])

@app.callback(
    [Output("progress-bar", "value"),
     Output("log-output", "children"),
     Output("interval", "disabled")],
    [Input("btn-start", "n_clicks"),
     Input("interval", "n_intervals")]
)
def update_progress(n_clicks, n_intervals):
    trigger_id = ctx.triggered_id

    if trigger_id == "btn-start":
        # Lancer le traitement dans un thread séparé
        thread = Thread(target=start_process)
        thread.start()
        return 0, "🚀 Traitement en cours...", False  # Active l'intervalle

    elif trigger_id == "interval":
        # Mettre à jour la barre de progression
        progress_state = get_progress()
        progress = progress_state["progress"]
        message = progress_state["message"]

        if progress == 100:
            return progress, message, True  # Désactiver l'intervalle une fois terminé
        return progress, message, False

    return dash.no_update, dash.no_update, dash.no_update

if __name__ == "__main__":
    app.run_server(debug=True)
