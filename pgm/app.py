import os
import dash
from dash import dcc, html, Input, Output, ctx, State
import dash_bootstrap_components as dbc
import pandas as pd
import threading
import time
from flask import send_from_directory
from assets.accueil_ui import get_accueil_content
from assets.datapacks_ui import datapacks_content
from assets.data_quality_ui import data_quality_content
from assets.gap_analysis_ui import gap_analysis_content
from assets.download_ui import download_content
from assets.data_import import load_data
from assets.data_quality import data_quality_report
from main import start_process, get_progress
from dash.dash import no_update
import plotly.express as px

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.config.suppress_callback_exceptions = True

# Répertoire pour enregistrer le fichier de sortie
OUTPUT_DIR = '../../output'
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

# Répertoire pour charger le fichier d'entrée
INPUT_DIR = r"C:\Users\FayçalOUSSEINIMALI\Desktop\DASH\Dash\nx_projet_automatisation\input"
input_file = os.path.join(INPUT_DIR, 'demographic_data.csv')

# État de la langue
LANGUAGES = {
    "fr": "Français",
    "en": "English"
}

# Contenu de la barre latérale avec des icônes
sidebar = html.Div(
    [
        html.H2("Menu", style={"text-align": "center", "margin-top": "20px", "color": "white"}),
        dbc.Nav(
            [
                dbc.NavLink([html.I(className="fas fa-home", style={"margin-right": "10px"}),
                             "Accueil"], href="/accueil", id="accueil-link", style={"color": "white"}),
                dbc.NavLink([html.I(className="fas fa-database", style={"margin-right": "10px"}),
                             "Datapacks"], href="/datapacks", id="datapacks-link", style={"color": "white"}),
                dbc.NavLink([html.I(className="fas fa-chart-line", style={"margin-right": "10px"}),
                             "Data Quality"], href="/dataquality", id="dataquality-link", style={"color": "white"}),
                dbc.NavLink([html.I(className="fas fa-search", style={"margin-right": "10px"}),
                             "Gap Analysis"], href="/gapanalysis", id="gapanalysis-link", style={"color": "white"}),
                dbc.NavLink([html.I(className="fas fa-download", style={"margin-right": "10px"}),
                             "Téléchargement"], href="/download", id="download-link", style={"color": "white"}),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style={"position": "fixed", "top": "0", "left": "0", "bottom": "0", "width": "250px",
           "background-color": "black", "padding": "20px", "color": "white"},
)

# Bouton de basculement de la langue
language_toggle = html.Div([dbc.Button(id="language-toggle", children="Français",
                                       color="primary", style={"position": "absolute", "top": "10px", "right": "10px"})])

# Zone de contenu principal
main_content = html.Div(
    [
        html.H1("Titrisation", style={"background-color": "red", "color": "white", "padding": "10px"}),
        language_toggle,
        html.Div(id="tab-content", style={"padding": "20px"}),
        dcc.Interval(id="interval", interval=1000, n_intervals=0, disabled=True),
    ],
    style={"margin-left": "250px", "padding": "20px"},
)

# Mise en page avec Font Awesome inclus
app.layout = html.Div(
    [
        html.Link(rel="stylesheet",
                  href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css"),
        sidebar,
        main_content,
        dcc.Location(id='url', refresh=False),
        dcc.Store(id='language-store', data='fr'),
    ]
)

# Rappel pour changer le contenu en fonction de l'URL active
@app.callback(Output("tab-content", "children"),
              Input("url",
                    "pathname"), State('language-store', 'data'))
def display_content(pathname, language):
    if pathname == "/accueil":
        return get_accueil_content(language)
    elif pathname == "/datapacks":
        return datapacks_content
    elif pathname == "/dataquality":
        return data_quality_content
    elif pathname == "/gapanalysis":
        return gap_analysis_content
    elif pathname == "/download":
        return download_content
    return get_accueil_content(language)

# Rappel pour basculer la langue
@app.callback([Output('language-store', 'data'),
               Output('language-toggle', 'children')],
              Input('language-toggle', 'n_clicks'),
              State('language-store', 'data'))
def toggle_language(n_clicks, current_language):
    if n_clicks is None:
        return current_language, LANGUAGES[current_language]
    new_language = "en" if current_language == "fr" else "fr"
    return new_language, LANGUAGES[new_language]



# Rappel pour gérer le clic sur le bouton, la progression et le téléchargement
@app.callback(
    [Output("progress-bar-datapack", "value"),
     Output("log-output-datapack", "children"),
     Output("btn-download-datapack", "style"),
     Output("download-link", "href"),
     Output("interval-datapack", "disabled")],
    [Input("btn-start-datapack", "n_clicks"), Input("interval-datapack", "n_intervals")]
)
def update_progress(n_clicks, n_intervals):
    triggered_id = ctx.triggered_id

    if triggered_id == "btn-start-datapack":
        # Démarrer le processus dans un thread séparé
        thread = threading.Thread(target=start_process)
        thread.start()

        # Initialement, afficher le statut de traitement
        return 0, "🚀 Traitement en cours...", {"display": "none"}, "", False

    elif triggered_id == "interval-datapack":
        # Simuler la progression à des fins de démonstration
        progress_state = get_progress()  # Cela devrait appeler votre fonction de suivi de progression réelle
        progress = progress_state["progress"]
        message = progress_state["message"]

        if progress == 100:
            # Afficher le bouton de téléchargement lorsque terminé
            return (
                progress,
                message,
                {"display": "block", "background-color": "#28a745", "color": "white", "padding": "10px 20px", "border": "none", "border-radius": "5px", "cursor": "pointer", "margin-top": "20px"},
                f"/download/",
                True
            )

        return progress, message, {"display": "none"}, "", False

    return no_update, no_update, no_update, no_update, no_update

# Route pour le téléchargement de fichier
@app.server.route("/download/<path:filename>")
def download_file_route(filename):
    return send_from_directory(OUTPUT_DIR, filename, as_attachment=True)

# Rappel pour générer le rapport de qualité des données

# Bouton de téléchargement du rapport de qualité des données
download_button_dq = dbc.Button(
    "Télécharger le Rapport de Qualité des Données",
    id="btn-download-report",
    color="primary",
    size="lg",
    style={"margin-top": "20px", "padding": "10px 20px", "width": "auto"}
)

@app.callback(
    [
        Output('data-quality-report', 'children'),
        Output('missing-data-graph', 'figure'),
        Output('data-distribution-graph', 'figure'),
        Output('missing-data-heatmap', 'figure'),
        Output('correlation-matrix', 'figure'),
        Output('outliers-detection', 'figure'),
        Output('data-quality-table', 'columns'),
        Output('data-quality-table', 'data')
    ],
    Input('url', 'pathname')
)
def generate_data_quality_report(pathname):
    if pathname == "/dataquality":
        try:
            # Load the data
            df = load_data(input_file)

            # Vérification des types de données dans le DataFrame
            print(df.dtypes)

            # Générer le rapport de qualité des données
            report = data_quality_report(df, id_column='id')

            # Filtrer uniquement les colonnes numériques
            numeric_df = df.select_dtypes(include='number')

            # Missing data graph (Bar plot)
            missing_data_fig = px.bar(
                report['missing_per_variable'].reset_index(),
                x='index',
                y=0,
                labels={'index': 'Variables', '0': 'Missing Values'},
                title='Missing Values per Variable'
            )

            # Data distribution graph (Histogram for all columns)
            data_distribution_fig = px.histogram(numeric_df, title='Data Distribution')

            # Missing data heatmap (Visualize missing data)
            missing_data_heatmap_fig = px.imshow(
                df.isnull(),
                title='Missing Data Heatmap'
            )

            # Correlation matrix (Correlation heatmap)
            correlation_matrix_fig = px.imshow(
                numeric_df.corr(),
                title='Correlation Matrix'
            )

            # Outliers detection (Box plot for numerical columns)
            outliers_detection_fig = px.box(
                numeric_df,
                title='Outliers Detection'
            )

            # Data quality table (Table with missing and duplicate information)
            data_quality_table_columns = [{"name": i, "id": i} for i in report['missing_per_variable'].index]
            data_quality_table_data = [{"Variable": k, "Missing Values": v} for k, v in
                                       report['missing_per_variable'].items()]

            return (
                f"Total Missing Values: {report['total_missing']}",
                missing_data_fig,
                data_distribution_fig,
                missing_data_heatmap_fig,
                correlation_matrix_fig,
                outliers_detection_fig,
                data_quality_table_columns,
                data_quality_table_data
            )
        except Exception as e:
            print(f"Error generating data quality report: {e}")
            return str(e), {}, {}, {}, {}, {}, [], []
    return {}, {}, {}, {}, {}, {}, [], []

if __name__ == "__main__":
    app.run_server(debug=True)