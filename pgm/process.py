import os
from datetime import datetime


class Process:
    def __init__(self, data_type, period, mapping_file_path, input_folder, output_folder):
        """
        Initialise la classe Process avec le type de données, la période, le fichier de mapping, et les dossiers d'entrée et de sortie.
        :param data_type: Type de données (PD, LGD, etc.).
        :param period: Période d'extraction.
        :param mapping_file_path: Chemin vers le fichier Excel de mapping.
        :param input_folder: Dossier contenant les fichiers de données.
        :param output_folder: Dossier où seront stockés les résultats.
        """
        self.data_type = data_type
        self.period = period
        self.mapping_file_path = mapping_file_path
        self.input_folder = input_folder
        self.output_folder = output_folder
        self.data_instance = None
        self.data_quality_instance = None
        self.indicator_instance = None
        self.datapack_instance = None

    def run_process(self):
        """
        Exécute le processus de bout en bout : collecte, vérification de la qualité, calcul d'indicateurs, et génération du datapack.
        """
        try:
            # 1. Collecte des données
            self.data_instance = Data(self.data_type, self.period, self.mapping_file_path)
            self.data_instance.collect_data(self.input_folder)

            # Vérification si la collecte est réussie
            if self.data_instance.dataframe is None:
                raise ValueError("Aucune donnée collectée. Vérifiez le dossier d'entrée ou le fichier de mapping.")

            # 2. Analyse de la qualité des données
            self.data_quality_instance = DataQuality(self.data_instance.dataframe)
            dq_report = self.data_quality_instance.run_checks()
            print("Rapport de qualité des données :")
            print(dq_report)

            # 3. Calcul des indicateurs
            self.indicator_instance = Indicators(self.data_instance.dataframe)
            indicators_df = self.indicator_instance.calculate_indicators()
            print("Indicateurs calculés :")
            print(indicators_df)

            # 4. Génération du datapack
            timestamp = datetime.now().strftime("%Y%m%d_%H%M")
            datapack_folder = os.path.join(self.output_folder, f"datapack_{self.period}_{timestamp}")
            self.datapack_instance = Datapack(self.period, indicators_df, dq_report)
            self.datapack_instance.generate_folder(datapack_folder)
            print(f"Datapack généré dans le dossier : {datapack_folder}")

        except Exception as e:
            print(f"Erreur lors de l'exécution du processus : {e}")

# Initialisation et exécution du processus
process = Process(
    data_type="PD",
    period="2024-10",
    mapping_file_path="input/mapping.xlsx",
    input_folder="input_folder",
    output_folder="output_folder"
)

process.run_process()
