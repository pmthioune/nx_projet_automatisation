from dash import Input, Output, State, ctx, no_update

from pgm.callbacks.data_quality_callback import register_data_quality_callbacks
from pgm.callbacks.language_callback import register_language_callbacks
from pgm.callbacks.progress_callback import register_progress_callbacks
from pgm.callbacks.gap_analysis_callback import register_gap_analysis_callbacks


def register_callbacks(app):
    @app.callback(Output("tab-content", "children"),
                  Input("url", "pathname"), State('language-store', 'data'))
    def display_content(pathname, language):
        from pgm.assets.accueil_ui import get_accueil_content
        from pgm.assets.datapacks_ui import datapacks_content
        from pgm.assets.data_quality_ui import data_quality_content
        from pgm.assets.gap_analysis_ui import gap_analysis_content
        from pgm.assets.download_ui import download_content

        if pathname == "/accueil":
            return get_accueil_content(language)
        elif pathname == "/datapacks":
            return datapacks_content
        elif pathname == "/dataquality":
            return data_quality_content
        elif pathname == "/gapanalysis":
            return gap_analysis_content
        elif pathname == "/download":
            return download_content
        return get_accueil_content(language)

    register_data_quality_callbacks(app)
    register_language_callbacks(app)
    register_progress_callbacks(app)
