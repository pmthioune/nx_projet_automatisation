import dash
from dash import dcc, html, Input, Output, State
import datetime
import subprocess

# Initialisation de l'application Dash
app = dash.Dash(__name__)
app.title = "Exécuter un programme avec Dash"

# Mise en page de l'application
app.layout = html.Div([
    html.H1("Exécuter le programme principal", style={'text-align': 'center'}),

    # Input pour id_datapack
    html.Div([
        html.Label("ID du datapack (entier):"),
        dcc.Input(id="id-datapack", type="number", placeholder="Entrez l'ID du datapack", style={'width': '100%'})
    ], style={'margin-bottom': '20px'}),

    # Input pour name_datapack
    html.Div([
        html.Label("Nom du datapack (texte):"),
        dcc.Input(id="name-datapack", type="text", placeholder="Entrez le nom du datapack", style={'width': '100%'})
    ], style={'margin-bottom': '20px'}),

    # Inputs pour extraction_date (début et fin)
    html.Div([
        html.Label("Date d'extraction (début):"),
        dcc.DatePickerSingle(
            id="start-date",
            placeholder="Choisissez une date de début",
            date=datetime.date.today()
        ),
        html.Br(),
        html.Label("Date d'extraction (fin):"),
        dcc.DatePickerSingle(
            id="end-date",
            placeholder="Choisissez une date de fin",
            date=datetime.date.today()
        )
    ], style={'margin-bottom': '20px'}),

    # Bouton pour exécuter le programme
    html.Button("Exécuter", id="run-button", n_clicks=0, style={'margin-top': '20px'}),

    # Section de sortie
    html.Div(id="output", style={'margin-top': '30px', 'whiteSpace': 'pre-line'})
])


# Callback pour exécuter le programme principal
@app.callback(
    Output("output", "children"),
    Input("run-button", "n_clicks"),
    State("id-datapack", "value"),
    State("name-datapack", "value"),
    State("start-date", "date"),
    State("end-date", "date")
)
def run_main(n_clicks, id_datapack, name_datapack, start_date, end_date):
    if n_clicks > 0:
        # Vérification des entrées utilisateur
        if id_datapack is None or name_datapack is None or start_date is None or end_date is None:
            return "Veuillez remplir tous les champs avant d'exécuter le programme."

        # Conversion des dates en chaînes lisibles
        start_date_str = str(start_date)
        end_date_str = str(end_date)

        # Commande pour exécuter le programme principal
        try:
            # Remplacez 'main.py' par le chemin vers votre script
            result = subprocess.run(
                ["python", "main.py",
                 str(id_datapack), name_datapack, start_date_str, end_date_str],
                text=True, capture_output=True
            )

            # Retourne le résultat de l'exécution
            if result.returncode == 0:
                return f"Programme exécuté avec succès !\n\nSortie :\n{result.stdout}"
            else:
                return f"Erreur lors de l'exécution du programme.\n\nSortie d'erreur :\n{result.stderr}"
        except Exception as e:
            return f"Une erreur est survenue : {str(e)}"
    return "Cliquez sur le bouton pour exécuter le programme."


# Lancer l'application Dash
if __name__ == "__main__":
    app.run_server(debug=True)
