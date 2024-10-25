import pandas as pd
from pyspark.sql import DataFrame
from pyspark.sql import SparkSession


class Indicator:
    """
    Classe de base pour gérer et calculer les indicateurs d'un datapack.

    Attributs:
    - name: Nom de l'indicateur.
    - data: DataFrame PySpark contenant les données nécessaires au calcul de l'indicateur.
    - type_family: Famille de l'indicateur, par exemple 'PD' ou 'LGD'.
    - period: Période de l'indicateur (par exemple, année N ou N-1).
    """

    def __init__(self, name: str, data: DataFrame, type_family: str, period: str):
        self.name = name
        self.data = data
        self.type_family = type_family
        self.period = period


class DefaultRate(Indicator):
    """
    Classe pour calculer le taux de défaut, héritant de Indicator.

    Méthodes:
    - calculate(): Calcule le taux de défaut en fonction de la colonne 'is_default'.
    """

    def __init__(self, name: str, data: DataFrame, type_family: str = 'PD', period: str = 'N'):
        super().__init__(name, data, type_family, period)

    def calculate(self, default_column: str = 'is_default') -> pd.DataFrame:
        """
        Calcule le taux de défaut dans le DataFrame.

        :param default_column: Nom de la colonne indiquant si une entité est en défaut (1 = défaut, 0 = non).
        :return: DataFrame Pandas contenant le taux de défaut calculé.
        """
        total_count = self.data.count()
        default_count = self.data.filter(self.data[default_column] == 1).count()
        default_rate = default_count / total_count if total_count > 0 else 0

        result = pd.DataFrame({"DefaultRate": [default_rate]})
        print(f"Taux de défaut pour {self.name} ({self.period}): {default_rate * 100:.2f}%")
        return result


class MigrationMatrix(Indicator):
    """
    Classe pour calculer la matrice de migration, héritant de Indicator.

    Méthodes:
    - calculate(): Calcule une matrice de migration en fonction des colonnes 'rating' et 'previous_rating'.
    """

    def __init__(self, name: str, data: DataFrame, type_family: str = 'Migration', period: str = 'N'):
        super().__init__(name, data, type_family, period)

    def calculate(self, rating_column: str = 'rating', previous_rating_column: str = 'previous_rating') -> pd.DataFrame:
        """
        Calcule une matrice de migration basée sur les changements de rating entre deux périodes.

        :param rating_column: Nom de la colonne indiquant la note de risque.
        :param previous_rating_column: Nom de la colonne indiquant la note de risque de la période précédente.
        :return: DataFrame Pandas représentant la matrice de migration.
        """
        migration_matrix = self.data.groupBy(previous_rating_column, rating_column).count()
        migration_matrix_pandas = migration_matrix.toPandas()
        print("Matrice de migration :")
        print(migration_matrix_pandas)
        return migration_matrix_pandas


class BackInBonis(Indicator):
    """
    Classe pour calculer le taux de back-in-bonis, héritant de Indicator.

    Méthodes:
    - calculate(): Calcule le taux de back-in-bonis en fonction des colonnes 'is_default' et 'is_recovered'.
    """

    def __init__(self, name: str, data: DataFrame, type_family: str = 'Recovery', period: str = 'N'):
        super().__init__(name, data, type_family, period)

    def calculate(self, default_column: str = 'is_default', recovery_column: str = 'is_recovered') -> pd.DataFrame:
        """
        Calcule le taux de back-in-bonis, c'est-à-dire la proportion des défauts qui ont été récupérés.

        :param default_column: Nom de la colonne indiquant le défaut initial.
        :param recovery_column: Nom de la colonne indiquant si le défaut a été récupéré.
        :return: DataFrame Pandas contenant le taux de back-in-bonis calculé.
        """
        default_cases = self.data.filter(self.data[default_column] == 1)
        recovered_count = default_cases.filter(default_cases[recovery_column] == 1).count()
        back_in_bonis_rate = recovered_count / default_cases.count() if default_cases.count() > 0 else 0

        result = pd.DataFrame({"BackInBonisRate": [back_in_bonis_rate]})
        print(f"Taux de back-in-bonis pour {self.name} ({self.period}): {back_in_bonis_rate * 100:.2f}%")
        return result

# Initialisation de Spark et d'un DataFrame avec des données fictives
spark = SparkSession.builder.appName("IndicatorTests").getOrCreate()
data = [
    Row(is_default=1, rating="A", previous_rating="B", is_recovered=1),
    Row(is_default=0, rating="B", previous_rating="B", is_recovered=0),
    Row(is_default=1, rating="C", previous_rating="A", is_recovered=1),
    Row(is_default=0, rating="A", previous_rating="C", is_recovered=0),
    Row(is_default=1, rating="B", previous_rating="A", is_recovered=0),
]
df = spark.createDataFrame(data)

# Calcul des indicateurs
default_rate = DefaultRate(name="DefaultRateIndicator", data=df)
default_rate.calculate()

migration_matrix = MigrationMatrix(name="MigrationMatrixIndicator", data=df)
migration_matrix.calculate()

back_in_bonis = BackInBonis(name="BackInBonisIndicator", data=df)
back_in_bonis.calculate()
