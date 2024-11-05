from pyspark.sql import functions as F
from pyspark.sql import DataFrame


class DataQuality:
    def __init__(self, data: DataFrame):
        self.data = data

    def check_and_calculate_outliers(self, threshold_dict):
        """
        Identifie les outliers dans les colonnes spécifiées en fonction des seuils et
        calcule le taux d'outliers pour chaque colonne.

        Paramètres:
        threshold_dict (dict): Dictionnaire contenant les limites d'outliers par colonne.

        Retourne:
        tuple:
            - dict contenant les taux d'outliers par colonne en pourcentage.
            - DataFrame des lignes contenant des valeurs outliers.
        """
        outlier_rates = {}
        total_rows = self.data.count()

        # Commence avec un DataFrame vide pour accumuler les outliers
        outliers_df = self.data.filter(F.lit(False))

        for column, limits in threshold_dict.items():
            # Initialiser la condition d'outlier pour la colonne
            column_condition = F.lit(False)

            # Ajouter une condition seulement si la limite existe
            if limits.get("min") is not None:
                column_condition |= (F.col(column) < limits["min"])
            if limits.get("max") is not None:
                column_condition |= (F.col(column) > limits["max"])

            # Filtrer les valeurs d'outliers pour la colonne
            column_outliers_df = self.data.filter(column_condition)
            outliers_df = outliers_df.union(column_outliers_df)

            # Calculer le taux d'outliers
            outlier_count = column_outliers_df.count()
            outlier_rate = (outlier_count / total_rows) * 100
            outlier_rates[column] = outlier_rate

            print(f"Taux d'outliers pour {column}: {outlier_rate:.2f}%")

        return outlier_rates, outliers_df
