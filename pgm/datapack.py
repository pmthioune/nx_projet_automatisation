from dash import html, dcc, Input, Output, dash_table
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objects as go
import numpy as np
from app import app

# 📌 Création de bases de données fictives
np.random.seed(42)
df1 = pd.DataFrame({"Index": np.arange(100), "Valeur": np.random.normal(50, 10, 100)})
df2 = pd.DataFrame({"Index": np.arange(100), "Valeur": np.random.normal(55, 15, 100)})
df3 = pd.DataFrame({"Index": np.arange(100), "Valeur": np.random.normal(60, 20, 100)})

DATASETS = {
    "Base A": df1,
    "Base B": df2,
    "Base C": df3
}

# 📌 Définition des couleurs associées à chaque base
COLORS = {
    "Base A": "blue",
    "Base B": "green",
    "Base C": "red"
}

# 📌 Layout de l'onglet Datapacks
datapacks_layout = html.Div([
    html.H1("📊 Comparaison des Datapacks"),

    # Sélection multiple des bases
    dcc.Dropdown(
        id="file-dropdown",
        options=[{"label": name, "value": name} for name in DATASETS.keys()],
        multi=True,
        placeholder="Sélectionnez les bases à comparer",
        style={"width": "60%"}
    ),

    # Graphiques
    dcc.Graph(id="histogram-graph"),
    dcc.Graph(id="line-graph"),
    dcc.Graph(id="gap-graph"),

    # Tableau des écarts
    dash_table.DataTable(
        id="gap-table",
        columns=[
            {"name": "Base", "id": "Base"},
            {"name": "Moyenne", "id": "Moyenne"},
            {"name": "Écart-Type", "id": "Écart-Type"},
            {"name": "Valeur Min", "id": "Valeur Min"},
            {"name": "Valeur Max", "id": "Valeur Max"}
        ],
        style_table={"overflowX": "auto"}
    )
])

# 📌 Mise à jour des graphiques et du tableau
@app.callback(
    [Output("histogram-graph", "figure"),
     Output("line-graph", "figure"),
     Output("gap-graph", "figure"),
     Output("gap-table", "data")],
    Input("file-dropdown", "value")
)
def update_graphs(selected_files):
    if not selected_files:
        return {}, {}, {}, []

    fig_histogram = go.Figure()
    fig_line = go.Figure()
    gap_data = []

    for name in selected_files:
        df = DATASETS[name]

        # Ajout des histogrammes avec des couleurs différentes
        fig_histogram.add_trace(go.Histogram(
            x=df["Valeur"],
            name=name,
            marker_color=COLORS.get(name, "black"),  # Couleur spécifique à la base
            opacity=0.75
        ))

        # Ajout des courbes
        fig_line.add_trace(go.Scatter(
            x=df["Index"],
            y=df["Valeur"],
            mode="lines",
            name=name,
            line=dict(color=COLORS.get(name, "black"))
        ))

        # Stats pour le tableau des écarts
        gap_data.append({
            "Base": name,
            "Moyenne": round(df["Valeur"].mean(), 2),
            "Écart-Type": round(df["Valeur"].std(), 2),
            "Valeur Min": round(df["Valeur"].min(), 2),
            "Valeur Max": round(df["Valeur"].max(), 2)
        })

    # Mise en forme des graphiques
    fig_histogram.update_layout(title="Histogramme des valeurs", barmode='overlay')
    fig_line.update_layout(title="Courbe des valeurs")

    # Calcul des écarts absolus entre la première et la deuxième base
    if len(selected_files) >= 2:
        df1 = DATASETS[selected_files[0]]
        df2 = DATASETS[selected_files[1]]
        df_gap = abs(df1["Valeur"] - df2["Valeur"])

        fig_gap = go.Figure()
        fig_gap.add_trace(go.Scatter(
            x=df1["Index"], y=df_gap,
            mode="lines",
            name=f"Écart entre {selected_files[0]} et {selected_files[1]}",
            line=dict(color="purple")
        ))
        fig_gap.update_layout(title="Écart absolu entre bases")
    else:
        fig_gap = go.Figure()

    return fig_histogram, fig_line, fig_gap, gap_data
