from dash import Dash, html, Input, Output, dcc
import dash_bootstrap_components as dbc
import threading
import main  # Importer le programme principal

# Application Dash
app = Dash(
    __name__,
    external_stylesheets=[
        "https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css",
    ],
)

# Mise en page de l'application
app.layout = html.Div(
    [
        html.H1("Titrisation - Barre de Progression", style={"textAlign": "center"}),
        dbc.Button("Lancer le Traitement", id="start-button", color="primary", className="mb-4"),
        dcc.Interval(id="progress-interval", interval=500, n_intervals=0, disabled=True),  # Intervalle de mise à jour
        dbc.Progress(id="progress-bar", striped=True, animated=True, value=0),
        html.Div(id="progress-text", className="mt-2", style={"textAlign": "center"}),
    ],
    style={"padding": "20px"},
)

# Lancer le programme principal dans un thread séparé
def run_main():
    main.main()

# Callback pour démarrer le traitement
@app.callback(
    Output("progress-interval", "disabled"),
    Input("start-button", "n_clicks"),
    prevent_initial_call=True,
)
def start_processing(n_clicks):
    # Démarrer le traitement dans un thread
    threading.Thread(target=run_main).start()
    return False  # Active l'intervalle pour surveiller la progression

# Callback pour mettre à jour la barre de progression
@app.callback(
    [Output("progress-bar", "value"), Output("progress-text", "children")],
    Input("progress-interval", "n_intervals"),
)
def update_progress(n_intervals):
    # Lire la progression globale
    progress = main.progress
    return progress, f"Progression : {progress}%"


if __name__ == "__main__":
    app.run_server(debug=True)
