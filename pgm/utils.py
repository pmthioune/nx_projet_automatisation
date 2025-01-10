import os
import pandas as pd


def load_named_ranges_from_csv(folder_path, period=None):
    """
    Charge les fichiers CSV dont les noms commencent par 'ind' et ajoute la période aux clés du dictionnaire si spécifiée.

    Args:
        folder_path (str): Chemin du dossier contenant les fichiers CSV.
        period (str, optional): Période à inclure dans les noms des clés du dictionnaire (exemple : '2024', 'Q1'). Par défaut, None.

    Returns:
        dict: Dictionnaire où les clés sont les noms des plages nommées (avec ou sans période) et les valeurs sont des DataFrames.
    """
    named_ranges_dict = {}

    # Parcourir les fichiers CSV dans le dossier
    for file_name in os.listdir(folder_path):
        # Vérifier si le fichier commence par "ind" et a l'extension ".csv"
        if file_name.startswith("ind") and file_name.endswith(".csv"):
            # Nom de la clé sans extension
            base_key = os.path.splitext(file_name)[0]

            # Ajouter la période au nom de la clé si spécifiée
            if period:
                key = f"{base_key}_{period}"
            else:
                key = base_key

            # Charger le fichier CSV en DataFrame
            file_path = os.path.join(folder_path, file_name)
            df = pd.read_csv(file_path)

            # Ajouter au dictionnaire
            named_ranges_dict[key] = df

    return named_ranges_dict
