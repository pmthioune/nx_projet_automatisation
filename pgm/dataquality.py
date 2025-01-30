import dash
from dash import dcc, html, Input, Output, State
import subprocess
import threading
import time

dash.register_page(__name__)

# 🔹 Layout Data Quality
layout = html.Div([
    html.H2("Contrôle Qualité des Données", style={"fontFamily": "Arial"}),

    html.Button("Lancer Analyse Qualité", id="btn-quality", style={"backgroundColor": "black", "color": "white"}),

    dcc.Progress(id="progress-quality", value=0, max=100),

    html.Div(id="output-quality")
])


# 🔹 Callback pour exécuter `dataquality.py`
@dash.callback(
    Output("progress-quality", "value"),
    Output("output-quality", "children"),
    Input("btn-quality", "n_clicks"),
    prevent_initial_call=True
)
def execute_quality(n_clicks):
    progress = 0

    def run_quality():
        nonlocal progress
        process = subprocess.Popen(["python", "dataquality.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                   text=True)

        for _ in range(5):
            progress += 20
            time.sleep(1)

        process.wait()
        progress = 100

    thread = threading.Thread(target=run_quality)
    thread.start()

    return progress, "✅ Analyse terminée."
