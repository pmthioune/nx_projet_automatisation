from dash import Dash, html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
import time
import threading

# Créer l'application Dash
app = Dash(
    __name__,
    external_stylesheets=[
        "https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css",
        "https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&family=Source+Sans+Pro:wght@400;700&display=swap"
    ]
)

# Style général
header_style = {
    "backgroundColor": "rgb(233, 4, 30)",
    "padding": "10px",
    "display": "flex",
    "alignItems": "center",
    "justifyContent": "space-between",
}

title_style = {
    "color": "white",
    "fontFamily": "Montserrat",
    "fontSize": "20px",
    "margin": "0",
}

logo_style = {
    "height": "40px",
    "marginRight": "10px",
}

content_style = {
    "fontFamily": "Source Sans Pro",
    "fontSize": "16px",
    "padding": "20px",
}

# Mise en page de l'application
app.layout = html.Div(
    [
        # En-tête
        html.Div(
            [
                html.H1("Titrisation", style=title_style),
                html.Img(
                    src="https://upload.wikimedia.org/wikipedia/commons/e/e7/Logo_Soci%C3%A9t%C3%A9_G%C3%A9n%C3%A9rale.svg",
                    style=logo_style
                )
            ],
            style=header_style
        ),
        # Formulaire principal
        html.Div(
            [
                # Champ Id_datapack
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.Label("Id Datapack", style={"fontWeight": "bold"}),
                                dcc.Input(
                                    id="id-datapack",
                                    type="number",
                                    placeholder="Entrez un entier",
                                    style={"width": "100%"},
                                ),
                            ],
                            width=6
                        ),
                    ],
                    className="mb-3"
                ),
                # Liste déroulante Name_datapack
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.Label("Name Datapack", style={"fontWeight": "bold"}),
                                dcc.Dropdown(
                                    id="name-datapack",
                                    options=[
                                        {"label": "RACER", "value": "RACER"},
                                        {"label": "JUNON", "value": "JUNON"},
                                    ],
                                    placeholder="Sélectionnez un datapack",
                                    style={"width": "100%"}
                                ),
                            ],
                            width=6
                        ),
                    ],
                    className="mb-3"
                ),
                # Date Début et Date Fin
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.Label("Date Début", style={"fontWeight": "bold"}),
                                dcc.DatePickerSingle(
                                    id="start-date",
                                    display_format="YYYY/MM/DD",
                                    placeholder="YYYY/MM/DD",
                                    style={"width": "100%"}
                                ),
                            ],
                            width=6
                        ),
                        dbc.Col(
                            [
                                html.Label("Date Fin", style={"fontWeight": "bold"}),
                                dcc.DatePickerSingle(
                                    id="end-date",
                                    display_format="YYYY/MM/DD",
                                    placeholder="YYYY/MM/DD",
                                    style={"width": "100%"}
                                ),
                            ],
                            width=6
                        ),
                    ],
                    className="mb-3"
                ),
                # Bouton "Création Datapack"
                dbc.Row(
                    [
                        dbc.Col(
                            dbc.Button(
                                "Création Datapack",
                                id="create-datapack-btn",
                                color="primary",
                                className="mt-3",
                                style={"width": "100%"}
                            ),
                            width=6
                        )
                    ]
                ),
            ],
            style=content_style
        ),
        # Pop-Up de progression
        dbc.Modal(
            [
                dbc.ModalHeader("Progression"),
                dbc.ModalBody(
                    [
                        dbc.Progress(id="progress-bar", striped=True, animated=True, value=0),
                        html.Div(id="progress-text", className="mt-2", style={"textAlign": "center"})
                    ]
                ),
                dbc.ModalFooter(
                    dbc.Button("Fermer", id="close-modal", color="secondary", className="ms-auto", n_clicks=0)
                )
            ],
            id="progress-modal",
            is_open=False,
        )
    ]
)

# Callback pour ouvrir le modal et afficher la progression
@app.callback(
    [Output("progress-modal", "is_open"), Output("progress-bar", "value"), Output("progress-text", "children")],
    [Input("create-datapack-btn", "n_clicks"), Input("close-modal", "n_clicks")],
    [
        State("id-datapack", "value"),
        State("name-datapack", "value"),
        State("start-date", "date"),
        State("end-date", "date")
    ],
    prevent_initial_call=True
)
def create_datapack(n_clicks_create, n_clicks_close, id_datapack, name_datapack, start_date, end_date):
    # Si l'utilisateur ferme le modal
    if n_clicks_close:
        return False, 0, ""

    # Vérifier que les champs sont remplis
    if not all([id_datapack, name_datapack, start_date, end_date]):
        return False, 0, "Veuillez remplir tous les champs !"

    # Simuler une tâche avec progression
    progress = 0
    for i in range(1, 120, 20):
        time.sleep(0.5)
        progress = i

    return True, progress, f"Traitement en cours : {progress}%"

# Lancer l'application
if __name__ == "__main__":
    app.run_server(debug=True)
