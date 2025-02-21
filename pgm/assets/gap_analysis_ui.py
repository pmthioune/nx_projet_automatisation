from dash import html, dcc
import dash_bootstrap_components as dbc
from dash_iconify import DashIconify

# Styles récurrents
card_style = {
    "padding": "20px",
    "background-color": "#ffffff",
    "border-radius": "12px",
    "border": "1px solid #ddd",
    "box-shadow": "2px 2px 10px rgba(0,0,0,0.1)",
}

header_style = {
    "color": "#FF5733",
    "text-align": "left",
    "margin-bottom": "20px",
    "font-weight": "bold",
    "font-size": "30px"
}

dropdown_style = {
    "margin-bottom": "10px",
    "border-radius": "5px",
    "box-shadow": "2px 2px 10px rgba(0,0,0,0.1)",
}

button_style = {
    "width": "100%",
    "font-weight": "bold",
    "border-radius": "5px",
    "box-shadow": "2px 2px 10px rgba(0,0,0,0.1)",
}

gap_analysis_content = dbc.Container(
    [
        dbc.Card(
            dbc.CardBody(
                [
                    html.H3("🔍 Gap Analysis", style=header_style),
                    html.Br(),
                    dbc.Row(
                        [
                            dbc.Col(
                                [
                                    html.Label("📂 Sélectionner le premier DataFrame :", className="fw-bold"),
                                    dcc.Dropdown(
                                        id="df-selector-1",
                                        options=[],  # Options mises à jour dynamiquement
                                        placeholder="Choisissez un premier fichier...",
                                        style=dropdown_style,
                                    ),
                                ],
                                md=6,
                            ),
                            dbc.Col(
                                [
                                    html.Label("📂 Sélectionner le deuxième DataFrame :", className="fw-bold"),
                                    dcc.Dropdown(
                                        id="df-selector-2",  # Correction de l'ID
                                        options=[],  # Options mises à jour dynamiquement
                                        placeholder="Choisissez un deuxième fichier...",
                                        style=dropdown_style,
                                    ),
                                ],
                                md=6,
                            ),
                        ]
                    ),
                    html.Br(),
                    dbc.Row(
                        [
                            dbc.Col(
                                dbc.Button(
                                    "🚀 Lancer l'Analyse",
                                    id="run-gap-analysis",
                                    color="primary",
                                    size="lg",
                                    style=button_style,
                                    n_clicks=0,
                                ),
                                width={"size": 6, "offset": 3},
                            )
                        ]
                    ),
                    html.Br(),
                    # Section des résultats
                    html.Hr(),
                    html.H4("📊 Résultats de l'Analyse", style={"font-weight": "bold", "text-align": "center"}),
                    dbc.Row(
                        [
                            dbc.Col(
                                dbc.Card(
                                    dbc.CardBody(
                                        [
                                            html.H5("Comparaison des Valeurs Manquantes", style={"font-weight": "bold"}),
                                            dcc.Graph(id="missing-data-graph"),
                                        ]
                                    ),
                                    style=card_style,
                                ),
                                md=6,
                            ),
                            dbc.Col(
                                dbc.Card(
                                    dbc.CardBody(
                                        [
                                            html.H5("Comparaison des Outliers", style={"font-weight": "bold"}),
                                            dcc.Graph(id="outliers-detection"),
                                        ]
                                    ),
                                    style=card_style,
                                ),
                                md=6,
                            ),
                        ]
                    ),
                    html.Br(),
                    dbc.Row(
                        [
                            dbc.Col(
                                dbc.Card(
                                    dbc.CardBody(
                                        [
                                            html.H5("Comparaison des Doublons", style={"font-weight": "bold"}),
                                            dcc.Graph(id="duplicates-by-key-graph"),
                                        ]
                                    ),
                                    style=card_style,
                                ),
                                md=6,
                            ),
                            dbc.Col(
                                dbc.Card(
                                    dbc.CardBody(
                                        [
                                            html.H5("Distribution des Colonnes", style={"font-weight": "bold"}),
                                            dcc.Graph(id="distribution-graph"),
                                        ]
                                    ),
                                    style=card_style,
                                ),
                                md=6,
                            ),
                        ]
                    ),
                    html.Br(),
                    html.Hr(),
                    html.Div(id="gap-analysis-summary", style={"text-align": "center", "font-weight": "bold", "font-size": "18px"}),
                    html.Div(id="error-message", style={"color": "red", "text-align": "center", "font-weight": "bold"}),  # Ajout d'un message d'erreur
                ]
            ),
            style=card_style,
        ),
    ],
    fluid=True,
)
