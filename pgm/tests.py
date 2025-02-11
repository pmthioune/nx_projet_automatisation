import dash
from dash import dcc, html, Input, Output, State, ctx, dash_table
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

# Détail des valeurs aberrantes (exemple fictif)
outlier_details = [
    {"Colonne": "A", "Valeur": 999, "Description": "Valeur hors plage attendue."},
    {"Colonne": "A", "Valeur": -50, "Description": "Valeur négative non permise."},
    {"Colonne": "C", "Valeur": 200, "Description": "Écart par rapport à la médiane de plus de 3 écarts-types."},
    {"Colonne": "D", "Valeur": 1000, "Description": "Valeur extrême détectée."},
    {"Colonne": "D", "Valeur": 1050, "Description": "Valeur hors seuil maximal défini."}
]

df = pd.DataFrame(data)
outlier_df = pd.DataFrame(outlier_details)

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
                    html.P("Détails des valeurs aberrantes détectées :"),
                    dash_table.DataTable(
                        id="outliers-table",
                        columns=[
                            {"name": "Colonne", "id": "Colonne"},
                            {"name": "Valeur", "id": "Valeur"},
                            {"name": "Description", "id": "Description"}
                        ],
                        style_table={"overflowX": "auto"},
                        style_cell={
                            "textAlign": "left",
                            "padding": "10px",
                            "fontSize": "14px",
                        },
                        style_header={
                            "backgroundColor": "#f4f4f4",
                            "fontWeight": "bold",
                        },
                        style_data_conditional=[
                            {
                                "if": {"column_id": "Valeur"},
                                "backgroundColor": "#ffe6e6",
                                "color": "black",
                            }
                        ],
                    )
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
     Output("outliers-table", "data")],
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

    return missing_values_fig, duplicates_fig, outlier_df.to_dict("records")


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
