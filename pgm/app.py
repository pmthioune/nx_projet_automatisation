import os
import dash
from dash import dcc, html, Input, Output, ctx
import dash_bootstrap_components as dbc
from threading import Thread
from dash.dash import no_update
from flask import send_from_directory
import plotly.express as px
import plotly.figure_factory as ff
import pandas as pd


# Assuming main.py contains the required functions
from main import start_process, get_progress

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.config.suppress_callback_exceptions = True  # Suppress callback exceptions

# Directory to save the output file
OUTPUT_DIR = '../../output'
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

# Sidebar content
sidebar = html.Div(
    [
        html.H2("Menu", style={"text-align": "center", "margin-top": "20px", "color": "white"}),
        dbc.Nav(
            [
                dbc.NavLink("Accueil", href="/accueil", id="accueil-link", style={"color": "white"}),
                dbc.NavLink("Datapacks", href="/datapacks", id="datapacks-link", style={"color": "white"}),
                dbc.NavLink("Data Quality", href="/dataquality", id="dataquality-link", style={"color": "white"}),
                dbc.NavLink("Gap Analysis", href="/gapanalysis", id="gapanalysis-link", style={"color": "white"}),
                dbc.NavLink("Téléchargement", href="/telechargement", id="telechargement-link", style={"color": "white"}),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style={
        "position": "fixed",
        "top": "0",
        "left": "0",
        "bottom": "0",
        "width": "250px",
        "background-color": "black",
        "padding": "20px",
        "color": "white",
    },
)

# Explanation content for the "Accueil" section
# Contenu de la section "Accueil"
accueil_content = html.Div(
    children=[
        # Titre de la section
        html.H3(
            "Bienvenue sur l'outil de Titrisation",
            style={"color": "#FF5733", "margin-bottom": "20px"}  # Couleur modernisée
        ),

        # Paragraphe d'introduction
        html.P(
            """
            Cette application vous permet de gérer et de suivre la construction des datapacks de la titrisation.
            Voici un guide pour prendre en main l'outil :
            """,
            style={"font-size": "18px", "margin-top": "20px", "line-height": "1.6"}
        ),

        # Liste des étapes pour utiliser l'application
        html.Ul(
            children=[
                # Étape 1 : Configuration des datapacks
                html.Li(
                    """
                    1. Allez dans la section 'Datapacks' pour configurer et construire le datapack.
                    Une fois la configuration terminée, appuyez sur le bouton 'Lancer le traitement' pour générer
                    le datapack. Suivez la progression du traitement avec la barre de progression en bas de la page.
                    Une fois le traitement terminé, vous recevrez un message de confirmation.
                    """,
                    style={"font-size": "16px", "margin-bottom": "10px"}
                ),

                # Étape 2 : Qualité des données
                html.Li(
                    "2. Utilisez la section 'Data Quality' pour évaluer et produire le rapport de la qualité des données.",
                    style={"font-size": "16px", "margin-bottom": "10px"}
                ),

                # Étape 3 : Analyse des écarts
                html.Li(
                    "3. Consultez la section 'Gap Analysis' pour analyser les écarts.",
                    style={"font-size": "16px", "margin-bottom": "10px"}
                ),

                # Étape 4 : Téléchargement des fichiers
                html.Li(
                    "4. Téléchargez les datapacks de la titrisation ainsi que les autres fichiers si besoin.",
                    style={"font-size": "16px", "margin-bottom": "10px"}
                ),
            ],
            style={"list-style-type": "disc", "padding-left": "40px", "color": "#333"}
        ),

        # Paragraphe de conclusion
        html.P(
            "Configurez et téléchargez vos fichiers selon le format approprié.",
            style={"font-size": "18px", "margin-top": "20px", "font-weight": "bold"}
        ),
    ],
    style={"padding": "20px", "background-color": "#f9f9f9", "border-radius": "8px"}  # Style moderne
)

# Datapacks section with button, file download option, and preview
datapacks_content = html.Div(
    children=[
        # Titre de la section
        html.H3("Datapacks", style={"color": "#FF5733", "margin-bottom": "20px"}),  # Couleur modernisée

        # Bouton pour lancer le traitement
        html.Button(
            "Lancer le traitement",
            id="btn-start-datapack",
            style={
                "background-color": "#333",  # Couleur modernisée
                "color": "white",
                "padding": "10px 20px",
                "border": "none",
                "border-radius": "5px",
                "cursor": "pointer",
                "margin-top": "20px"
            }
        ),

        # Barre de progression
        dbc.Progress(
            id="progress-bar-datapack",
            value=0,
            max=100,
            striped=True,
            animated=True,
            style={"margin-top": "20px", "height": "20px"}
        ),

        # Section pour afficher les logs
        html.Div(
            id="log-output-datapack",
            style={
                "margin-top": "20px",
                "padding": "10px",
                "background-color": "#f0f0f0",  # Fond clair pour les logs
                "border-radius": "5px",
                "border": "1px solid #ddd",
                "max-height": "200px",
                "overflow-y": "auto",
                "font-family": "monospace",
                "font-size": "14px",
                "color": "#333"
            }
        ),

        # Section pour le téléchargement des fichiers
        html.Div(id="download-section", children=[], style={"margin-top": "20px"}),

        # Section pour l'aperçu du DataFrame
        html.Div(id="df-preview", style={"margin-top": "20px"}),

        # Intervalle pour les mises à jour dynamiques
        dcc.Interval(id="interval-datapack", interval=1000, n_intervals=0, disabled=True),

        # Sélection du format de téléchargement
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
                        value='csv',  # Valeur par défaut
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
        "background-color": "#f9f9f9",  # Fond modernisé
        "border-radius": "8px",  # Bordures arrondies
        "border": "1px solid #ddd"  # Bordure légère
    }
)



# Data Quality section with innovative and comprehensible graphs
data_quality_content = html.Div(
    [
        html.H3("Data Quality", style={"color": "#FF5733", "margin-bottom": "20px"}),
        dcc.Graph(id='missing-data-graph'),
        dcc.Graph(id='data-distribution-graph'),
        dcc.Graph(id='missing-data-heatmap'),
        dcc.Graph(id='correlation-matrix'),
        dcc.Graph(id='outliers-detection'),
        html.H4("Variables Summary", style={"color": "#FF5733", "margin-top": "20px"}),
        html.Div(id='variables-summary'),
    ],
    style={"padding": "20px", "background-color": "#f9f9f9", "border-radius": "8px", "border": "1px solid #ddd"},
)

# Téléchargement section content
telechargement_content = html.Div(
    [
        html.H3("Téléchargement", style={"color": "red"}),
        html.P("Vous pouvez télécharger les fichiers générés ici.", style={"font-size": "18px", "margin-top": "20px"}),

        # Dropdown to select file
        dcc.Dropdown(
            id='file-dropdown',
            options=[],
            placeholder="Sélectionnez un fichier",
            style={"margin-top": "20px"}
        ),

        # RadioItems to select file format
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

        # Button to download the selected file
        html.Button("Télécharger", id="btn-download",
                    style={"background-color": "black", "color": "white", "margin-top": "20px"}),

        # Display DataFrame preview
        html.Div(id="df-preview", style={"margin-top": "20px"}),

        # Links for downloading files
        html.Div(id="download-links", style={"margin-top": "20px"}),
    ],
    style={"padding": "20px"},
)

# Main content area
main_content = html.Div(
    [
        html.H1("Titrisation", style={"background-color": "red", "color": "white", "padding": "10px"}),

        # Tab content
        html.Div(id="tab-content", style={"padding": "20px"}),

        dcc.Interval(id="interval", interval=1000, n_intervals=0, disabled=True),
    ],
    style={"margin-left": "250px", "padding": "20px"},
)

app.layout = html.Div([sidebar, main_content, dcc.Location(id='url', refresh=False)])


# Callback to switch content based on the active URL
@app.callback(
    Output("tab-content", "children"),
    Input("url", "pathname"),
)
def display_content(pathname):
    if pathname == "/accueil":
        return accueil_content
    elif pathname == "/datapacks":
        return datapacks_content
    elif pathname == "/dataquality":
        return data_quality_content
    elif pathname == "/gapanalysis":
        return html.Div([html.H3("Gap Analysis section content")])
    elif pathname == "/telechargement":  # New section
        return telechargement_content
    return accueil_content  # Default to "Accueil" content if no URL matched


@app.callback(
    [Output("progress-bar-datapack", "value"),
     Output("log-output-datapack", "children"),
     Output("download-section", "children"),
     Output("df-preview", "children"),
     Output("interval-datapack", "disabled")],
    [Input("btn-start-datapack", "n_clicks"),
     Input("interval-datapack", "n_intervals"),
     Input("file-format", "value")]
)


def update_progress(n_clicks, n_intervals, file_format):
    trigger_id = ctx.triggered_id

    if trigger_id == "btn-start-datapack":
        # Lancer le traitement dans un thread séparé
        thread = Thread(target=start_process)
        thread.start()
        return 0, "🚀 Traitement en cours...", "", "", False

    elif trigger_id == "interval-datapack":
        # Mettre à jour la barre de progression
        progress_state = get_progress()
        progress = progress_state["progress"]
        message = progress_state["message"]

        if progress == 100:
            # After processing, allow file download
            output_file_path = os.path.join(OUTPUT_DIR, f'output_file.{file_format}')
            # Create a dummy file for download
            with open(output_file_path, 'w') as f:
                f.write("Dummy output content")

            # Read the first few rows of the output file to preview it
            try:
                if file_format == 'csv':
                    df = pd.read_csv(output_file_path)
                elif file_format == 'xlsx':
                    df = pd.read_excel(output_file_path)
                else:
                    df = None  # For other formats, no preview available

                # Display the first few rows of the DataFrame as a preview
                preview = html.Div([
                    html.H5(f"Aperçu du fichier généré : {output_file_path}", style={"color": "blue"}),
                    html.Div([
                        html.P(f"Lignes 1-5 :"),
                        html.Table(
                            # Create an HTML table for preview
                            children=[
                                html.Tr([html.Th(col) for col in df.columns])  # Headers
                            ] +
                            [html.Tr([html.Td(df.iloc[i][col]) for col in df.columns]) for i in range(min(5, len(df)))]  # Data rows
                        ),
                    ])
                ])
            except Exception as e:
                preview = html.P(f"Erreur lors de l'aperçu du fichier : {str(e)}", style={"color": "red"})

            return progress, message, html.A(f"Télécharger le fichier ({file_format.upper()})",
                                             href=f"/download/{output_file_path}",
                                             download=f"output_file.{file_format}"), preview, True

        return progress, message, "", "", False

    return no_update, no_update, no_update, no_update, no_update


if __name__ == "__main__":
    app.run_server(debug=True)
