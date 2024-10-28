import os
import datetime
from pyspark.sql import DataFrame
from indicator import Indicator  # Assurez-vous que ce chemin d'import est correct en fonction de votre structure
from dataquality import DataQuality  # Assurez-vous également que l'import est correct

# Classe d'exception personnalisée pour le processus
class ProcessError(Exception):
    def __init__(self, message):
        super().__init__(message)


class Process:
    def __init__(self, name: str, data: DataFrame):
        self.name = name
        self.data = data
        self.data_quality = DataQuality(data)

    def collect_data(self, data_folder: str):
        """
        Collecte les données à partir du dossier spécifié.
        """
        try:
            # Exemple de simulation de collecte de données
            print(f"Collecting data from {data_folder}...")
            # Logique de collecte de données ici
            if not os.path.exists(data_folder):
                raise ProcessError(f"Data folder '{data_folder}' does not exist.")
        except Exception as e:
            raise ProcessError(f"Error during data collection: {str(e)}")

    def process_data(self):
        """
        Applique les traitements nécessaires aux données.
        """
        try:
            print("Processing data...")
            # Ajoutez ici les transformations nécessaires
            # Exemple de traitement
        except Exception as e:
            raise ProcessError(f"Error during data processing: {str(e)}")

    def analyze_data_quality(self):
        """
        Effectue l'analyse de qualité de données en utilisant la classe DataQuality.
        """
        try:
            print("Analyzing data quality...")
            self.data_quality.check_missing_values()
            self.data_quality.detect_duplicates()
            self.data_quality.detect_outliers()
        except Exception as e:
            raise ProcessError(f"Error during data quality analysis: {str(e)}")

    def generate_datapack_folder(self):
        """
        Crée un dossier avec un horodatage pour stocker les datapacks et analyses de gap.
        """
        try:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            folder_name = f"{self.name}_datapack_{timestamp}"
            os.makedirs(folder_name, exist_ok=True)
            print(f"Folder '{folder_name}' created to store datapacks and gap analysis.")
            return folder_name
        except Exception as e:
            raise ProcessError(f"Error creating datapack folder: {str(e)}")

    def generate_gap_analysis(self):
        """
        Génère une analyse de gap entre les périodes N-1 et N.
        """
        try:
            print("Generating gap analysis...")
            # Logique de calcul pour l’analyse de gap
        except Exception as e:
            raise ProcessError(f"Error generating gap analysis: {str(e)}")

    def execute(self, data_folder: str):
        """
        Exécute toutes les étapes du processus en séquence avec gestion des erreurs.
        """
        print(f"Starting process: {self.name}")
        try:
            self.collect_data(data_folder)
            self.process_data()
            self.analyze_data_quality()
            folder = self.generate_datapack_folder()
            self.generate_gap_analysis()
            print(f"Process {self.name} completed successfully.")
        except ProcessError as e:
            print(f"Process failed: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
