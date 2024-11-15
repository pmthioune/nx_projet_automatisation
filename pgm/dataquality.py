# data_processing/data_quality.py
from .exceptions import DataQualityError
from .logger_config import logger
import pandas as pd


class DataQuality:
    def __init__(self, data):
        self.data = data

    def calculate_obligors_stats(self, obligor_column, cohort_column, pole_column):
        """
        Calculate distinct obligors statistics in one pass:
        - Total number of distinct obligors.
        - Number of obligors per cohort.
        - Number of obligors per pole and cohort.

        Args:
            obligor_column (str): Name of the column representing obligor IDs.
            cohort_column (str): Name of the column representing cohorts.
            pole_column (str): Name of the column representing poles.

        Returns:
            dict: A dictionary with calculated stats.
        """
        try:
            logger.info("Starting obligors statistics calculation...")

            # Vérifier les colonnes nécessaires
            required_columns = {obligor_column, cohort_column, pole_column}
            if not required_columns.issubset(self.data.columns):
                missing_columns = required_columns - set(self.data.columns)
                raise DataQualityError(f"Missing required columns: {missing_columns}")

            # Calculer les statistiques en une seule passe
            grouped = self.data.groupby([pole_column, cohort_column])[obligor_column].nunique()

            # Construire les résultats
            total_distinct_obligors = self.data[obligor_column].nunique()
            results = {
                "total_distinct_obligors": total_distinct_obligors,
                "obligors_per_cohort": grouped.groupby(level=1).sum().reset_index(name='distinct_obligors'),
                "obligors_per_pole_cohort": grouped.reset_index(name='distinct_obligors'),
            }

            logger.info(f"Total distinct obligors: {total_distinct_obligors}")
            logger.info("Successfully calculated all obligors statistics.")

            return results

        except Exception as e:
            logger.error(f"Error calculating obligors statistics: {e}")
            raise DataQualityError(f"Error calculating obligors statistics: {e}") from e
