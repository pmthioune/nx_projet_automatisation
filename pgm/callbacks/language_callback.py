from dash import Input, Output, State

LANGUAGES = {
    "fr": "Français",
    "en": "English"
}


def register_language_callbacks(app):
    @app.callback(
        [Output('language-store', 'data'),
         Output('language-toggle', 'children')],
        Input('language-toggle', 'n_clicks'),
        State('language-store', 'data')
    )
    def toggle_language(n_clicks, current_language):
        if n_clicks is None:
            return current_language, LANGUAGES[current_language]
        new_language = "en" if current_language == "fr" else "fr"
        return new_language, LANGUAGES[new_language]
