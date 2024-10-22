import os
from pyspark.sql import DataFrame, SparkSession
from datetime import datetime


class Datapack:
    """
    Classe simplifiée Datapack qui contient une méthode principale `generate_folder()`.
    Cette méthode crée un dossier et y génère les fichiers du datapack et les rapports d'analyse de gap.

    Attributs :
    - id_datapack : Identifiant unique du datapack.
    - name : Nom du datapack (RACER, JUNON, Colisée, Mercure, etc.).
    - indicators : Dictionnaire des indicateurs (PD, LGD, etc.).
    - creation_date : Date de création du datapack.
    - gap_analysis_results : Résultats de l'analyse de gap entre N et N-1.
    - output_folder : Dossier où les fichiers seront générés.

    Méthodes :
    - generate_folder() : Crée le dossier de sortie et y écrit les indicateurs et les résultats de gap analysis.
    """

    def __init__(self, id_datapack: int, name: str, output_folder: str):
        """
        Initialise la classe avec un identifiant unique, un nom de datapack et un dossier de sortie.
        :param id_datapack: Identifiant unique du datapack.
        :param name: Nom du datapack.
        :param output_folder: Dossier où seront stockés les fichiers générés.
        """
        self.id_datapack = id_datapack
        self.name = name
        self.indicators = {}
        self.creation_date = datetime.now().strftime("%Y-%m-%d")
        self.gap_analysis_results = {}
        self.output_folder = output_folder

    def add_indicator(self, indicator_name: str, indicator_data: DataFrame):
        """
        Ajoute un indicateur (comme PD ou LGD) au datapack.
        :param indicator_name: Nom de l'indicateur (PD, LGD, etc.).
        :param indicator_data: Données associées à l'indicateur (DataFrame Spark).
        """
        self.indicators[indicator_name] = indicator_data

    def perform_gap_analysis(self, n_data: DataFrame, n_minus_1_data: DataFrame):
        """
        Réalise une analyse de gap entre les périodes N et N-1 pour chaque indicateur.
        :param n_data: Données pour la période N.
        :param n_minus_1_data: Données pour la période N-1.
        :return: Résultats de l'analyse de gap pour chaque indicateur.
        """
        for indicator_name, data_n in self.indicators.items():
            data_n_minus_1 = n_minus_1_data[indicator_name]

            # Exemple de calcul de gap entre N et N-1
            gap = data_n.join(data_n_minus_1, on="category", how="outer") \
                .withColumn("gap", data_n["value"] - data_n_minus_1["value"])

            self.gap_analysis_results[indicator_name] = gap
        return self.gap_analysis_results

    def generate_folder(self):
        """
        Crée un dossier de sortie pour le datapack, enregistre les indicateurs et les résultats d'analyse de gap.
        :return: Chemin du dossier généré.
        """
        folder_path = os.path.join(self.output_folder, f"datapack_{self.name}_{self.creation_date}")

        # Créer le dossier de sortie
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        # Sauvegarder les indicateurs
        for indicator_name, data in self.indicators.items():
            indicator_file_path = os.path.join(folder_path, f"{indicator_name}.csv")
            data.write.csv(indicator_file_path)

        # Sauvegarder les résultats de l'analyse de gap
        for indicator_name, gap_result in self.gap_analysis_results.items():
            gap_file_path = os.path.join(folder_path, f"gap_analysis_{indicator_name}.csv")
            gap_result.write.csv(gap_file_path)

        return folder_path
