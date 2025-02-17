import dash
import dash_bootstrap_components as dbc
from pgm.layout import create_layout
from pgm.callbacks import register_callbacks

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.config.suppress_callback_exceptions = True

app.layout = create_layout()

register_callbacks(app)

if __name__ == "__main__":
    app.run_server(debug=True)