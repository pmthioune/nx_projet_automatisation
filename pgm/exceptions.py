# data_processing/exceptions.py

class DataCollectionError(Exception):
    """Raised when there is an error in data collection."""
    pass

class DataQualityError(Exception):
    """Raised when there is an error in data quality analysis."""
    pass

class CalculationError(Exception):
    """Raised when there is an error in calculating indicators."""
    pass

class DatapackGenerationError(Exception):
    """Raised when there is an error in generating the datapack."""
    pass


