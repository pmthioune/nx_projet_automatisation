from dash import html, dcc

sidebar = html.Div([
    html.H2("Menu", style={"textAlign": "center"}),
    html.Hr(),
    dcc.Link("🏠 Accueil", href="/", className="sidebar-link"),
    dcc.Link("📊 Datapacks", href="/datapacks", className="sidebar-link"),
    dcc.Link("🔍 Data Quality", href="/data_quality", className="sidebar-link"),
    dcc.Link("📈 Gap Analysis", href="/gap_analysis", className="sidebar-link"),
], className="sidebar")
