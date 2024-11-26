from pyspark.sql import DataFrame
from pyspark.sql.functions import col, avg, stddev, min, max, count, expr


class DataQuality:
    def __init__(self):
        pass

    @staticmethod
    def descriptive_stats_on_ratings(df: DataFrame, rating_col: str) -> DataFrame:
        """
        Effectue des statistiques descriptives sur une colonne de notation.

        Args:
            df (DataFrame): Le DataFrame Spark contenant les données.
            rating_col (str): La colonne contenant les notations à analyser.

        Returns:
            DataFrame: Résumé des statistiques descriptives.
        """
        # Vérifier si la colonne existe
        if rating_col not in df.columns:
            raise ValueError(f"La colonne '{rating_col}' n'existe pas dans le DataFrame.")

        # Calcul des métriques descriptives
        stats_df = df.select(
            count(col(rating_col)).alias("count"),
            count(expr(f"CASE WHEN {rating_col} IS NULL THEN 1 END")).alias("missing_values"),
            avg(col(rating_col)).alias("mean"),
            stddev(col(rating_col)).alias("stddev"),
            min(col(rating_col)).alias("min"),
            max(col(rating_col)).alias("max"),
        )

        return stats_df
