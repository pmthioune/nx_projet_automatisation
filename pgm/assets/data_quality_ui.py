from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc

# Content for Data Quality section
data_quality_content = html.Div(
    [
        html.H3("Data Quality Analysis", style={"color": "#FF5733", "margin-bottom": "20px"}),
        dcc.Dropdown(id='variable-selector', options=[], multi=True, placeholder="Select variables"),
        dcc.Graph(id='missing-data-graph'),
        dcc.Graph(id='outliers-detection'),
        dcc.Graph(id='duplicates-graph'),
        dcc.Graph(id='data-distribution-graph'),
        dcc.Graph(id='correlation-matrix'),
        html.H4("Detailed DQ Report", style={"color": "#FF5733", "margin-top": "20px"}),
        html.H4("Résumé des variables sélectionnées", style={"textAlign": "center", "color": "#2c3e50"}),
        html.Div(id='variables-summary'),
        html.Div(id='data-quality-report'),
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