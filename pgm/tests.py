import dash
from dash import dcc, html, Input, Output, dash_table
import pandas as pd

# Initialiser l'application
app = dash.Dash(__name__)

# Simuler les données pour l'analyse de la qualité des données
data = {
    "Colonne1": [1, 2, 2, 4, 5, 6, 6],
    "Colonne2": ["A", "B", "B", "D", "E", "F", "F"],
    "Colonne3": [10, 20, 20, 40, 50, 60, 60]
}
df = pd.DataFrame(data)

# Layout principal
app.layout = html.Div([
    dcc.Tabs([
        dcc.Tab(label="Data Quality", children=[
            html.Div([
                html.H3("Analyse de la qualité des données", style={"marginBottom": "20px"}),

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
                        columns=[
                            {"name": col, "id": col} for col in df.columns
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

# Callback pour la gestion des doublons
@app.callback(
    [Output("duplicate-count", "children"),
     Output("duplicates-table", "data"),
     Output("missing-values-pd-graph", "figure"),
     Output("missing-values-lgd-graph", "figure")],
    [Input("duplicate-count", "id")]  # Trigger initial au chargement
)
def update_data_quality(trigger):
    # Identifier les doublons
    duplicate_rows = df[df.duplicated()]
    duplicate_count = len(duplicate_rows)

    # Message pour les doublons
    if duplicate_count > 0:
        duplicate_message = f"Nombre total de lignes en doublons : {duplicate_count}"
        duplicates_data = duplicate_rows.head(5).to_dict("records")
    else:
        duplicate_message = "Aucun doublon détecté dans les données."
        duplicates_data = []

    # Graphique des valeurs manquantes pour PD
    missing_values_pd_fig = {
        "data": [
            {"x": ["Colonne1", "Colonne2", "Colonne3"], "y": [0, 0, 0], "type": "bar", "name": "PD"}
        ],
        "layout": {"title": "Valeurs manquantes (%) - PD"}
    }

    # Graphique des valeurs manquantes pour LGD
    missing_values_lgd_fig = {
        "data": [
            {"x": ["Colonne1", "Colonne2", "Colonne3"], "y": [0, 0, 0], "type": "bar", "name": "LGD"}
        ],
        "layout": {"title": "Valeurs manquantes (%) - LGD"}
    }

    return duplicate_message, duplicates_data, missing_values_pd_fig, missing_values_lgd_fig


# Lancer l'application
if __name__ == "__main__":
    app.run_server(debug=True)
