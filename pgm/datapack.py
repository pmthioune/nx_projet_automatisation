import dash
from dash import dcc, html, Input, Output, State
import subprocess
import time
import threading

dash.register_page(__name__)

# 🔹 Layout de l'onglet Datapack
layout = html.Div([
    html.H2("Titrisation",
            style={"backgroundColor": "red", "color": "white", "padding": "10px", "fontFamily": "Montserrat"}),

    dcc.Input(id="input-id-datapack", type="number", placeholder="ID Datapack"),
    dcc.Dropdown(id="dropdown-datapack", options=[
        {"label": "RACER", "value": "RACER"},
        {"label": "JUNON", "value": "JUNON"}
    ], value="RACER"),

    dcc.DatePickerRange(id="date-range", display_format="YYYY/MM/DD"),

    dcc.Dropdown(id="dropdown-indicateurs", multi=True, placeholder="Sélectionnez les indicateurs"),

    html.Button("Lancer", id="btn-run", style={"backgroundColor": "black", "color": "white"}),

    dcc.Progress(id="progress-bar", value=0, max=100),

    html.Div(id="output-result")
])


# 🔹 Callback pour exécuter `main.py`
def run_main(n_clicks, id_datapack, name_datapack, start_date, end_date, indicateurs):
    if not all([id_datapack, name_datapack, start_date, end_date, indicateurs]):
        return 0, "⚠️ Veuillez remplir tous les champs."

    progress = 0

    def execute_main():
        nonlocal progress
        command = ["python", "main.py", str(id_datapack), name_datapack, start_date, end_date] + indicateurs
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        for _ in range(5):
            progress += 20
            time.sleep(1)

        process.wait()
        progress = 100

    thread = threading.Thread(target=execute_main)
    thread.start()

    return progress, "✅ Programme exécuté avec succès."


# 🔹 Callback pour exécuter le script
@dash.callback(
    Output("progress-bar", "value"),
    Output("output-result", "children"),
    Input("btn-run", "n_clicks"),
    State("input-id-datapack", "value"),
    State("dropdown-datapack", "value"),
    State("date-range", "start_date"),
    State("date-range", "end_date"),
    State("dropdown-indicateurs", "value"),
    prevent_initial_call=True
)
def execute(n_clicks, id_datapack, name_datapack, start_date, end_date, indicateurs):
    return run_main(n_clicks, id_datapack, name_datapack, start_date, end_date, indicateurs)
