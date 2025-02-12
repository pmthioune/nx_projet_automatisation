from dash import html, dcc
import dash_bootstrap_components as dbc

layout = html.Div(
    children=[
        html.H3("Datapacks", style={"color": "#FF5733", "margin-bottom": "20px"}),

        # Cadre de configuration
        html.Div(
            children=[
                html.H4("Configuration", style={"color": "#333", "margin-bottom": "20px"}),

                # Champ Date
                dbc.Row(
                    [
                        dbc.Col(dbc.Label("Date", style={"font-weight": "bold"}), width=2),
                        dbc.Col(dcc.DatePickerSingle(id='config-date', date='2025-02-12'), width=10),
                    ],
                    style={"margin-bottom": "10px"}
                ),

                # Champ Nom
                dbc.Row(
                    [
                        dbc.Col(dbc.Label("Nom", style={"font-weight": "bold"}), width=2),
                        dbc.Col(dbc.Input(id='config-nom', type='text', placeholder='Entrez le nom'), width=10),
                    ],
                    style={"margin-bottom": "10px"}
                ),

                # Champ Family Name
                dbc.Row(
                    [
                        dbc.Col(dbc.Label("Family Name", style={"font-weight": "bold"}), width=2),
                        dbc.Col(dbc.Input(id='config-family-name', type='text', placeholder='Entrez le nom de famille'), width=10),
                    ],
                    style={"margin-bottom": "10px"}
                ),

                # Champ ID
                dbc.Row(
                    [
                        dbc.Col(dbc.Label("ID", style={"font-weight": "bold"}), width=2),
                        dbc.Col(dbc.Input(id='config-id', type='text', placeholder='Entrez l\'ID'), width=10),
                    ],
                    style={"margin-bottom": "10px"}
                ),

                # Bouton de soumission
                dbc.Button("Soumettre", id="btn-submit-config", color="primary", style={"margin-top": "20px"}),
            ],
            style={
                "padding": "20px",
                "background-color": "#f9f9f9",
                "border-radius": "8px",
                "border": "1px solid #ddd",
                "margin-bottom": "20px"
            }
        ),

        html.Button(
            "Lancer le traitement",
            id="btn-start-datapack",
            style={
                "background-color": "#333",
                "color": "white",
                "padding": "10px 20px",
                "border": "none",
                "border-radius": "5px",
                "cursor": "pointer",
                "margin-top": "20px"
            }
        ),
        dbc.Progress(
            id="progress-bar-datapack",
            value=0,
            max=100,
            striped=True,
            animated=True,
            style={"margin-top": "20px", "height": "20px"}
        ),
        html.Div(
            id="log-output-datapack",
            style={
                "margin-top": "20px",
                "padding": "10px",
                "background-color": "#f0f0f0",
                "border-radius": "5px",
                "border": "1px solid #ddd",
                "max-height": "200px",
                "overflow-y": "auto",
                "font-family": "monospace",
                "font-size": "14px",
                "color": "#333"
            }
        ),
        html.Div(id="download-section", children=[], style={"margin-top": "20px"}),
        html.Div(id="df-preview", style={"margin-top": "20px"}),
        dcc.Interval(id="interval-datapack", interval=1000, n_intervals=0, disabled=True),
        dbc.Row(
            [
                dbc.Col(
                    dbc.Label("Choisissez le format de téléchargement :", style={"color": "#333", "font-weight": "bold"}),
                    width=4
                ),
                dbc.Col(
                    dbc.RadioItems(
                        id='file-format',
                        options=[
                            {'label': 'CSV', 'value': 'csv'},
                            {'label': 'PDF', 'value': 'pdf'},
                            {'label': 'XLSX', 'value': 'xlsx'}
                        ],
                        value='csv',
                        inline=True,
                        labelStyle={'margin-right': '10px', 'font-weight': 'normal'}
                    ),
                    width=8
                ),
            ],
            style={"margin-top": "20px"}
        ),
    ],
    style={
        "padding": "20px",
        "background-color": "#f9f9f9",
        "border-radius": "8px",
        "border": "1px solid #ddd"
    }
)