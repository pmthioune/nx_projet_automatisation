from pyspark.sql import SparkSession
import os

class DataLoader:
    def __init__(self, spark: SparkSession):
        self.spark = spark

    def retrieve_dataframes(self, folder_path: str) -> dict:
        """
        Récupère tous les fichiers CSV dans un dossier et retourne un dictionnaire de DataFrames PySpark.

        Args:
            folder_path (str): Chemin du dossier contenant les fichiers CSV.

        Returns:
            dict: Un dictionnaire où les clés sont les noms des fichiers (sans extension)
                  et les valeurs sont les DataFrames Spark correspondants.
        """
        # Vérification si le dossier existe
        if not os.path.exists(folder_path):
            raise FileNotFoundError(f"Le dossier '{folder_path}' n'existe pas.")

        # Filtrer les fichiers CSV dans le dossier
        csv_files = [f for f in os.listdir(folder_path) if f.endswith(".csv")]

        if not csv_files:
            raise ValueError(f"Aucun fichier CSV trouvé dans le dossier '{folder_path}'.")

        # Charger chaque fichier CSV dans un DataFrame séparé
        dataframes = {}
        for file in csv_files:
            file_path = os.path.join(folder_path, file)
            try:
                # Charger le fichier dans un DataFrame Spark
                df = self.spark.read.csv(file_path, header=True, inferSchema=True)
                # Utiliser le nom du fichier sans extension comme clé
                file_name = os.path.splitext(file)[0]
                dataframes[file_name] = df
            except Exception as e:
                raise RuntimeError(f"Erreur lors du chargement du fichier '{file}': {str(e)}")

        return dataframes
