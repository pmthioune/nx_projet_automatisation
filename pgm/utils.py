import os
import pandas as pd


def load_named_ranges_from_csv(folder_path):
    """
    Charge les fichiers CSV depuis un dossier et les associe aux plages nommées.

    Args:
        folder_path (str): Chemin du dossier contenant les fichiers CSV.

    Returns:
        dict: Dictionnaire où les clés sont les noms des plages nommées et les valeurs sont des DataFrames.
    """
    named_ranges_dict = {}

    # Parcourir les fichiers CSV dans le dossier
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".csv"):
            # Utiliser le nom du fichier (sans extension) comme clé pour la plage nommée
            named_range = os.path.splitext(file_name)[0]

            # Charger le fichier CSV en DataFrame
            file_path = os.path.join(folder_path, file_name)
            df = pd.read_csv(file_path)

            # Ajouter au dictionnaire
            named_ranges_dict[named_range] = df

    return named_ranges_dict
