import os
import pandas as pd
from openpyxl import load_workbook

def find_excel_file(folder_path: str, keyword="Data Pack") -> str:
    for file in os.listdir(folder_path):
        if keyword in file and file.endswith(".xlsx"):
            return os.path.join(folder_path, file)
    raise FileNotFoundError(f"Aucun fichier Excel contenant '{keyword}' trouvé dans {folder_path}")

def extract_data_from_excel(file_path: str) -> dict:
    wb = load_workbook(file_path, data_only=True)
    data = {}

    # Fonction utilitaire pour extraire une plage dynamique
    def extract_from_sheet(sheet_name, start_col, end_col, start_row):
        sheet = wb[sheet_name]
        rows = []
        row = start_row
        while True:
            row_values = [sheet[f"{col}{row}"].value for col in range_to_col_letters(start_col, end_col)]
            if all(cell is None for cell in row_values):
                break
            rows.append(row_values)
            row += 1
        return pd.DataFrame(rows)

    def range_to_col_letters(start_col, end_col):
        # Convertit 'B' à 'E' en ['B', 'C', 'D', 'E']
        return [chr(i) for i in range(ord(start_col), ord(end_col) + 1)]

    # Extraction depuis Prepayments : B22:E...
    data['Prepayments'] = extract_from_sheet("Prepayments", "B", "E", 22)

    # Extraction depuis Origination Volume : B22:D...
    data['Origination Volume'] = extract_from_sheet("Origination Volume", "B", "D", 22)

    return data

# Exemple d'utilisation
if __name__ == "__main__":
    folder = "chemin/vers/ton/dossier"
    try:
        file = find_excel_file(folder)
        extracted_data = extract_data_from_excel(file)
        print("✅ Données extraites avec succès.")
        print("Prepayments :")
        print(extracted_data["Prepayments"].head())
        print("Origination Volume :")
        print(extracted_data["Origination Volume"].head())
    except Exception as e:
        print(f"❌ Erreur : {e}")
