from pyspark.sql import DataFrame
from pyspark.sql.types import StringType
import pandas as pd
from pyspark.sql import functions as F


def convert_spark_to_pandas(df_spark: DataFrame) -> pd.DataFrame:
    """
    Convertit un DataFrame Spark en DataFrame Pandas en gérant les colonnes de type timestamp.

    Args:
        df_spark (DataFrame): Le DataFrame Spark à convertir.

    Returns:
        pd.DataFrame: Le DataFrame Pandas résultant avec les colonnes timestamp en datetime64[ns].
    """
    # Identifier les colonnes de type timestamp
    timestamp_columns = [col for col, dtype in df_spark.dtypes if dtype == "timestamp"]

    # Convertir uniquement les colonnes de type timestamp en string dans Spark
    for column in timestamp_columns:
        df_spark = df_spark.withColumn(column, F.col(column).cast(StringType()))

    # Convertir le DataFrame Spark en DataFrame Pandas
    df_pandas = df_spark.toPandas()

    # Reconvertir uniquement les colonnes timestamp en datetime64[ns] dans Pandas
    for column in timestamp_columns:
        df_pandas[column] = pd.to_datetime(df_pandas[column], errors="coerce")

    return df_pandas
