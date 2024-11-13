# data_processing/data_quality.py
import pandas as pd
from .exceptions import MissingValuesError, DuplicatesError, OutliersError
from .logger_config import logger


class DataQuality:
    def __init__(self, dataframe):
        self.dataframe = dataframe

    def check_missing_values(self, columns_to_check):
        try:
            missing_values = self.dataframe[columns_to_check].isnull().sum()
            if missing_values.any():
                logger.warning(f"Missing values found in columns: {missing_values[missing_values > 0].index.tolist()}")
                raise MissingValuesError(
                    f"Missing values detected in the following columns: {missing_values[missing_values > 0].index.tolist()}")
            else:
                logger.info("No missing values detected.")
        except KeyError as e:
            error_message = f"Column(s) not found in the dataframe: {e}"
            logger.error(error_message)
            raise MissingValuesError(error_message) from e
        except Exception as e:
            error_message = f"Unexpected error while checking missing values: {e}"
            logger.error(error_message)
            raise MissingValuesError(error_message) from e

    def check_duplicates(self):
        try:
            duplicates = self.dataframe.duplicated().sum()
            if duplicates > 0:
                logger.warning(f"{duplicates} duplicate rows detected.")
                raise DuplicatesError(f"{duplicates} duplicate rows detected.")
            else:
                logger.info("No duplicate rows detected.")
        except Exception as e:
            error_message = f"Unexpected error while checking duplicates: {e}"
            logger.error(error_message)
            raise DuplicatesError(error_message) from e

    def check_outliers(self, column, threshold=1.5):
        try:
            q1 = self.dataframe[column].quantile(0.25)
            q3 = self.dataframe[column].quantile(0.75)
            iqr = q3 - q1
            lower_bound = q1 - (iqr * threshold)
            upper_bound = q3 + (iqr * threshold)

            outliers = self.dataframe[(self.dataframe[column] < lower_bound) | (self.dataframe[column] > upper_bound)]

            if not outliers.empty:
                logger.warning(f"Outliers detected in column {column}.")
                raise OutliersError(f"Outliers detected in column {column}.")
            else:
                logger.info(f"No outliers detected in column {column}.")
        except KeyError as e:
            error_message = f"Column '{column}' not found in the dataframe: {e}"
            logger.error(error_message)
            raise OutliersError(error_message) from e
        except Exception as e:
            error_message = f"Unexpected error while checking for outliers in column {column}: {e}"
            logger.error(error_message)
            raise OutliersError(error_message) from e
