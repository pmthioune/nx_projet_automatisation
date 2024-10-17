from pyspark.sql import DataFrame, SparkSession


class Data:
    def __init__(self, id_data, raw_data: DataFrame, source: str):
        self.id_data = id_data
        self.raw_data = raw_data  # Spark DataFrame with raw data
        self.cleaned_data = None
        self.source = source
        self.status = 'raw'  # raw, cleaned

    def clean(self):
        # Example cleaning logic: remove null values, handle outliers
        self.cleaned_data = self.raw_data.dropna()  # Drop rows with null values
        self.status = 'cleaned'
        return self.cleaned_data

    def process(self):
        # Process the cleaned data for further use, such as filtering or transforming it
        if self.cleaned_data is not None:
            processed_data = self.cleaned_data.filter("value > 0")  # Example filtering condition
            return processed_data
        else:
            raise Exception("Data must be cleaned before processing.")
