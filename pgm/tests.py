from dash import Dash, html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
import time
import os

# Initialisation de l'application
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Mise en page de l'application
app.layout = html.Div([
    # Titre avec fond rouge
    html.Div(
        html.H1("Titrisation", style={"color": "white", "textAlign": "center", "padding": "10px"}),
        style={"backgroundColor": "rgb(233, 4, 30)"}
    ),
    # Onglets principaux
    dcc.Tabs(
        id="tabs",
        value="tab-datapack",
        children=[
            # Onglet Datapack
            dcc.Tab(
                label="Datapack",
                value="tab-datapack",
                children=[
                    html.Div(
                        [
                            html.H4("Calcul des Indicateurs"),
                            # Dropdown pour les indicateurs
                            dcc.Dropdown(
                                id="dropdown-indicateurs",
                                options=[
                                    {"label": f"Indicateur {i}", "value": i} for i in range(1, 21)
                                ],
                                placeholder="Sélectionnez les indicateurs",
                                multi=True,  # Autorise la sélection multiple
                                style={"width": "50%"}
                            ),
                            html.Br(),
                            # Progress bar et bouton
                            html.Div(
                                [
                                    dbc.Progress(id="progress-bar", striped=True, animated=True, style={"height": "30px"}),
                                    html.Br(),
                                    dbc.Button("Lancer le programme", id="run-program-btn", color="primary"),
                                ],
                                style={"padding": "10px"}
                            ),
                        ],
                        style={"padding": "20px"}
                    )
                ]
            ),
            # Autres onglets placeholder
            dcc.Tab(label="Data Quality", value="tab-dataquality"),
            dcc.Tab(label="Gap Analyse", value="tab-gapanalyse"),
        ]
    )
])

# Callbacks pour gérer la progression
@app.callback(
    [Output("progress-bar", "value"),
     Output("progress-bar", "label")],
    [Input("run-program-btn", "n_clicks")],
    [State("dropdown-indicateurs", "value")]
)
def run_program(n_clicks, selected_indicators):
    if not n_clicks:
        return 0, ""

    if not selected_indicators:
        return 0, "Veuillez sélectionner des indicateurs."

    # Écrire la configuration des indicateurs dans ind_config.py
    with open("ind_config.py", "w") as f:
        f.write(f"SELECTED_INDICATORS = {selected_indicators}\n")

    # Simuler l'exécution de main.py avec une barre de progression
    total_steps = 100
    for i in range(total_steps + 1):
        time.sleep(0.05)  # Simuler le temps d'exécution
        yield i, f"{i}%"

    # Simuler l'appel de main.py
    os.system("python main.py")

    return 100, "Programme terminé avec succès."

# Démarrage de l'application
if __name__ == "__main__":
    app.run_server(debug=True)
