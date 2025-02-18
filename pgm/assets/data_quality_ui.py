from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc

# Content for Data Quality section
data_quality_content = html.Div(
    [
        html.H3("Data Quality Analysis", style={"color": "#FF5733", "margin-bottom": "20px"}),

        # KPI Section
        html.Div(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            dbc.Card(
                                dbc.CardBody(
                                    [
                                        html.H5("Total Missing Values", className="card-title"),
                                        html.P(id='total-missing-values', className="card-text"),
                                    ]
                                ),
                                className="kpi-card",
                                style={"background-color": "#f8d7da", "color": "#721c24", "border": "1px solid #f5c6cb", "height": "100%"}
                            ),
                            width=3
                        ),
                        dbc.Col(
                            dbc.Card(
                                dbc.CardBody(
                                    [
                                        html.H5("Total Duplicates", className="card-title"),
                                        html.P(id='total-duplicates', className="card-text"),
                                    ]
                                ),
                                className="kpi-card",
                                style={"background-color": "#d1ecf1", "color": "#0c5460", "border": "1px solid #bee5eb", "height": "100%"}
                            ),
                            width=3
                        ),
                        dbc.Col(
                            dbc.Card(
                                dbc.CardBody(
                                    [
                                        html.H5("Total Outliers", className="card-title"),
                                        html.P(id='total-outliers', className="card-text"),
                                    ]
                                ),
                                className="kpi-card",
                                style={"background-color": "#fff3cd", "color": "#856404", "border": "1px solid #ffeeba", "height": "100%"}
                            ),
                            width=3
                        ),
                        dbc.Col(
                            dbc.Card(
                                dbc.CardBody(
                                    [
                                        html.H5("Timeliness", className="card-title"),
                                        html.P(id='timeliness', className="card-text"),
                                    ]
                                ),
                                className="kpi-card",
                                style={"background-color": "#d4edda", "color": "#155724", "border": "1px solid #c3e6cb", "height": "100%"}
                            ),
                            width=3
                        ),
                    ],
                    className="kpi-row"
                ),
            ],
            className="kpi-section"
        ),

        # Graphs for data quality metrics
        dbc.Card(
            dbc.CardBody(
                [
                    html.H5("Missing Data", className="card-title"),
                    dcc.Graph(id='missing-data-graph')
                ]
            ),
            className="mt-4",
            style={"background-color": "#f8f9fa", "border": "1px solid #dee2e6"}
        ),
        dbc.Card(
            dbc.CardBody(
                [
                    html.H5("Outliers Detection", className="card-title"),
                    dcc.Graph(id='outliers-detection')
                ]
            ),
            className="mt-4",
            style={"background-color": "#f8f9fa", "border": "1px solid #dee2e6"}
        ),

        # Placeholder for the duplicates text
        dbc.Card(
            dbc.CardBody(
                [
                    html.H5("Duplicate Values Analysis", className="card-title"),
                    html.Div(id='duplicates-graph', className="card-text"),
                    html.H6("Duplicates by Key", className="card-title mt-3"),
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

        html.H4("Detailed DQ Report", style={"color": "#FF5733", "margin-top": "20px"}),

        # Data quality table
        dbc.Card(
            dbc.CardBody(
                [
                    html.H5("Data Quality Table", className="card-title"),
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
            style={"background-color": "#f8f9fa", "border": "1px solid #dee2e6"}
        ),

        # Summary of selected variables
        dbc.Card(
            dbc.CardBody(
                [
                    html.H5("Summary of Selected Variables", className="card-title"),
                    html.Div(id='variables-summary', className="card-text")
                ]
            ),
            className="mt-4",
            style={"background-color": "#f8f9fa", "border": "1px solid #dee2e6"}
        ),

        # Dropdown for selecting variables
        dbc.Card(
            dbc.CardBody(
                [
                    html.H5("Select Variables", className="card-title"),
                    dcc.Dropdown(id='variable-selector', options=[], multi=True, placeholder="Select variables")
                ]
            ),
            className="mt-4",
            style={"background-color": "#f8f9fa", "border": "1px solid #dee2e6"}
        ),

        # Data quality report
        dbc.Card(
            dbc.CardBody(
                [
                    html.H5("Data Quality Report", className="card-title"),
                    html.Div(id='data-quality-report', className="card-text")
                ]
            ),
            className="mt-4",
            style={"background-color": "#f8f9fa", "border": "1px solid #dee2e6"}
        ),

        html.H4("Statistiques Descriptives", style={"color": "#FF5733", "margin-top": "20px"}),

        # Descriptive statistics table
        dbc.Card(
            dbc.CardBody(
                [
                    html.H5("Descriptive Statistics", className="card-title"),
                    dash_table.DataTable(
                        id='descriptive-stats-table',
                        columns=[],
                        data=[],
                        style_table={'overflowX': 'auto'},
                        style_header={
                            'backgroundColor': 'rgb(30, 30, 30)',
                            'color': 'white',
                            'fontWeight': 'bold',
                            'textAlign': 'center'
                        },
                        style_cell={
                            'backgroundColor': 'rgb(50, 50, 50)',
                            'color': 'white',
                            'textAlign': 'left',
                            'padding': '10px'
                        },
                        style_data_conditional=[
                            {'if': {'row_index': 'odd'}, 'backgroundColor': 'rgb(40, 40, 40)'}
                        ]
                    )
                ]
            ),
            className="mt-4",
            style={"background-color": "#f8f9fa", "border": "1px solid #dee2e6"}
        ),

        dbc.Card(
            dbc.CardBody(
                [
                    html.H5("Data Distribution", className="card-title"),
                    dcc.Graph(id='data-distribution-graph')
                ]
            ),
            className="mt-4",
            style={"background-color": "#f8f9fa", "border": "1px solid #dee2e6"}
        ),
        dbc.Card(
            dbc.CardBody(
                [
                    html.H5("Correlation Matrix", className="card-title"),
                    dcc.Graph(id='correlation-matrix')
                ]
            ),
            className="mt-4",
            style={"background-color": "#f8f9fa", "border": "1px solid #dee2e6"}
        ),


        # Button to download the report
        dbc.Button(
            "Télécharger le rapport",
            id="download-report",
            color="primary",
            size="lg",
            style={"margin-top": "20px", "padding": "10px 20px", "width": "auto"}
        ),
        dcc.Download(id="download-report")
    ],
    style={"padding": "20px", "background-color": "#f9f9f9", "border-radius": "8px", "border": "1px solid #ddd"},
)