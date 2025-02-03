import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import time
import threading

# 🔹 Création de l'application Dash
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Stockage de la progression (Initialisé à 0)
progress_store = {"progress": 0}


# 🔹 Fonction qui simule l'exécution de main.py en arrière-plan
def execute_main(id_datapack, name_datapack, start_date, end_date):
    global progress_store
    progress_store["progress"] = 0  # Réinitialiser la barre

    steps = [
        ("Collecte des données", 25),
        ("Vérification qualité des données", 50),
        ("Calcul des indicateurs", 75),
        ("Génération du Datapack", 100)
    ]

    for message, progress in steps:
        print(f"[{progress}%] {message} en cours...")
        time.sleep(2)  # Simule le temps d'exécution
        progress_store["progress"] = progress

    print("[100%] ✅ Traitement terminé.")


# 🔹 Interface utilisateur
app.layout = html.Div([
    html.H1("Titrisation", style={"background-color": "red", "color": "white", "padding": "10px"}),

    dcc.Input(id="input-id", type="number", placeholder="ID Datapack"),
    dcc.Dropdown(id="name-datapack",
                 options=[{"label": "RACER", "value": "RACER"}, {"label": "JUNON", "value": "JUNON"}],
                 placeholder="Choisir un datapack"),
    dcc.DatePickerRange(id="date-range", display_format="YYYY/MM/DD"),

    html.Button("Créer Datapack", id="btn-create", style={"background-color": "black", "color": "white"}),

    # Barre de progression
    dcc.Interval(id="interval", interval=1000, n_intervals=0, disabled=True),  # Rafraîchit la barre
    dbc.Progress(id="progress-bar", value=0, max=100, striped=True, animated=True, style={"margin-top": "20px"}),

    html.Div(id="log-output", style={"margin-top": "20px", "font-family": "Arial", "font-size": "16px"}),
])


# 🔹 Callback pour démarrer l'exécution en arrière-plan
@app.callback(
    Output("interval", "disabled"),
    Input("btn-create", "n_clicks"),
    State("input-id", "value"),
    State("name-datapack", "value"),
    State("date-range", "start_date"),
    State("date-range", "end_date"),
    prevent_initial_call=True
)
def start_main(n_clicks, id_datapack, name_datapack, start_date, end_date):
    if not all([id_datapack, name_datapack, start_date, end_date]):
        return True  # Ne pas activer le rafraîchissement si des champs sont vides

    # Démarrer `main.py` dans un thread séparé
    thread = threading.Thread(target=execute_main, args=(id_datapack, name_datapack, start_date, end_date))
    thread.start()

    return False  # Active `dcc.Interval` pour mettre à jour la barre


# 🔹 Callback pour mettre à jour la barre de progression
@app.callback(
    [Output("progress-bar", "value"), Output("log-output", "children")],
    Input("interval", "n_intervals")
)
def update_progress(n_intervals):
    global progress_store
    progress = progress_store["progress"]

    messages = {
        25: "➡ Collecte des données en cours...",
        50: "➡ Vérification de la qualité des données...",
        75: "➡ Calcul des indicateurs en cours...",
        100: "✅ Génération du Datapack terminée."
    }

    log_message = messages.get(progress, "🚀 Démarrage...")

    if progress == 100:
        return progress, html.P(log_message, style={"color": "green"})

    return progress, html.P(log_message, style={"color": "blue"})


# 🔹 Lancer l'application
if __name__ == "__main__":
    app.run_server(debug=True)
