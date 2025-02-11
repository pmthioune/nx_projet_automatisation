import dash
from dash import dcc, html, Input, Output, State, ctx
from threading import Thread
import time
import pandas as pd
import dash_bootstrap_components as dbc

# Initialiser l'application
app = dash.Dash(__name__)

# Simuler un DataFrame pour les analyses de qualité des données
data = {
    "Colonne": ["A", "B", "C", "D"],
    "Valeurs manquantes (%)": [5, 0, 10, 2],
    "Doublons détectés": [0, 2, 0, 1],
    "Valeurs aberrantes détectées": [3, 0, 2, 5]
}
df = pd.DataFrame(data)

# Variable globale pour stocker l'état de progression
progress_state = {"progress": 0, "message": ""}

# Layout principal
app.layout = html.Div([
    dcc.Tabs([
        dcc.Tab(label="Datapack", children=[
            html.Div([
                html.Label("Nom du projet :"),
                dcc.Input(id="project-name", type="text", placeholder="Entrez le nom du projet"),
                html.Label("Date de début :"),
                dcc.Input(id="start-date", type="date", placeholder="Sélectionnez une date"),
                html.Button("Lancer le traitement", id="btn-start", n_clicks=0),
                html.Div(id="error-message", style={"color": "red", "marginTop": "10px"})
            ]),
            dbc.Progress(id="progress-bar", value=0, color="success", striped=True, animated=True, label="0%"),
            html.Div(id="log-output", style={"marginTop": "10px", "fontSize": "16px"})
        ]),
        dcc.Tab(label="Data Quality", children=[
            html.Div([
                html.H3("Analyse de la qualité des données", style={"marginBottom": "20px"}),

                # Bloc des valeurs manquantes
                html.Div([
                    html.H4("Valeurs manquantes"),
                    html.P("Pourcentage des valeurs manquantes détectées par colonne :"),
                    dcc.Graph(id="missing-values-graph")
                ], style={"border": "1px solid #ddd", "padding": "20px", "marginBottom": "20px", "borderRadius": "8px"}),

                # Bloc des doublons
                html.Div([
                    html.H4("Doublons"),
                    html.P("Nombre de doublons détectés dans les données par colonne :"),
                    dcc.Graph(id="duplicates-graph")
                ], style={"border": "1px solid #ddd", "padding": "20px", "marginBottom": "20px", "borderRadius": "8px"}),

                # Bloc des valeurs aberrantes
                html.Div([
                    html.H4("Valeurs aberrantes"),
                    html.P("Nombre de valeurs aberrantes détectées par colonne :"),
                    dcc.Graph(id="outliers-graph")
                ], style={"border": "1px solid #ddd", "padding": "20px", "borderRadius": "8px"}),
            ])
        ]),
        dcc.Tab(label="Gap Analysis", children=[
            html.H3("Section Gap Analysis en développement...")
        ]),
    ]),
    dcc.Interval(id="interval", interval=1000, n_intervals=0, disabled=True)
])

# Callbacks pour l'onglet Data Quality
@app.callback(
    [Output("missing-values-graph", "figure"),
     Output("duplicates-graph", "figure"),
     Output("outliers-graph", "figure")],
    [Input("btn-start", "n_clicks")]
)
def update_data_quality(n_clicks):
    # Graphiques pour chaque analyse
    missing_values_fig = {
        "data": [
            {"x": df["Colonne"], "y": df["Valeurs manquantes (%)"], "type": "bar", "name": "Valeurs manquantes"}
        ],
        "layout": {"title": "Valeurs manquantes (%) par colonne"}
    }

    duplicates_fig = {
        "data": [
            {"x": df["Colonne"], "y": df["Doublons détectés"], "type": "bar", "name": "Doublons"}
        ],
        "layout": {"title": "Doublons détectés par colonne"}
    }

    outliers_fig = {
        "data": [
            {"x": df["Colonne"], "y": df["Valeurs aberrantes détectées"], "type": "bar", "name": "Valeurs aberrantes"}
        ],
        "layout": {"title": "Valeurs aberrantes détectées par colonne"}
    }

    return missing_values_fig, duplicates_fig, outliers_fig


# Callback principal pour la barre de progression
@app.callback(
    [Output("progress-bar", "value"),
     Output("progress-bar", "label"),
     Output("log-output", "children"),
     Output("interval", "disabled"),
     Output("error-message", "children")],
    [Input("btn-start", "n_clicks"),
     Input("interval", "n_intervals")],
    [State("project-name", "value"),
     State("start-date", "value")]
)
def update_progress(n_clicks, n_intervals, project_name, start_date):
    global progress_state
    trigger_id = ctx.triggered_id

    # Validation des champs requis
    if trigger_id == "btn-start":
        if not project_name or not start_date:
            return dash.no_update, dash.no_update, dash.no_update, dash.no_update, "⚠️ Veuillez remplir tous les champs obligatoires."

        # Lancer le traitement dans un thread séparé
        thread = Thread(target=start_process)
        thread.start()
        return 0, "0%", "🚀 Traitement en cours...", False, ""

    elif trigger_id == "interval":
        # Récupérer l'état de progression
        progress = progress_state["progress"]
        message = progress_state["message"]
        label = f"{progress}%"

        if progress == 100:
            return progress, label, message, True, ""
        return progress, label, message, False, ""

    return dash.no_update, dash.no_update, dash.no_update, dash.no_update, ""

# Simuler le traitement principal
def start_process():
    global progress_state
    states = [
        {"progress": 25, "message": "1/4 - Collecte des données terminée."},
        {"progress": 50, "message": "2/4 - Contrôle qualité des données terminé."},
        {"progress": 75, "message": "3/4 - Calcul des indicateurs terminé."},
        {"progress": 100, "message": "4/4 - Génération du datapack terminée."}
    ]

    for state in states:
        progress_state.update(state)
        time.sleep(2)  # Simuler le délai pour chaque étape

# Lancer l'application
if __name__ == '__main__':
    app.run_server(debug=True)
