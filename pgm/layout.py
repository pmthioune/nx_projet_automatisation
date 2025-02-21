from dash import html, dcc
import dash_bootstrap_components as dbc

def create_layout():
    # Sidebar
    sidebar = html.Div(
        [
            html.H2("Menu", style={"text-align": "center", "margin-top": "20px", "color": "white"}),
            dbc.Nav(
                [
                    dbc.NavLink(
                        [html.I(className="fas fa-home", style={"margin-right": "10px"}), "Accueil"],
                        href="/accueil",
                        id="accueil-link",
                        style={"color": "white", "padding": "10px", "border-radius": "5px"}
                    ),
                    dbc.NavLink(
                        [html.I(className="fas fa-database", style={"margin-right": "10px"}), "Datapacks"],
                        href="/datapacks",
                        id="datapacks-link",
                        style={"color": "white", "padding": "10px", "border-radius": "5px"}
                    ),
                    dbc.NavLink(
                        [html.I(className="fas fa-chart-line", style={"margin-right": "10px"}), "Data Quality"],
                        href="/dataquality",
                        id="dataquality-link",
                        style={"color": "white", "padding": "10px", "border-radius": "5px"}
                    ),
                    dbc.NavLink(
                        [html.I(className="fas fa-search", style={"margin-right": "10px"}), "Gap Analysis"],
                        href="/gapanalysis",
                        id="gapanalysis-link",
                        style={"color": "white", "padding": "10px", "border-radius": "5px"}
                    ),
                    dbc.NavLink(
                        [html.I(className="fas fa-download", style={"margin-right": "10px"}), "Téléchargement"],
                        href="/download",
                        id="download-link",
                        style={"color": "white", "padding": "10px", "border-radius": "5px"}
                    ),
                ],
                vertical=True,
                pills=True,
                style={"margin-top": "20px"}
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
            "box-shadow": "2px 0 5px rgba(0, 0, 0, 0.1)"
        },
    )

    # Language Toggle Button
    language_toggle = html.Div([
        dbc.Button(
            id="language-toggle",
            children="Français",
            color="danger",  # Using red color for the button
            style={"position": "absolute", "top": "10px", "right": "10px", "border-radius": "5px"}
        )
    ])

    # Main Content
    main_content = html.Div(
        [
            html.H1(
                "Titrisation",
                style={
                    "background-color": "red",
                    "color": "white",
                    "padding": "15px",
                    "margin-bottom": "20px",
                    "border-radius": "5px",
                    "box-shadow": "0 2px 5px rgba(0, 0, 0, 0.1)"
                }
            ),
            language_toggle,
            html.Div(
                id="tab-content",
                style={"padding": "20px", "background-color": "#f8f9fa", "border-radius": "5px", "box-shadow": "0 2px 5px rgba(0, 0, 0, 0.1)"}
            ),
            dcc.Interval(id="interval", interval=1000, n_intervals=0, disabled=True),
        ],
        style={"margin-left": "250px", "padding": "20px"},
    )

    # Main Layout
    return html.Div(
        [
            html.Link(
                rel="stylesheet",
                href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css"
            ),
            sidebar,
            main_content,
            dcc.Location(id='url', refresh=False),
            dcc.Store(id='language-store', data='fr'),
        ],
        style={"font-family": "Arial, sans-serif"}
    )