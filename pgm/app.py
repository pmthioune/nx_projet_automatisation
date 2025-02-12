import os
import dash
from dash import dcc, html, Input, Output, ctx
import dash_bootstrap_components as dbc
from threading import Thread
from dash.dash import no_update
import pandas as pd
from main import start_process, get_progress
from assets import accueil_ui, datapacks_ui, data_quality_ui, download_ui, gap_analysis_ui

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css"])
app.config.suppress_callback_exceptions = True

OUTPUT_DIR = '../../output'
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

sidebar = html.Div(
    [
        html.H2("Menu", style={"text-align": "center", "margin-top": "20px", "color": "white"}),
        dbc.Nav(
            [
                dbc.NavLink([html.I(className="fas fa-home"), " Accueil"], href="/accueil", id="accueil-link", style={"color": "white"}),
                dbc.NavLink([html.I(className="fas fa-database"), " Datapacks"], href="/datapacks", id="datapacks-link", style={"color": "white"}),
                dbc.NavLink([html.I(className="fas fa-chart-bar"), " Data Quality"], href="/dataquality", id="dataquality-link", style={"color": "white"}),
                dbc.NavLink([html.I(className="fas fa-chart-pie"), " Gap Analysis"], href="/gapanalysis", id="gapanalysis-link", style={"color": "white"}),
                dbc.NavLink([html.I(className="fas fa-download"), " Téléchargement"], href="/telechargement", id="telechargement-link", style={"color": "white"}),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style={
        "position": "fixed",
        "top": "0",
        "left": "0",
        "bottom": "0",
        "width": "250px",
        "background-color": "black",
        "padding": "20px",
        "color": "white",
    },
)

main_content = html.Div(
    [
        html.H1("Titrisation", style={"background-color": "red", "color": "white", "padding": "10px"}),
        html.Div(id="tab-content", style={"padding": "20px"}),
        dcc.Interval(id="interval", interval=1000, n_intervals=0, disabled=True),
    ],
    style={"margin-left": "250px", "padding": "20px"},
)

app.layout = html.Div([sidebar, main_content, dcc.Location(id='url', refresh=False)])

@app.callback(
    Output("tab-content", "children"),
    Input("url", "pathname"),
)
def display_content(pathname):
    if pathname == "/accueil":
        return accueil_ui.layout
    elif pathname == "/datapacks":
        return datapacks_ui.layout
    elif pathname == "/dataquality":
        return data_quality_ui.layout
    elif pathname == "/gapanalysis":
        return gap_analysis_ui.layout
    elif pathname == "/telechargement":
        return download_ui.layout
    return accueil_ui.layout

@app.callback(
    [Output("progress-bar-datapack", "value"),
     Output("log-output-datapack", "children"),
     Output("download-section", "children"),
     Output("df-preview", "children"),
     Output("interval-datapack", "disabled")],
    [Input("btn-start-datapack", "n_clicks"),
     Input("interval-datapack", "n_intervals"),
     Input("file-format", "value")]
)
def update_progress(n_clicks, n_intervals, file_format):
    trigger_id = ctx.triggered_id

    if trigger_id == "btn-start-datapack":
        thread = Thread(target=start_process)
        thread.start()
        return 0, "🚀 Traitement en cours...", "", "", False

    elif trigger_id == "interval-datapack":
        progress_state = get_progress()
        progress = progress_state["progress"]
        message = progress_state["message"]

        if progress == 100:
            output_file_path = os.path.join(OUTPUT_DIR, f'output_file.{file_format}')
            with open(output_file_path, 'w') as f:
                f.write("Dummy output content")

            try:
                if file_format == 'csv':
                    df = pd.read_csv(output_file_path)
                elif file_format == 'xlsx':
                    df = pd.read_excel(output_file_path)
                else:
                    df = None

                preview = html.Div([
                    html.H5(f"Aperçu du fichier généré : {output_file_path}", style={"color": "blue"}),
                    html.Div([
                        html.P(f"Lignes 1-5 :"),
                        html.Table(
                            children=[
                                html.Tr([html.Th(col) for col in df.columns])
                            ] +
                            [html.Tr([html.Td(df.iloc[i][col]) for i in range(min(5, len(df)))]) for col in df.columns]
                        ),
                    ])
                ])
            except Exception as e:
                preview = html.P(f"Erreur lors de l'aperçu du fichier : {str(e)}", style={"color": "red"})

            return progress, message, html.A(f"Télécharger le fichier ({file_format.upper()})",
                                             href=f"/download/{output_file_path}",
                                             download=f"output_file.{file_format}"), preview, True

        return progress, message, "", "", False

    return no_update, no_update, no_update, no_update, no_update

if __name__ == "__main__":
    app.run_server(debug=True)