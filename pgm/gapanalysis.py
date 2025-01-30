import dash
from dash import dcc, html, Input, Output, State
import subprocess
import threading
import time

dash.register_page(__name__)

# 🔹 Layout Gap Analysis
layout = html.Div([
    html.H2("Analyse des écarts (Gap Analysis)", style={"fontFamily": "Arial"}),

    html.Button("Lancer Gap Analysis", id="btn-gap", style={"backgroundColor": "black", "color": "white"}),

    dcc.Progress(id="progress-gap", value=0, max=100),

    html.Div(id="output-gap")
])


# 🔹 Callback pour exécuter `gapanalysis.py`
@dash.callback(
    Output("progress-gap", "value"),
    Output("output-gap", "children"),
    Input("btn-gap", "n_clicks"),
    prevent_initial_call=True
)
def execute_gap(n_clicks):
    progress = 0

    def run_gap():
        nonlocal progress
        process = subprocess.Popen(["python", "gapanalysis.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                   text=True)

        for _ in range(5):
            progress += 20
            time.sleep(1)

        process.wait()
        progress = 100

    thread = threading.Thread(target=run_gap)
    thread.start()

    return progress, "✅ Gap Analysis terminé."
