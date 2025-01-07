import os
import pandas as pd
from openpyxl import load_workbook


def update_excel_named_ranges_and_save_copy(excel_file, named_ranges_dict, output_folder):
    """
    Met à jour les plages nommées dans un fichier Excel avec des données issues de DataFrames,
    puis enregistre une copie dans un dossier de sortie sous un nouveau nom.

    Args:
        excel_file (str): Chemin du fichier Excel existant.
        named_ranges_dict (dict): Dictionnaire où les clés sont les noms des plages et les valeurs sont des DataFrames.
        output_folder (str): Dossier où enregistrer le fichier mis à jour.
    """
    try:
        # Charger le fichier Excel
        workbook = load_workbook(excel_file)
    except FileNotFoundError:
        raise FileNotFoundError(f"Le fichier '{excel_file}' n'existe pas.")

    for named_range, df in named_ranges_dict.items():
        # Vérifier si la plage nommée existe
        if named_range not in workbook.defined_names:
            print(f"La plage nommée '{named_range}' n'existe pas dans le fichier Excel.")
            continue

        # Obtenir la feuille et la plage associées
        destination = workbook.defined_names[named_range].destinations  # Liste des destinations
        for sheet_name, cell_range in destination:
            sheet = workbook[sheet_name]

            # Obtenir les coordonnées de la plage nommée
            start_cell = sheet[cell_range.split(":")[0]]
            start_row = start_cell.row
            start_col = start_cell.column

            # Écrire les données du DataFrame dans la plage
            for row_idx, row in enumerate(df.itertuples(index=False), start=start_row):
                for col_idx, value in enumerate(row, start=start_col):
                    sheet.cell(row=row_idx, column=col_idx, value=value)

    # Générer le chemin de sortie
    os.makedirs(output_folder, exist_ok=True)  # Créer le dossier s'il n'existe pas
    output_file = os.path.join(output_folder, "Projet_Data_Pack.xlsx")

    # Sauvegarder le fichier mis à jour sous un nouveau nom
    workbook.save(output_file)
    print(f"Fichier mis à jour enregistré dans : {output_file}")


# Exemple de DataFrames
df1 = pd.DataFrame({
    "Rating": ["A", "B", "C"],
    "Default Rate (%)": [1.5, 2.0, 2.5]
})

df2 = pd.DataFrame({
    "Year": [2021, 2022, 2023],
    "Default Rate (%)": [1.8, 2.1, 2.3]
})

# Dictionnaire des plages nommées et DataFrames correspondants
named_ranges_dict = {
    "indicator_1": df1,
    "indicator_2": df2
}

# Chemin vers le fichier Excel existant
input_excel_file = "modele_indicateurs.xlsx"

# Dossier de sortie
output_folder = "output_folder"

# Appeler la fonction pour mettre à jour les plages nommées et sauvegarder une copie
update_excel_named_ranges_and_save_copy(input_excel_file, named_ranges_dict, output_folder)
