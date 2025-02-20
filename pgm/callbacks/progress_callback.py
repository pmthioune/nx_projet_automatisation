from dash import Input, Output, State, ctx, no_update
import threading
from pgm.main import start_process, get_progress


def register_progress_callbacks(app):
    @app.callback(
        [Output("progress-bar-datapack", "value"),
         Output("log-output-datapack", "children"),
         Output("btn-download-datapack", "style"),
         Output("download-link", "href"),
         Output("interval-datapack", "disabled")],
        [Input("btn-start-datapack", "n_clicks"),
         Input("interval-datapack", "n_intervals")]
    )
    def update_progress(n_clicks, n_intervals):
        triggered_id = ctx.triggered_id

        if triggered_id == "btn-start-datapack":
            # Démarrer le processus dans un thread séparé
            thread = threading.Thread(target=start_process)
            thread.start()

            # Initialement, afficher le statut de traitement
            return 0, "🚀 Traitement en cours...", {"display": "none"}, "", False

        elif triggered_id == "interval-datapack":
            # Simuler la progression à des fins de démonstration
            progress_state = get_progress()  # Cela devrait appeler votre fonction de suivi de progression réelle
            progress = progress_state["progress"]
            message = progress_state["message"]

            if progress == 100:
                # Afficher le bouton de téléchargement lorsque terminé
                return (
                    progress,
                    message,
                    {"display": "block", "background-color": "#28a745", "color": "white", "padding": "10px 20px",
                     "border": "none", "border-radius": "5px", "cursor": "pointer", "margin-top": "20px"},
                    f"/download/",
                    True
                )

            return progress, message, {"display": "none"}, "", False

        return no_update, no_update, no_update, no_update, no_update
