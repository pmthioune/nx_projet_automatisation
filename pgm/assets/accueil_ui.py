from dash import html

def get_accueil_content(language):
    if language == "fr":
        return html.Div(
            children=[
                html.H3("Bienvenue sur l'outil de Titrisation", style={"color": "#FF5733", "margin-bottom": "20px"}),
                html.P(
                    """
                    Cette application vous permet de gérer et de suivre la construction des datapacks de la titrisation.
                    Voici un guide pour prendre en main l'outil :
                    """,
                    style={"font-size": "18px", "margin-top": "20px", "line-height": "1.6"}
                ),
                html.Ul(
                    children=[
                        html.Li(
                            """
                            1. Allez dans la section 'Datapacks' pour configurer et construire le datapack.
                            Une fois la configuration terminée, appuyez sur le bouton 'Lancer le traitement' pour générer
                            le datapack. Suivez la progression du traitement avec la barre de progression en bas de la page.
                            Une fois le traitement terminé, vous recevrez un message de confirmation.
                            """,
                            style={"font-size": "16px", "margin-bottom": "10px"}
                        ),
                        html.Li(
                            "2. Utilisez la section 'Data Quality' pour évaluer et produire le rapport de la qualité des données.",
                            style={"font-size": "16px", "margin-bottom": "10px"}
                        ),
                        html.Li(
                            "3. Consultez la section 'Gap Analysis' pour analyser les écarts.",
                            style={"font-size": "16px", "margin-bottom": "10px"}
                        ),
                    ],
                    style={"list-style-type": "disc", "padding-left": "40px", "color": "#333"}
                ),
                html.P(
                    "Configurez et téléchargez vos fichiers selon le format approprié.",
                    style={"font-size": "18px", "margin-top": "20px", "font-weight": "bold"}
                ),
            ],
            style={"padding": "20px", "background-color": "#f9f9f9", "border-radius": "8px"}
        )
    else:
        return html.Div(
            children=[
                html.H3("Welcome to the Titrisation Tool", style={"color": "#FF5733", "margin-bottom": "20px"}),
                html.P(
                    """
                    This application allows you to manage and track the construction of securitization datapacks.
                    Here is a guide to get started:
                    """,
                    style={"font-size": "18px", "margin-top": "20px", "line-height": "1.6"}
                ),
                html.Ul(
                    children=[
                        html.Li(
                            """
                            1. Go to the 'Datapacks' section to configure and build the datapack.
                            Once the configuration is complete, click the 'Start Processing' button to generate
                            the datapack. Track the progress of the process with the progress bar at the bottom of the page.
                            Once the process is complete, you will receive a confirmation message.
                            """,
                            style={"font-size": "16px", "margin-bottom": "10px"}
                        ),
                        html.Li(
                            "2. Use the 'Data Quality' section to evaluate and produce the data quality report.",
                            style={"font-size": "16px", "margin-bottom": "10px"}
                        ),
                        html.Li(
                            "3. Check the 'Gap Analysis' section to analyze gaps.",
                            style={"font-size": "16px", "margin-bottom": "10px"}
                        ),
                    ],
                    style={"list-style-type": "disc", "padding-left": "40px", "color": "#333"}
                ),
                html.P(
                    "Configure and download your files in the appropriate format.",
                    style={"font-size": "18px", "margin-top": "20px", "font-weight": "bold"}
                ),
            ],
            style={"padding": "20px", "background-color": "#f9f9f9", "border-radius": "8px"}
        )