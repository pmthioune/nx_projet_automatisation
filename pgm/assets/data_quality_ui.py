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
                        dbc.Col(html.Div(id='total-missing-values', className='kpi-box'), width=3),
                        dbc.Col(html.Div(id='total-duplicates', className='kpi-box'), width=3),
                        dbc.Col(html.Div(id='total-outliers', className='kpi-box'), width=3),
                        dbc.Col(html.Div(id='timeliness', className='kpi-box'), width=3),
                    ],
                    className="kpi-row"
                ),
            ],
            className="kpi-section"
        ),

        # Graphs for data quality metrics
        dcc.Graph(id='missing-data-graph'),
        dcc.Graph(id='outliers-detection'),
        dcc.Graph(id='duplicates-graph'),
        dcc.Graph(id='data-distribution-graph'),
        dcc.Graph(id='correlation-matrix'),

        html.H4("Detailed DQ Report", style={"color": "#FF5733", "margin-top": "20px"}),

        # Dropdown for selecting variables
        dcc.Dropdown(id='variable-selector', options=[], multi=True, placeholder="Select variables"),

        html.H4("DQ Sum up", style={"textAlign": "center", "color": "#2c3e50"}),

        # Summary of selected variables
        html.Div(id='variables-summary'),

        # Data quality report
        html.Div(id='data-quality-report'),

        # Data quality table
        dash_table.DataTable(
            id='data-quality-table',
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
        ),

        html.H4("Statistiques Descriptives", style={"color": "#FF5733", "margin-top": "20px"}),

        # Descriptive statistics table
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