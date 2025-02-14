from dash import html, dcc
import dash_bootstrap_components as dbc

datapacks_content = html.Div(
    children=[
        html.H3("Datapacks", style={"color": "#FF5733", "margin-bottom": "20px"}),
        html.Button(
            "Lancer le traitement",
            id="btn-start-datapack",
            style={
                "background-color": "#333",
                "color": "white",
                "padding": "10px 20px",
                "border": "none",
                "border-radius": "5px",
                "cursor": "pointer",
                "margin-top": "20px"
            }
        ),
        dbc.Progress(
            id="progress-bar-datapack",
            value=0,
            max=100,
            striped=True,
            animated=True,
            style={"margin-top": "20px", "height": "20px"}
        ),
        html.Div(
            id="log-output-datapack",
            style={
                "margin-top": "20px",
                "padding": "10px",
                "background-color": "#f0f0f0",
                "border-radius": "5px",
                "border": "1px solid #ddd",
                "max-height": "200px",
                "overflow-y": "auto",
                "font-family": "monospace",
                "font-size": "14px",
                "color": "#333"
            }
        ),
        html.Div(
            id="download-section",
            children=[
                html.Button(
                    "Téléchargement du datapack",
                    id="btn-download-datapack",
                    style={
                        "background-color": "#28a745",
                        "color": "white",
                        "padding": "10px 20px",
                        "border": "none",
                        "border-radius": "5px",
                        "cursor": "pointer",
                        "margin-top": "20px",
                        "display": "none"
                    }
                ),
                html.A(
                    id="download-link",
                    href="",
                    download="datapack.xlsx",
                    style={"display": "none"}
                )
            ],
            style={"margin-top": "20px"}
        ),
        dcc.Interval(id="interval-datapack", interval=1000, n_intervals=0, disabled=True),
    ],
    style={
        "padding": "20px",
        "background-color": "#f9f9f9",
        "border-radius": "8px",
        "border": "1px solid #ddd"
    }
)