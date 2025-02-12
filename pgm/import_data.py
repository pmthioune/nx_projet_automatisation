import pandas as pd
import os

class data_loader:
    def __init__(self, directory_path):
        self.directory_path = directory_path
        self.data_frame = None
        self.excel_file = None

    def find_file(self):
        # Liste tous les fichiers dans le répertoire et trouve le premier fichier Excel ou CSV
        for filename in os.listdir(self.directory_path):
            if filename.endswith(('.csv', '.xls', '.xlsx')):
                self.excel_file = os.path.join(self.directory_path, filename)
                print(f"Fichier trouvé : {self.excel_file}")
                return True
        print("Aucun fichier Excel ou CSV trouvé dans le répertoire spécifié.")
        return False

    def load_data(self):
        if self.find_file():
            try:
                # Vérifie l'extension du fichier pour charger correctement
                if self.excel_file.endswith('.csv'):
                    # Utilisation de read_csv pour les fichiers CSV
                    self.data_frame = pd.read_csv(self.excel_file)
                    print(f"Fichier CSV chargé avec succès depuis {self.excel_file}")
                else:
                    # Utilisation de read_excel pour les fichiers Excel
                    self.data_frame = pd.read_excel(self.excel_file)
                    print(f"Fichier Excel chargé avec succès depuis {self.excel_file}")
            except Exception as e:
                print(f"Erreur lors du chargement des données depuis {self.excel_file}: {e}")
        else:
            print("Les données n'ont pas pu être chargées car aucun fichier n'a été trouvé.")

    def get_data(self):
        if self.data_frame is not None:
            return self.data_frame
        else:
            print("Aucune donnée chargée. Veuillez charger les données d'abord avec la méthode 'load_data'.")
            return None

    def show_info(self):
        if self.data_frame is not None:
            print(self.data_frame.info())
        else:
            print("Aucune donnée chargée. Veuillez charger les données d'abord avec la méthode 'load_data'.")

    def preview_data(self, n=5):
        if self.data_frame is not None:
            return self.data_frame.head(n)
        else:
            print("Aucune donnée chargée. Veuillez charger les données d'abord avec la méthode 'load_data'.")
            return None


