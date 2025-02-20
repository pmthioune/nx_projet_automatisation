from dash import Input, Output, State, dcc
import pandas as pd


def register_download_callbacks(app):
    @app.callback(
        Output("download-report", "data"),
        Input("download-report", "n_clicks"),
        State("data-quality-table", "data"),
        prevent_initial_call=True
    )
    def download_report(n_clicks, table_data):
        df = pd.DataFrame(table_data)
        return dcc.send_data_frame(df.to_csv, "data_quality_report.csv")
