from dash import html, dcc, Input, Output, State, ctx, no_update
import os
import plotly.express as px
from pgm.assets.data_import import load_data
from pgm.assets.data_quality import data_quality_report



def register_data_quality_callbacks(app):
    OUTPUT_DIR = r"C:\Users\FayçalOUSSEINIMALI\Desktop\DASH\Dash\nx_projet_automatisation\output"
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    INPUT_DIR = r"C:\Users\FayçalOUSSEINIMALI\Desktop\DASH\Dash\nx_projet_automatisation\input"
    input_file = os.path.join(INPUT_DIR, 'demographic_data.csv')

    @app.callback(
        [
            Output('total-missing-values', 'children'),
            Output('total-duplicates', 'children'),
            Output('total-outliers', 'children'),
            Output('timeliness', 'children'),
            Output('missing-data-graph', 'figure'),
            Output('outliers-detection', 'figure'),
            Output('duplicates-by-key-graph', 'figure'),
            Output('data-quality-table', 'columns'),
            Output('data-quality-table', 'data'),
            Output('variable-selector', 'options'),
            Output('duplicate-key-selector', 'options'),
            Output('duplicates-graph', 'children'),
            Output('data-description', 'children')
        ],
        [
            Input('url', 'pathname'),
            Input('variable-selector', 'value'),
            Input('duplicate-key-selector', 'value')
        ]
    )
    def generate_data_quality_report(pathname, selected_variables, duplicate_key):
        print(f"Pathname: {pathname}")
        print(f"Selected variables: {selected_variables}")
        print(f"Duplicate key: {duplicate_key}")

        if pathname == "/dataquality":
            try:
                # Charger les données
                df = load_data(input_file)
                print("Data loaded successfully")

                # Générer le rapport de qualité des données
                report = data_quality_report(df, id_column='id')
                print("Data quality report generated")

                # Sélectionner uniquement les colonnes numériques
                numeric_df = df.select_dtypes(include='number')
                print("Numeric columns selected")

                # Options pour le dropdown
                variable_options = [{'label': col, 'value': col} for col in df.columns]
                print("Variable options created")

                # KPI values
                total_rows = len(df)
                total_missing_values = (f"Total Missing Values: {report['total_missing']} "
                                        f"({(report['total_missing'] / (total_rows * len(df.columns))) * 100:.2f}%)")
                total_duplicates = (f"Total Duplicates: {report['duplicates']} "
                                    f"({(report['duplicates'] / total_rows) * 100:.2f}%)")
                total_outliers = (f"Total Outliers: {report['outliers'].sum()} "
                                  f"({(report['outliers'].sum() / total_rows) * 100:.2f}%)")
                timeliness = f"Timeliness (days): {report['timeliness']}"

                # Graphique des valeurs manquantes
                missing_data_fig = px.bar(
                    report['missing_per_variable'].reset_index(),
                    x='index',
                    y=0,
                    title='Missing Values per Variable',
                    labels={'index': 'Variable', 0: 'Missing Values'},
                    color='index',
                    color_discrete_sequence=px.colors.qualitative.Plotly
                )
                print("Missing data figure created")

                missing_data_fig.update_layout(
                    title={
                        'text': "Missing Values per Variable",
                        'y': 0.9,
                        'x': 0.5,
                        'xanchor': 'center',
                        'yanchor': 'top'
                    },
                    xaxis_title="Variables",
                    yaxis_title="Number of Missing Values",
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(
                        family="Arial, sans-serif",
                        size=12,
                        color="RebeccaPurple"
                    )
                )

                missing_data_fig.update_traces(marker=dict(line=dict(width=1, color='DarkSlateGrey')))

                # Graphique de détection des outliers
                outliers_detection_fig = px.box(
                    numeric_df,
                    title='Outliers Detection',
                    labels={'value': 'Value', 'variable': 'Variable'},
                    color_discrete_sequence=px.colors.qualitative.Plotly
                )
                print("Outliers detection figure created")

                outliers_detection_fig.update_layout(
                    title={
                        'text': "Outliers per variable",
                        'y': 0.9,
                        'x': 0.5,
                        'xanchor': 'center',
                        'yanchor': 'top'
                    },
                    xaxis_title="Variables",
                    yaxis_title="Values",
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(
                        family="Arial, sans-serif",
                        size=12,
                        color="RebeccaPurple"
                    )
                )

                outliers_detection_fig.update_traces(marker=dict(line=dict(width=1, color='DarkSlateGrey')))

                # Texte explicatif pour les doublons
                if report['duplicates'] > 0:
                    duplicates_text = html.Div([
                        html.P(f"Il y a {report['duplicates']} valeurs dupliquées dans les données."),
                        html.P(
                            f"Ce qui représente {(report['duplicates'] / total_rows) * 100:.2f}% du total des lignes.")
                    ])
                else:
                    duplicates_text = html.P("Aucune valeur dupliquée trouvée dans les données.")
                print("Duplicates text created")

                # Graphique des doublons par clé
                if duplicate_key:
                    duplicates_by_key = df[df.duplicated(subset=[duplicate_key], keep=False)]
                    duplicates_by_key_fig = px.histogram(
                        duplicates_by_key,
                        x=duplicate_key,
                        title=f'Duplicates by {duplicate_key}'
                    )
                else:
                    duplicates_by_key_fig = {}
                print("Duplicates by key figure created")

                # Table globale de DQ
                data_quality_table_columns = [
                    {"name": "Variable", "id": "Variable"},
                    {"name": "Missing Values (%)", "id": "Missing Values (%)"},
                    {"name": "Duplicates (%)", "id": "Duplicates (%)"},
                    {"name": "Outliers (%)", "id": "Outliers (%)"}
                ]

                data_quality_table_data = [
                    {
                        "Variable": var,
                        "Missing Values": val,
                        "Missing Values (%)": f"{(val / total_rows) * 100:.2f}%",
                        "Duplicates": report['duplicates_by_id'] if var == 'id' else '',
                        "Duplicates (%)": f"{(report['duplicates_by_id'] / total_rows) * 100:.2f}%" if var == 'id' else '',
                        "Outliers": report['outliers'][var] if var in report['outliers'] else '',
                        "Outliers (%)": f"{(report['outliers'][var] / total_rows) * 100:.2f}%" if var in report[
                            'outliers'] else ''
                    }
                    for var, val in report['missing_per_variable'].items()
                ]
                print("Data quality table created")

                # Description de la base de données et des statistiques descriptives
                data_description = html.Div([
                    html.Ul([html.Li(f"Variable: {var}") for var in df.columns])
                ])
                print("Data description created")

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
                print("Summary created")

                return (
                    total_missing_values,
                    total_duplicates,
                    total_outliers,
                    timeliness,
                    missing_data_fig,
                    outliers_detection_fig,
                    duplicates_by_key_fig,
                    data_quality_table_columns,
                    data_quality_table_data,
                    variable_options,
                    variable_options,
                    duplicates_text,
                    data_description
                )
            except Exception as e:
                print(f"Error generating data quality report: {e}")
                return str(e), {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}
        return {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}