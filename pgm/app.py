import plotly.graph_objects as go
import plotly.express as px

# 📌 Palette de couleurs dynamiques
COLOR_PALETTE = px.colors.qualitative.Set1

# 📌 Création de l'histogramme avec années sur l'axe des abscisses
fig_histogram = go.Figure()

for idx, name in enumerate(selected_files):
    df = DATASETS[name]

    fig_histogram.add_trace(go.Bar(  # 📌 Utilisation de go.Bar pour une meilleure lisibilité
        x=df["Année"],  # 📌 Affichage des années sur l'axe X
        y=df["Valeur"],
        name=name,
        marker=dict(
            color=COLOR_PALETTE[idx % len(COLOR_PALETTE)],  # 📌 Couleur selon la position
            line=dict(width=0.5)
        ),
        opacity=0.8
    ))

# 📌 Mise en page pour améliorer l'affichage des années
fig_histogram.update_layout(
    title="Comparaison des valeurs par année",
    barmode="group",  # 📌 Affichage côte à côte
    bargap=0.2,  # 📌 Petit espace entre les barres
    xaxis=dict(
        title="Années",
        tickmode="linear",  # 📌 Affichage des années sans saut
        tickangle=-45,  # 📌 Rotation des années pour lisibilité
    ),
    yaxis=dict(title="Valeurs"),
)
