from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc

# Constantes pour les styles
CARD_STYLE = {
    "background-color": "#f8f9fa",
    "border": "1px solid #dee2e6"
}

KPI_CARD_STYLE = {
    "height": "100%"
}

KPI_CARD_BODY_STYLE = {
    "background-color": "#f8d7da",
    "color": "#721c24",
    "border": "1px solid #f5c6cb"
}


# Fonction pour créer une carte KPI avec des icônes à côté du titre
def create_kpi_card(title, icon_class, icon_color, text_id, card_style, body_style):
    return dbc.Card(
        dbc.CardBody(
            [
                # Titre avec l'icône à côté
                html.Div(
                    [
                        html.I(className=f"fas {icon_class} fa-lg", style={
                            "color": icon_color,
                            "margin-right": "10px",
                            "font-size": '24px',
                            'opacity': 0.8
                        }),
                        html.H5(title, className="card-title", style={'font-size': '18px', 'font-weight': '600'})
                    ],
                    style={"display": "flex", "align-items": "center"}
                    # Flexbox pour aligner l'icône et le titre horizontalement
                ),
                html.P(id=text_id, className="card-text", style={'font-size': '16px', 'font-weight': '500'})
            ]
        ),
        className="kpi-card",
        style={**KPI_CARD_STYLE, **card_style, **body_style}
    )


# Contenu de la section Qualité des données avec des icônes à côté du titre
data_quality_content = html.Div(
    [
        # Ligne de cartes KPI avec des icônes à côté du titre
        dbc.Row(
            [
                dbc.Col(
                    create_kpi_card("Values", "fa-exclamation-circle", "#721c24",
                                    'total-missing-values',{"background-color": "#f8d7da"},
                                    {"color": "#721c24", "border": "1px solid #f5c6cb"}), width=3),
                dbc.Col(create_kpi_card("Duplicates", "fa-clone", "#0c5460",
                                        'total-duplicates',{"background-color": "#d1ecf1"},
                                        {"color": "#0c5460", "border": "1px solid #bee5eb"}), width=3),
                dbc.Col(create_kpi_card("Outliers", "fa-chart-line", "#856404",
                                        'total-outliers',{"background-color": "#fff3cd"},
                                        {"color": "#856404", "border": "1px solid #ffeeba"}), width=3),
                dbc.Col(
                    create_kpi_card("Timeliness", "fa-clock", "#155724", 'timeliness',
                                    {"background-color": "#d4edda"},
                                    {"color": "#155724", "border": "1px solid #c3e6cb"}), width=3),
            ],
            className="kpi-row"
        ),

        # Graphiques
        dbc.Card(
            dbc.CardBody(
                [
                    html.H5("Missing Data", className="card-title", style={'font-size': '18px', 'font-weight': '600'}),
                    dcc.Graph(id='missing-data-graph')
                ]
            ),
            className="mt-4",
            style=CARD_STYLE
        ),
        dbc.Card(
            dbc.CardBody(
                [
                    html.H5("Outliers Detection", className="card-title",
                            style={'font-size': '18px', 'font-weight': '600'}),
                    dcc.Graph(id='outliers-detection'),
                    dcc.Graph(id='z-score-detection')
                ]
            ),
            className="mt-4",
            style=CARD_STYLE
        ),

        # Analyse des valeurs dupliquées
        dbc.Card(
            dbc.CardBody(
                [
                    html.H5("Duplicate Values Analysis", className="card-title",
                            style={'font-size': '18px', 'font-weight': '600'}),
                    html.Div(id='duplicates-graph', className="card-text"),
                    html.H6("Duplicates by Key", className="card-title mt-3", style={'font-size': '16px'}),
                    dcc.Dropdown(
                        id='duplicate-key-selector',
                        options=[],
                        multi=False,
                        placeholder="Select key for duplicates",
                        className="mb-3"
                    ),
                    dcc.Graph(id='duplicates-by-key-graph')
                ]
            ),
            className="mt-3",
            style={"background-color": "#e9ecef", "border": "1px solid #dee2e6"}
        ),

        html.H4("Detailed DQ Report",
                style={"color": "#FF5733", "margin-top": "20px", 'font-size': '20px', 'font-weight': '700'}),

        # Tableau de qualité des données
        dbc.Card(
            dbc.CardBody(
                [
                    html.H5("Data Quality Table", className="card-title",
                            style={'font-size': '18px', 'font-weight': '600'}),
                    dash_table.DataTable(
                        id='data-quality-table',
                        columns=[],
                        data=[],
                        style_table={'overflowX': 'auto'},
                        style_header={
                            'backgroundColor': '#343a40',
                            'color': 'white',
                            'fontWeight': 'bold',
                            'textAlign': 'center'
                        },
                        style_cell={
                            'backgroundColor': '#495057',
                            'color': 'white',
                            'textAlign': 'left',
                            'padding': '10px',
                            'border': '1px solid #dee2e6'
                        },
                        style_data_conditional=[
                            {'if': {'row_index': 'odd'}, 'backgroundColor': '#3e444a'}
                        ]
                    )
                ]
            ),
            className="mt-4",
            style=CARD_STYLE
        ),

        # Vue d'ensemble du jeu de données
        dbc.Card(
            dbc.CardBody(
                [
                    html.H5("Dataset Overview", className="card-title",
                            style={'font-size': '18px', 'font-weight': '600'}),
                    html.Div(id='data-description', className="card-text", style={'font-size': '16px'}),
                    html.H5("Variables description", className="card-title",
                            style={'font-size': '18px', 'font-weight': '600'}),
                    dcc.Dropdown(id='variable-selector', options=[], multi=True, placeholder="Select variables")
                ]
            ),
            className="mt-4",
            style=CARD_STYLE
        ),

        # Bouton pour télécharger le rapport
        dbc.Button(
            "Télécharger le rapport",
            id="download-report",
            color="primary",
            size="lg",
            style={"margin-top": "20px", "padding": "10px 20px", "width": "auto", 'font-size': '16px'},
            className="shadow-sm"
        ),
        dcc.Download(id="download-report")
    ],
    style={"padding": "20px", "background-color": "#f9f9f9", "border-radius": "8px", "border": "1px solid #ddd"}
)
