from dash import Input, Output, State, ctx, no_update
import threading
import pandas as pd
import os
from dash import html, dcc
from assets.data_import import load_data
from assets.data_quality import data_quality_report, save_data_quality_report
import plotly.express as px
from main import start_process, get_progress

OUTPUT_DIR = '../../output'
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

INPUT_DIR = r"C:\Users\FayçalOUSSEINIMALI\Desktop\DASH\Dash\nx_projet_automatisation\input"
input_file = os.path.join(INPUT_DIR, 'demographic_data.csv')

LANGUAGES = {
    "fr": "Français",
    "en": "English"
}

def register_callbacks(app):
    @app.callback(Output("tab-content", "children"),
                  Input("url", "pathname"), State('language-store', 'data'))
    def display_content(pathname, language):
        from assets.accueil_ui import get_accueil_content
        from assets.datapacks_ui import datapacks_content
        from assets.data_quality_ui import data_quality_content
        from assets.gap_analysis_ui import gap_analysis_content
        from assets.download_ui import download_content

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

    @app.callback([Output('language-store', 'data'),
                   Output('language-toggle', 'children')],
                  Input('language-toggle', 'n_clicks'),
                  State('language-store', 'data'))
    def toggle_language(n_clicks, current_language):
        if n_clicks is None:
            return current_language, LANGUAGES[current_language]
        new_language = "en" if current_language == "fr" else "fr"
        return new_language, LANGUAGES[new_language]

    @app.callback(
        [
            Output('total-missing-values', 'children'),
            Output('total-duplicates', 'children'),
            Output('total-outliers', 'children'),
            Output('timeliness', 'children'),
            Output('missing-data-graph', 'figure'),
            Output('data-distribution-graph', 'figure'),
            Output('outliers-detection', 'figure'),
            Output('correlation-matrix', 'figure'),
            Output('duplicates-graph', 'figure'),
            Output('data-quality-table', 'columns'),
            Output('data-quality-table', 'data'),
            Output('variable-selector', 'options'),
            Output('variables-summary', 'children'),
            Output('descriptive-stats-table', 'columns'),
            Output('descriptive-stats-table', 'data')
        ],
        [Input('url', 'pathname'), Input('variable-selector', 'value')]
    )
    def generate_data_quality_report(pathname, selected_variables):
        if pathname == "/dataquality":
            try:
                # Charger les données
                df = load_data(input_file)
                # Générer le rapport de qualité des données
                report = data_quality_report(df, id_column='id')
                # Sélectionner uniquement les colonnes numériques
                numeric_df = df.select_dtypes(include='number')
                # Options pour le dropdown
                variable_options = [{'label': col, 'value': col} for col in df.columns]
                # Enregistrer le rapport de qualité des données
                save_data_quality_report(report)

                # KPI values
                total_rows = len(df)
                total_missing_values = f"Total Missing Values: {report['total_missing']} ({(report['total_missing'] / (total_rows * len(df.columns))) * 100:.2f}%)"
                total_duplicates = f"Total Duplicates: {report['duplicates']} ({(report['duplicates'] / total_rows) * 100:.2f}%)"
                total_outliers = f"Total Outliers: {report['outliers'].sum()} ({(report['outliers'].sum() / total_rows) * 100:.2f}%)"
                timeliness = f"Timeliness (days): {report['timeliness']}"

                # Graphique des valeurs manquantes
                missing_data_fig = px.bar(
                    report['missing_per_variable'].reset_index(),
                    x='index',
                    y=0,
                    title='Missing Values per Variable'
                )

                # Graphique de détection des outliers
                outliers_detection_fig = px.box(numeric_df, title='Outliers Detection')
                # Graphique de distribution des données
                data_distribution_fig = px.histogram(numeric_df, title='Data Distribution')
                # Matrice de corrélation
                correlation_matrix_fig = px.imshow(numeric_df.corr(), title='Correlation Matrix')

                # Graphique des doublons
                duplicates_fig = px.bar(
                    pd.DataFrame({
                        'Variable': ['Total Duplicates', 'Duplicates by ID'],
                        'Count': [report['duplicates'], report['duplicates_by_id']]
                    }),
                    x='Variable',
                    y='Count',
                    title='Duplicate Values'
                )

                # Résumé des variables sélectionnées
                if not selected_variables:
                    summary = "Aucune variable sélectionnée."
                    descriptive_stats_columns = []
                    descriptive_stats_data = []
                else:
                    summary = [html.P(f"Variable: {var}") for var in selected_variables]
                    desc_df = df[selected_variables].describe().reset_index()
                    summary.append(html.P(desc_df.to_string()))

                    descriptive_stats_columns = [{"name": i, "id": i} for i in desc_df.columns]
                    descriptive_stats_data = desc_df.to_dict('records')

                # Colonnes et données pour le tableau de qualité des données
                data_quality_table_columns = [
                    {"name": "Variable", "id": "Variable"},
                    {"name": "Missing Values", "id": "Missing Values"},
                    {"name": "Duplicates", "id": "Duplicates"}
                ]
                data_quality_table_data = [
                    {"Variable": var, "Missing Values": val,
                     "Duplicates": report['duplicates_by_id'] if var == 'id' else ''}
                    for var, val in report['missing_per_variable'].items()
                ]

                return (
                    total_missing_values,
                    total_duplicates,
                    total_outliers,
                    timeliness,
                    missing_data_fig,
                    data_distribution_fig,
                    outliers_detection_fig,
                    correlation_matrix_fig,
                    duplicates_fig,
                    data_quality_table_columns,
                    data_quality_table_data,
                    variable_options,
                    summary,
                    descriptive_stats_columns,
                    descriptive_stats_data
                )
            except Exception as e:
                print(f"Error generating data quality report: {e}")
                return str(e), {}, {}, {}, {}, {}, [], [], [], [], [], [], [], []
        return {}, {}, {}, {}, {}, {}, [], [], [], [], [], [], [], []

    @app.callback(
        [
            Output("progress-bar-datapack", "value"),
            Output("log-output-datapack", "children"),
            Output("btn-download-datapack", "style"),
            Output("download-link", "href"),
            Output("interval-datapack", "disabled")
        ],
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
                    {"display": "block", "background-color": "#28a745", "color": "white", "padding": "10px 20px",
                     "border": "none", "border-radius": "5px", "cursor": "pointer", "margin-top": "20px"},
                    f"/download/",
                    True
                )

            return progress, message, {"display": "none"}, "", False

        return no_update, no_update, no_update, no_update, no_update

    @app.callback(
        Output("download-report", "data"),
        Input("download-report", "n_clicks"),
        State("data-quality-table", "data"),
        prevent_initial_call=True
    )
    def download_report(n_clicks, table_data):
        df = pd.DataFrame(table_data)
        return dcc.send_data_frame(df.to_csv, "data_quality_report.csv")
