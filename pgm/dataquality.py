from pyspark.sql import DataFrame
from pyspark.sql.functions import col, countDistinct, year


class DataQuality:
    def __init__(self):
        pass

    @staticmethod
    def calculate_facilities_by_default_year(
            df: DataFrame,
            default_date_col: str,
            entity_col: str,
            facility_col: str
    ) -> DataFrame:
        """
        Calcule le nombre de facilities distincts par année de défaut et par entité.

        Args:
            df (DataFrame): Le DataFrame Spark contenant les données.
            default_date_col (str): Colonne contenant la date de défaut.
            entity_col (str): Colonne contenant les entités.
            facility_col (str): Colonne contenant les facilities.

        Returns:
            DataFrame: Résultat des statistiques.
        """
        # Extraire l'année de défaut
        df = df.withColumn("default_year", year(col(default_date_col)))

        # Calculer le nombre de facilities distincts par année de défaut et entité
        stats_df = (
            df.groupBy("default_year", entity_col)
            .agg(countDistinct(col(facility_col)).alias("distinct_facilities"))
            .orderBy("default_year", entity_col)
        )

        return stats_df
