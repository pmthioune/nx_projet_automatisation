from dash import html, dcc

layout = html.Div([
    html.H4("Analyse de la Qualité des Données"),
    dcc.Graph(id="missing-values-graph"),
    dcc.Graph(id="outliers-graph"),
    dcc.Graph(id="duplicates-graph"),
    html.Button("Générer le rapport", id="generate-report-btn")
])
