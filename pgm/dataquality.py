from pyspark.sql import DataFrame
from pyspark.sql import functions as F


class DataQuality:
    def __init__(self, data: DataFrame):
        self.data = data
        self.dq_report = {}

    def check_duplicates(self):
        print("Checking for duplicates in the DataFrame...")
        duplicates_df = self.data.groupBy(self.data.columns).count().filter("count > 1")
        if duplicates_df.count() > 0:
            print("Duplicates found.")
            self.dq_report["duplicates"] = duplicates_df
        else:
            print("No duplicates detected.")
        return duplicates_df

    def check_missing_values(self, columns_to_check):
        """
        Calcule le pourcentage de valeurs manquantes pour les colonnes spécifiées.

        Paramètres:
        columns_to_check (list): Liste des noms de colonnes à vérifier pour les valeurs manquantes.

        Retourne:
        dict: Pourcentage de valeurs manquantes pour chaque colonne spécifiée.
        """
        # Calculer le total des valeurs non nulles pour chaque colonne spécifiée en une seule opération
        non_null_counts = self.data.select([
            F.sum(F.when(F.col(column).isNotNull(), 1).otherwise(0)).alias(column)
            for column in columns_to_check
        ])

        # Obtenir le nombre total de lignes dans le DataFrame
        total_count = self.data.count()

        # Calculer le pourcentage de valeurs manquantes pour chaque colonne
        missing_values_rate = {
            column: (1 - non_null_counts.collect()[0][column] / total_count) * 100
            for column in columns_to_check
        }

        # Enregistrer dans dq_report
        self.dq_report["missing_values_rate"] = missing_values_rate

        # Afficher les résultats
        print("Percentage of missing values in selected columns:")
        print(missing_values_rate)

        return missing_values_rate
