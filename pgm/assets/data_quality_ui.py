from dash import html, dcc

layout = html.Div(
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