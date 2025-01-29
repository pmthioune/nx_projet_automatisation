from dash import html, dcc

layout = html.Div([
    html.H4("Analyse des Écarts"),
    dcc.Dropdown(
        id="select-datapacks",
        options=[{"label": f"Datapack {i}", "value": f"datapack_{i}"} for i in range(1, 6)],
        placeholder="Sélectionnez les datapacks",
        multi=True
    ),
    dcc.Graph(id="comparison-graph")
])
