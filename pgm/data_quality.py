import pandas as pd
from import_data import data_loader


class DataQuality:
    def __init__(self, dataframe):
        self.dataframe = dataframe
        self.report = {}

    def check_missing_values(self):
        # Calcul du nombre de valeurs manquantes pour chaque colonne
        missing_values = self.dataframe.isnull().sum()
        missing_percentage = (missing_values / len(self.dataframe)) * 100
        self.report['missing_values'] = pd.DataFrame({
            'missing_values': missing_values,
            'missing_percentage': missing_percentage
        })

    def check_duplicates(self):
        # Vérification des doublons dans les données
        duplicates = self.dataframe.duplicated().sum()
        self.report['duplicates'] = duplicates

    def check_data_types(self):
        # Vérification des types de données
        data_types = self.dataframe.dtypes
        self.report['data_types'] = data_types

    def check_unique_values(self):
        # Vérification des valeurs uniques dans chaque colonne
        unique_values = self.dataframe.nunique()
        self.report['unique_values'] = unique_values

    def check_statistics(self):
        # Statistiques descriptives pour les colonnes numériques
        statistics = self.dataframe.describe()
        self.report['statistics'] = statistics

    def detect_outliers(self):
        # Filtrer uniquement les colonnes numériques
        numeric_df = self.dataframe.select_dtypes(include=['number'])

        # Vérification que nous avons des colonnes numériques
        if numeric_df.empty:
            print("Aucune colonne numérique trouvée pour détecter les valeurs aberrantes.")
            return

        # Détection des valeurs aberrantes (outliers) avec la méthode IQR (Interquartile Range)
        Q1 = numeric_df.quantile(0.25)
        Q3 = numeric_df.quantile(0.75)
        IQR = Q3 - Q1
        outliers = ((numeric_df < (Q1 - 1.5 * IQR)) | (numeric_df > (Q3 + 1.5 * IQR))).sum()
        self.report['outliers'] = outliers

    def generate_report(self):
        # Générer le rapport global
        self.check_missing_values()
        self.check_duplicates()
        self.check_data_types()
        self.check_unique_values()
        self.check_statistics()
        self.detect_outliers()

        return self.report

    def show_report(self):
        # Afficher le rapport
        for key, value in self.report.items():
            print(f"Report for {key}:")
            print(value)
            print("-" * 50)

