# data_processing/data_quality.py
from .exceptions import DataQualityError
from .logger_config import logger

class DataQuality:
    def __init__(self, data):
        self.data = data

    def check_missing_values(self, columns_to_check):
        try:
            for column in columns_to_check:
                if self.data[column].isnull().any():
                    logger.warning(f"Missing values found in column {column}")
            logger.info("Missing values check completed.")
        except Exception as e:
            logger.error(f"Error checking missing values: {e}")
            raise DataQualityError(f"Error checking missing values: {e}") from e

    def check_duplicates(self):
        try:
            if self.data.duplicated().any():
                logger.warning("Duplicates found in the data.")
            logger.info("Duplicate check completed.")
        except Exception as e:
            logger.error(f"Error checking duplicates: {e}")
            raise DataQualityError(f"Error checking duplicates: {e}") from e

    def check_outliers(self, column):
        try:
            if not column in self.data.columns:
                raise DataQualityError(f"Column {column} not found for outlier check")
            outliers = self.data[column][(self.data[column] < -3) | (self.data[column] > 3)]
            if not outliers.empty:
                logger.warning(f"Outliers detected in column {column}.")
            logger.info("Outlier check completed.")
        except Exception as e:
            logger.error(f"Error checking outliers: {e}")
            raise DataQualityError(f"Error checking outliers: {e}") from e
