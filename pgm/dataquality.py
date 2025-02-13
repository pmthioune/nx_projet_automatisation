import dash
from dash import dcc, html, Input, Output, dash_table
import pandas as pd
import os

# Initialiser l'application
app = dash.Dash(__name__)

# Répertoire contenant les fichiers de données
DATA_FOLDER = "./data"

# Fonction pour charger les fichiers disponibles dans le dossier
def get_data_files(folder):
    files = [f for f in os.listdir(folder) if f.endswith(".csv")]
    return files

# Layout principal
app.layout = html.Div([
    dcc.Tabs([
        dcc.Tab(label="Data Quality", children=[
            html.Div([
                html.H3("Analyse de la qualité des données", style={"marginBottom": "20px"}),

                # Liste déroulante pour choisir le fichier
                html.Div([
                    html.Label("Choisir un fichier à analyser :"),
                    dcc.Dropdown(
                        id="file-dropdown",
                        options=[{"label": f, "value": f} for f in get_data_files(DATA_FOLDER)],
                        placeholder="Sélectionnez un fichier",
                        style={"width": "50%"}
                    )
                ], style={"marginBottom": "20px"}),

                # Bloc des valeurs manquantes avec deux graphiques côte à côte
                html.Div([
                    html.H4("Valeurs manquantes pour les indicateurs PD et LGD"),
                    html.Div([
                        dcc.Graph(id="missing-values-pd-graph", style={"width": "48%", "display": "inline-block"}),
                        dcc.Graph(id="missing-values-lgd-graph", style={"width": "48%", "display": "inline-block"})
                    ]),
                ], style={"border": "1px solid #ddd", "padding": "20px", "marginBottom": "20px", "borderRadius": "8px"}),

                # Bloc des doublons
                html.Div([
                    html.H4("Doublons"),
                    html.P(id="duplicate-count", style={"fontSize": "16px"}),
                    dash_table.DataTable(
                        id="duplicates-table",
                        columns=[],
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
                    )
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
        ])
    ])
])

# Callback pour mettre à jour l'analyse selon le fichier sélectionné
@app.callback(
    [Output("missing-values-pd-graph", "figure"),
     Output("missing-values-lgd-graph", "figure"),
     Output("duplicate-count", "children"),
     Output("duplicates-table", "data"),
     Output("duplicates-table", "columns"),
     Output("outliers-table", "data")],
    [Input("file-dropdown", "value")]
)
def update_data_quality(file_name):
    if not file_name:
        # Aucune donnée sélectionnée
        return {}, {}, "Veuillez sélectionner un fichier.", [], [], []

    # Charger le fichier sélectionné
    file_path = os.path.join(DATA_FOLDER, file_name)
    df = pd.read_csv(file_path)

    # 1. Analyse des valeurs manquantes
    missing_values = df.isnull().sum() / len(df) * 100
    missing_values_pd_fig = {
        "data": [
            {"x": missing_values.index, "y": missing_values.values, "type": "bar", "name": "PD"}
        ],
        "layout": {"title": "Valeurs manquantes (%) - PD"}
    }
    missing_values_lgd_fig = {
        "data": [
            {"x": missing_values.index, "y": missing_values.values, "type": "bar", "name": "LGD"}
        ],
        "layout": {"title": "Valeurs manquantes (%) - LGD"}
    }

    # 2. Analyse des doublons
    duplicate_rows = df[df.duplicated()]
    duplicate_count = len(duplicate_rows)
    if duplicate_count > 0:
        duplicate_message = f"Nombre total de lignes en doublons : {duplicate_count}"
        duplicates_data = duplicate_rows.head(5).to_dict("records")
        duplicates_columns = [{"name": col, "id": col} for col in df.columns]
    else:
        duplicate_message = "Aucun doublon détecté dans les données."
        duplicates_data = []
        duplicates_columns = []

    # 3. Analyse des valeurs aberrantes (Exemple simple : valeurs supérieures à un seuil)
    outliers = []
    for col in df.select_dtypes(include=["float", "int"]):  # Numériques uniquement
        threshold = df[col].mean() + 3 * df[col].std()  # Détection simple basée sur la moyenne + 3*std
        outlier_values = df[df[col] > threshold][col]
        for val in outlier_values:
            outliers.append({"Colonne": col, "Valeur": val, "Description": "Valeur supérieure au seuil"})

    return missing_values_pd_fig, missing_values_lgd_fig, duplicate_message, duplicates_data, duplicates_columns, outliers

# Lancer l'application
if __name__ == "__main__":
    if not os.path.exists(DATA_FOLDER):
        os.makedirs(DATA_FOLDER)  # Créer le dossier si inexistant
    app.run_server(debug=True)
