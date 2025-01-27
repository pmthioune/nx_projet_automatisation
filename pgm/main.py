from dash import Dash, html, Input, Output, State, dcc
import dash_bootstrap_components as dbc
import threading
import time

# Variable globale pour stocker la progression
progress = 0

# Programme principal
def main(id_datapack, name_datapack, date_debut, date_fin):
    global progress
    progress = 0  # Réinitialiser la progression

    # Simule un traitement en plusieurs étapes
    for i in range(1, 101):
        time.sleep(0.05)  # Simule une tâche longue
        progress = i  # Met à jour la progression
        # Simule des étapes spécifiques basées sur les paramètres
        if i == 50:
            print(f"Traitement intermédiaire pour {name_datapack}, ID: {id_datapack}")
        if i == 100:
            print(f"Traitement terminé : {name_datapack}, Période : {date_debut} à {date_fin}")

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
        # En-tête
        html.Div(
            [
                html.H1(
                    "Titrisation - Barre de Progression",
                    style={
                        "textAlign": "center",
                        "fontFamily": "Montserrat",
                        "color": "white",
                    },
                ),
                html.Img(
                    src="https://upload.wikimedia.org/wikipedia/commons/6/60/Logo_Soci%C3%A9t%C3%A9_G%C3%A9n%C3%A9rale.svg",
                    style={"height": "50px", "float": "right"},
                ),
            ],
            style={"backgroundColor": "rgb(233, 4, 30)", "padding": "10px"},
        ),
        # Formulaire pour saisir les paramètres
        dbc.Row(
            [
                dbc.Col(dbc.Input(id="id-datapack", type="number", placeholder="ID Datapack"), width=3),
                dbc.Col(
                    dcc.Dropdown(
                        id="name-datapack",
                        options=[{"label": "RACER", "value": "RACER"}, {"label": "JUNON", "value": "JUNON"}],
                        placeholder="Nom du Datapack",
                    ),
                    width=3,
                ),
                dbc.Col(dcc.Input(id="date-debut", type="text", placeholder="Date Début (YYYY/MM/DD)"), width=3),
                dbc.Col(dcc.Input(id="date-fin", type="text", placeholder="Date Fin (YYYY/MM/DD)"), width=3),
            ],
            className="mb-3",
        ),
        # Bouton de lancement
        dbc.Button("Lancer le Traitement", id="start-button", color="primary", className="mb-4"),
        # Intervalle pour surveiller la progression
        dcc.Interval(id="progress-interval", interval=500, n_intervals=0, disabled=True),
        # Barre de progression
        dbc.Progress(id="progress-bar", striped=True, animated=True, value=0),
        # Texte de progression
        html.Div(id="progress-text", className="mt-2", style={"textAlign": "center"}),
    ],
    style={"padding": "20px", "fontFamily": "Source Sans Pro"},
)

# Lancer le programme principal dans un thread séparé
def run_main(id_datapack, name_datapack, date_debut, date_fin):
    main(id_datapack, name_datapack, date_debut, date_fin)

# Callback pour démarrer le traitement
@app.callback(
    Output("progress-interval", "disabled"),
    Input("start-button", "n_clicks"),
    [State("id-datapack", "value"), State("name-datapack", "value"), State("date-debut", "value"), State("date-fin", "value")],
    prevent_initial_call=True,
)
def start_processing(n_clicks, id_datapack, name_datapack, date_debut, date_fin):
    if not (id_datapack and name_datapack and date_debut and date_fin):
        return True  # Ne pas activer l'intervalle si les paramètres sont incomplets

    # Démarrer le traitement dans un thread séparé
    threading.Thread(target=run_main, args=(id_datapack, name_datapack, date_debut, date_fin)).start()
    return False  # Active l'intervalle pour surveiller la progression

# Callback pour mettre à jour la barre de progression
@app.callback(
    [Output("progress-bar", "value"), Output("progress-text", "children")],
    Input("progress-interval", "n_intervals"),
)
def update_progress(n_intervals):
    global progress
    return progress, f"Progression : {progress}%"

if __name__ == "__main__":
    app.run_server(debug=True)
