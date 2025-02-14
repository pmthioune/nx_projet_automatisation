
from dash import html, dcc, dash_table


# Content for Data Quality section
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
        html.H4("Data Quality Report", style={"color": "#FF5733", "margin-top": "20px"}),
        html.Div(id='data-quality-report'),
        html.H4("Detailed Data Quality Report", style={"color": "#FF5733", "margin-top": "20px"}),
        dash_table.DataTable(
            id='data-quality-table',
            columns=[],
            data=[],
            style_table={'overflowX': 'auto'},
            style_header={
                'backgroundColor': 'rgb(30, 30, 30)',
                'color': 'white'
            },
            style_cell={
                'backgroundColor': 'rgb(50, 50, 50)',
                'color': 'white'
            }
        ),
    ],
    style={"padding": "20px", "background-color": "#f9f9f9", "border-radius": "8px", "border": "1px solid #ddd"},
)
