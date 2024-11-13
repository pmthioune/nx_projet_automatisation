# exceptions.py

# data_processing/exceptions.py

class DataQualityError(Exception):
    """Base class for all data quality related errors."""
    def __init__(self, message, *args):
        super().__init__(message, *args)
        self.message = message

class MissingValuesError(DataQualityError):
    """Raised when there are missing values in the dataset."""
    def __init__(self, message, *args):
        super().__init__(message, *args)
        self.message = message

class DuplicatesError(DataQualityError):
    """Raised when there are duplicate rows in the dataset."""
    def __init__(self, message, *args):
        super().__init__(message, *args)
        self.message = message

class OutliersError(DataQualityError):
    """Raised when outliers are detected in the dataset."""
    def __init__(self, message, *args):
        super().__init__(message, *args)
        self.message = message

