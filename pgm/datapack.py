from dash import html, dcc, Output, Input, State
import dash_bootstrap_components as dbc
import time
import os

layout = html.Div([
    html.H4("Calcul des Indicateurs"),

    dcc.Dropdown(
        id="dropdown-indicateurs",
        options=[{"label": f"Indicateur {i}", "value": i} for i in range(1, 21)],
        placeholder="Sélectionnez les indicateurs",
        multi=True,
        style={"width": "50%"}
    ),
    html.Br(),

    html.Div([
        dbc.Progress(id="progress-bar", striped=True, animated=True, style={"height": "30px"}),
        html.Br(),
        dbc.Button("Lancer le programme", id="run-program-btn", color="primary"),
    ], style={"padding": "10px"})
])


def register_callbacks(app):
    @app.callback(
        [Output("progress-bar", "value"), Output("progress-bar", "label")],
        [Input("run-program-btn", "n_clicks")],
        [State("dropdown-indicateurs", "value")]
    )
    def run_program(n_clicks, selected_indicators):
        if not n_clicks:
            return 0, ""

        if not selected_indicators:
            return 0, "Sélectionnez des indicateurs."

        # Enregistrement des indicateurs sélectionnés
        with open("ind_config.py", "w") as f:
            f.write(f"SELECTED_INDICATORS = {selected_indicators}\n")

        # Exécution simulée avec barre de progression
        total_steps = 100
        for i in range(total_steps + 1):
            time.sleep(0.05)
            yield i, f"{i}%"

        os.system("python main.py")

        return 100, "Programme terminé."

