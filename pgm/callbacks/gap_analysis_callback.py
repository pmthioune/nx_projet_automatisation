import os
import pandas as pd
import plotly.express as px
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import logging
from pgm.assets.data_import import load_data
from pgm.assets.data_quality import data_quality_report

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def register_gap_analysis_callbacks(app):
    # Chemins d'accès
    OUTPUT_DIR = os.path.join(os.path.expanduser("~"), "Desktop", "DASH", "Dash", "nx_projet_automatisation", "output")
    INPUT_DIR = os.path.join(os.path.expanduser("~"), "Desktop", "DASH", "Dash", "nx_projet_automatisation", "input")

    # Créer le répertoire de sortie s'il n'existe pas
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    @app.callback(
        [
            Output('total-missing-values', 'children'),
            Output('total-duplicates', 'children'),
            Output('total-outliers', 'children'),
            Output('timeliness', 'children'),
            Output('missing-data-graph', 'figure'),
            Output('outliers-detection', 'figure'),
            Output('z-score-detection', 'figure'),
            Output('duplicates-by-key-graph', 'figure'),
            Output('data-quality-table', 'columns'),
            Output('data-quality-table', 'data'),
            Output('gap-analysis-summary', 'children'),
            Output('df-selector-1', 'options'),
            Output('df-selector-2', 'options'),
            Output('error-message', 'children'),  # Ajout d'un message d'erreur
        ],
        [
            Input('url', 'pathname'),
            Input('df-selector-1', 'value'),
            Input('df-selector-2', 'value'),
            Input('run-gap-analysis', 'n_clicks'),  # Ajout du bouton pour lancer l'analyse
        ]
    )
    def generate_gap_analysis(pathname, df1_name, df2_name, n_clicks):
        # Vérifier si l'utilisateur est sur la bonne page
        if pathname != "/gapanalysis":
            return [None] * 13  # Retourner des valeurs vides pour tous les outputs

        try:
            # Charger les fichiers disponibles
            available_files = [f for f in os.listdir(INPUT_DIR) if f.endswith('.csv')]
            df_options = [{'label': f, 'value': f} for f in available_files]

            # Vérifier si deux fichiers sont sélectionnés
            if not df1_name or not df2_name:
                return (
                    None, None, None, None, None, None, None, None, None, None,
                    html.P("Veuillez sélectionner deux fichiers.", style={"color": "red"}),
                    df_options, df_options, None
                )

            # Charger les DataFrames
            df1 = pd.read_csv(os.path.join(INPUT_DIR, df1_name))
            df2 = pd.read_csv(os.path.join(INPUT_DIR, df2_name))

            logger.info(f"✅ DataFrames chargés : {df1_name} et {df2_name}")

            # Générer les rapports de qualité
            report1 = data_quality_report(df1, id_column='id')
            report2 = data_quality_report(df2, id_column='id')

            # Calculer les écarts
            gap_missing = report1['total_missing'] - report2['total_missing']
            gap_duplicates = report1['duplicates'] - report2['duplicates']
            gap_outliers = report1['outliers'].sum() - report2['outliers'].sum()

            # Graphiques
            missing_data_fig = px.bar(
                pd.DataFrame({
                    'Variable': report1['missing_per_variable'].index,
                    'DF1': report1['missing_per_variable'].values,
                    'DF2': report2['missing_per_variable'].values
                }).melt(id_vars=['Variable'], var_name="DataFrame", value_name="Missing Values"),
                x='Variable',
                y='Missing Values',
                color='DataFrame',
                barmode='group',
                title="Comparaison des valeurs manquantes"
            )

            outliers_detection_fig = px.box(
                pd.concat([df1.select_dtypes(include='number').assign(Source='DF1'),
                           df2.select_dtypes(include='number').assign(Source='DF2')]),
                x='Source',
                y='value',
                title="Comparaison des outliers"
            )

            duplicates_by_key_fig = px.bar(
                pd.DataFrame({
                    'DataFrame': ['DF1', 'DF2'],
                    'Duplicates': [report1['duplicates'], report2['duplicates']]
                }),
                x='DataFrame',
                y='Duplicates',
                title="Comparaison des doublons"
            )

            # Tableau de qualité des données
            data_quality_table_columns = [
                {"name": "Variable", "id": "Variable"},
                {"name": "Missing Values DF1 (%)", "id": "Missing DF1"},
                {"name": "Missing Values DF2 (%)", "id": "Missing DF2"},
                {"name": "Outliers DF1 (%)", "id": "Outliers DF1"},
                {"name": "Outliers DF2 (%)", "id": "Outliers DF2"}
            ]

            data_quality_table_data = [
                {
                    "Variable": var,
                    "Missing DF1": f"{(val1 / len(df1)) * 100:.2f}%",
                    "Missing DF2": f"{(val2 / len(df2)) * 100:.2f}%",
                    "Outliers DF1": f"{(report1['outliers'][var] / len(df1)) * 100:.2f}%" if var in report1['outliers'] else "0%",
                    "Outliers DF2": f"{(report2['outliers'][var] / len(df2)) * 100:.2f}%" if var in report2['outliers'] else "0%"
                }
                for var, (val1, val2) in zip(report1['missing_per_variable'].index,
                                             zip(report1['missing_per_variable'], report2['missing_per_variable']))
            ]

            # Résumé de l'analyse
            gap_analysis_summary = html.Div([
                html.P(f"Comparaison entre {df1_name} et {df2_name}"),
                html.P(f"Écart des valeurs manquantes: {gap_missing}"),
                html.P(f"Écart des doublons: {gap_duplicates}"),
                html.P(f"Écart des outliers: {gap_outliers}")
            ])

            return (
                f"Écart des valeurs manquantes: {gap_missing}",
                f"Écart des doublons: {gap_duplicates}",
                f"Écart des outliers: {gap_outliers}",
                None,
                missing_data_fig,
                outliers_detection_fig,
                None,
                duplicates_by_key_fig,
                data_quality_table_columns,
                data_quality_table_data,
                gap_analysis_summary,
                df_options,
                df_options,
                None  # Pas d'erreur
            )

        except Exception as e:
            logger.error(f"❌ Erreur lors de l'analyse : {e}")
            return (
                None, None, None, None, None, None, None, None, None, None,
                html.P("Erreur lors de l'analyse. Vérifiez les fichiers sélectionnés.", style={"color": "red"}),
                [], [], str(e)  # Message d'erreur
            )
