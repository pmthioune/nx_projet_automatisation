from dash import Dash, html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# Initialisation de l'application
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Exemple de données pour les graphiques
df = pd.DataFrame({
    "Variable": ["A", "B", "C", "D"],
    "Missing": [5, 2, 8, 1],
    "Outliers": [3, 0, 2, 5],
    "Duplicates": [1, 3, 0, 2],
})

# Mise en page de l'application
app.layout = html.Div([
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
                            dbc.Checklist(
                                options=[{"label": f"Indicateur {i}", "value": i} for i in range(1, 21)],
                                id="checklist-indicateurs",
                                inline=True,
                            ),
                            html.Hr(),
                            html.H4("Informations"),
                            dbc.Row([
                                dbc.Col(dbc.Input(id="id-datapack", type="number", placeholder="ID Datapack"), width=3),
                                dbc.Col(dcc.Dropdown(
                                    id="name-datapack",
                                    options=[
                                        {"label": "RACER", "value": "RACER"},
                                        {"label": "JUNON", "value": "JUNON"},
                                    ],
                                    placeholder="Nom du Datapack",
                                ), width=3),
                                dbc.Col(dcc.Input(id="date-debut", type="text", placeholder="Date Début (YYYY/MM/DD)"), width=3),
                                dbc.Col(dcc.Input(id="date-fin", type="text", placeholder="Date Fin (YYYY/MM/DD)"), width=3),
                            ]),
                            html.Br(),
                            dbc.Button("Créer Datapack", id="create-datapack-btn", color="primary", className="me-2"),
                            dbc.Button("Télécharger", id="download-btn", color="success"),
                        ],
                        style={"padding": "20px"}
                    )
                ]
            ),
            # Onglet Data Quality
            dcc.Tab(
                label="Data Quality",
                value="tab-dataquality",
                children=[
                    html.Div(
                        [
                            html.H4("Graphiques de Data Quality"),
                            dbc.Row([
                                dbc.Col(dcc.Graph(
                                    id="missing-values-graph",
                                    figure=go.Figure(data=[
                                        go.Bar(x=df["Variable"], y=df["Missing"], name="Valeurs Manquantes")
                                    ]).update_layout(title="Valeurs Manquantes")
                                )),
                                dbc.Col(dcc.Graph(
                                    id="outliers-graph",
                                    figure=go.Figure(data=[
                                        go.Bar(x=df["Variable"], y=df["Outliers"], name="Outliers")
                                    ]).update_layout(title="Outliers")
                                )),
                                dbc.Col(dcc.Graph(
                                    id="duplicates-graph",
                                    figure=go.Figure(data=[
                                        go.Bar(x=df["Variable"], y=df["Duplicates"], name="Doublons")
                                    ]).update_layout(title="Doublons")
                                )),
                            ]),
                            html.Br(),
                            dbc.Button("Générer Rapport Word", id="generate-report-btn", color="info"),
                        ],
                        style={"padding": "20px"}
                    )
                ]
            ),
            # Onglet Gap Analyse
            dcc.Tab(
                label="Gap Analyse",
                value="tab-gapanalyse",
                children=[
                    html.Div(
                        [
                            html.H4("Comparaison des Datapacks"),
                            dbc.Row([
                                dbc.Col(dcc.Dropdown(
                                    id="datapack1",
                                    options=[
                                        {"label": "RACER", "value": "RACER"},
                                        {"label": "JUNON", "value": "JUNON"},
                                    ],
                                    placeholder="Datapack 1",
                                ), width=4),
                                dbc.Col(dcc.Dropdown(
                                    id="datapack2",
                                    options=[
                                        {"label": "RACER", "value": "RACER"},
                                        {"label": "JUNON", "value": "JUNON"},
                                    ],
                                    placeholder="Datapack 2",
                                ), width=4),
                            ]),
                            html.Br(),
                            html.H4("Indicateurs à Comparer"),
                            dbc.Checklist(
                                options=[{"label": f"Indicateur {i}", "value": i} for i in range(1, 21)],
                                id="checklist-comparison",
                                inline=True,
                            ),
                            html.Br(),
                            html.H4("Graphiques de Comparaison"),
                            dcc.Graph(
                                id="comparison-graph",
                                figure=go.Figure().update_layout(title="Comparaison des Indicateurs")
                            )
                        ],
                        style={"padding": "20px"}
                    )
                ]
            ),
        ]
    )
])

# Callbacks pour mettre à jour les graphiques de comparaison
@app.callback(
    Output("comparison-graph", "figure"),
    Input("checklist-comparison", "value"),
)
def update_comparison(selected_indicators):
    if not selected_indicators:
        return go.Figure().update_layout(title="Aucun indicateur sélectionné")
    else:
        # Exemple de comparaison fictive
        data = [
            go.Bar(name=f"Datapack 1 - Ind {i}", x=["Var A", "Var B"], y=np.random.randint(1, 10, 2))
            for i in selected_indicators
        ]
        data += [
            go.Bar(name=f"Datapack 2 - Ind {i}", x=["Var A", "Var B"], y=np.random.randint(1, 10, 2))
            for i in selected_indicators
        ]
        return go.Figure(data=data).update_layout(title="Comparaison des Indicateurs", barmode="group")

# Démarrage de l'application
if __name__ == "__main__":
    app.run_server(debug=True)
