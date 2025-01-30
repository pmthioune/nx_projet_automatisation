import dash
from dash import dcc, html, Input, Output

app = dash.Dash(__name__)

# 🔹 Mapping des indicateurs par Datapack
indicateurs_par_datapack = {
    "RACER": [f"Indicateur {i}" for i in range(1, 11)],  # 10 indicateurs pour RACER
    "JUNON": [f"Indicateur {i}" for i in range(11, 21)]  # 10 autres indicateurs pour JUNON
}

app.layout = html.Div([
    # 🔹 Sélection du Datapack
    dcc.Dropdown(
        id="dropdown-datapack",
        options=[
            {"label": "RACER", "value": "RACER"},
            {"label": "JUNON", "value": "JUNON"}
        ],
        value="RACER",  # Valeur par défaut
        placeholder="Sélectionnez un Datapack"
    ),

    # 🔹 Dropdown des indicateurs (mis à jour dynamiquement)
    dcc.Dropdown(
        id="dropdown-indicateurs",
        multi=True,  # Sélection multiple
        placeholder="Sélectionnez les indicateurs"
    )
])

# 🔹 Callback pour mettre à jour les indicateurs en fonction du Datapack
@app.callback(
    Output("dropdown-indicateurs", "options"),
    Output("dropdown-indicateurs", "value"),
    Input("dropdown-datapack", "value")
)
def update_indicateurs(name_datapack):
    if name_datapack in indicateurs_par_datapack:
        indicateurs = indicateurs_par_datapack[name_datapack]
        return [{"label": ind, "value": ind} for ind in indicateurs], indicateurs
    return [], []  # Si aucun datapack sélectionné, liste vide

if __name__ == "__main__":
    app.run_server(debug=True)
