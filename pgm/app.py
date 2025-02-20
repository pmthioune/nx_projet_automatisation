import dash
from dash import html, dcc, Input, Output
from sidebar import sidebar
import datapacks
import data_quality
import gap_analysis

# Initialiser l'application Dash
app = dash.Dash(__name__, suppress_callback_exceptions=True)
app.title = "Analyse des Données"

# Mise en page principale avec sidebar
app.layout = html.Div([
    dcc.Location(id="url", refresh=False),  # Gère la navigation entre pages
    sidebar,
    html.Div(id="page-content", style={"marginLeft": "250px", "padding": "20px"})
])

# Callback pour gérer la navigation
@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def display_page(pathname):
    if pathname == "/data_quality":
        return data_quality.layout
    elif pathname == "/gap_analysis":
        return gap_analysis.layout
    elif pathname == "/datapacks":
        return datapacks.layout
    else:
        return html.Div([
            html.H1("Bienvenue sur l'outil d'Analyse des Données"),
            html.P("Sélectionnez une section à gauche pour commencer.")
        ])

# Lancer l'application
if __name__ == "__main__":
    app.run_server(debug=True)
