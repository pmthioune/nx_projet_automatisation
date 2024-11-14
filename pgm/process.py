# data_processing/process.py
from .data_collection import DataCollector
from .data_quality import DataQuality
from .indicator_calculation import IndicatorCalculator
from .datapack import Datapack
from .exceptions import DataCollectionError, DataQualityError, CalculationError, DatapackGenerationError
from .logger_config import logger

class Process:
    def __init__(self, data_source):
        self.data_source = data_source
        self.data_collector = DataCollector(data_source)
        self.data_quality = None
        self.indicator_calculator = None
        self.datapack = None

    def run_process(self):
        # Step 1: Data Collection
        try:
            logger.info("Starting data collection...")
            data = self.data_collector.collect_data()
            logger.info("Data collection completed successfully.")
        except Exception as e:
            error_message = f"Data collection failed: {e}"
            logger.error(error_message)
            raise DataCollectionError(error_message) from e

        # Step 2: Data Quality Analysis
        try:
            logger.info("Starting data quality analysis...")
            self.data_quality = DataQuality(data)
            self.data_quality.check_missing_values(['col1', 'col2'])
            self.data_quality.check_duplicates()
            self.data_quality.check_outliers('col3')
            logger.info("Data quality analysis completed successfully.")
        except DataQualityError as e:
            logger.error(f"Data quality analysis failed: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error during data quality analysis: {e}")
            raise DataQualityError("Data quality analysis failed") from e

        # Step 3: Indicator Calculation
        try:
            logger.info("Starting indicator calculation...")
            self.indicator_calculator = IndicatorCalculator(data)
            indicators = self.indicator_calculator.calculate()
            logger.info("Indicator calculation completed successfully.")
        except Exception as e:
            logger.error(f"Indicator calculation failed: {e}")
            raise CalculationError("Indicator calculation failed") from e

        # Step 4: Datapack Generation
        try:
            logger.info("Starting datapack generation...")
            self.datapack = Datapack(indicators)
            self.datapack.generate_folder()
            logger.info("Datapack generation completed successfully.")
        except Exception as e:
            logger.error(f"Datapack generation failed: {e}")
            raise DatapackGenerationError("Datapack generation failed") from e
