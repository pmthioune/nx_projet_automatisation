from dash import html, dcc
import dash_bootstrap_components as dbc

layout = html.Div(
    [
        html.H3("Téléchargement", style={"color": "red"}),
        html.P("Vous pouvez télécharger les fichiers générés ici.", style={"font-size": "18px", "margin-top": "20px"}),
        dcc.Dropdown(
            id='file-dropdown',
            options=[],
            placeholder="Sélectionnez un fichier",
            style={"margin-top": "20px"}
        ),
        dbc.Label("Choisissez le format de téléchargement :", style={"color": "white", "margin-top": "20px"}),
        dbc.RadioItems(
            id='download-format',
            options=[
                {'label': 'CSV', 'value': 'csv'},
                {'label': 'PDF', 'value': 'pdf'},
                {'label': 'XLSX', 'value': 'xlsx'}
            ],
            value='csv',
            inline=True,
            labelStyle={'margin-right': '10px'}
        ),
        html.Button("Télécharger", id="btn-download",
                    style={"background-color": "black", "color": "white", "margin-top": "20px"}),
        html.Div(id="df-preview", style={"margin-top": "20px"}),
        html.Div(id="download-links", style={"margin-top": "20px"}),
    ],
    style={"padding": "20px"},
)