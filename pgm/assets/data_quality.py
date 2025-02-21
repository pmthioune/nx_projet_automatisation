import dash
import dash_bootstrap_components as dbc
import pandas as pd
import os
import numpy as np

REPORT_DIR = r"C:\Users\FayçalOUSSEINIMALI\Desktop\DASH\Dash\nx_projet_automatisation\output"
if not os.path.exists(REPORT_DIR):
    os.makedirs(REPORT_DIR)


# Data Quality Report Function
def data_quality_report(df, id_column, date_column=None):
    """
    Generate an advanced data quality report for the given dataframe.

    Parameters:
        df (pandas.DataFrame): The dataframe to analyze.
        id_column (str): The name of the ID column for checking duplicates.
        date_column (str, optional): The name of the timestamp column for timeliness check.

    Returns:
        dict: A dictionary with the data quality metrics.
    """
    report = {'total_missing': df.isnull().sum().sum(), 'missing_per_variable': df.isnull().sum(),
              'single_value_columns': df.nunique()[df.nunique() == 1].index.tolist(),
              'summary_statistics': df.describe(include='all')}

    # 🔹 Valeurs manquantes

    # 🔹 Colonnes contenant une seule valeur (peu utiles)

    # 🔹 Statistiques descriptives générales

    # 🔹 Sélection des colonnes numériques
    numeric_df = df.select_dtypes(include=['number'])

    if not numeric_df.empty:
        # 🔹 Détection des outliers par IQR
        Q1 = numeric_df.quantile(0.25)
        Q3 = numeric_df.quantile(0.75)
        IQR = Q3 - Q1
        report['outliers'] = ((numeric_df < (Q1 - 1.5 * IQR)) | (numeric_df > (Q3 + 1.5 * IQR))).sum()

        # 🔹 Détection des outliers par Z-score
        z_scores = np.abs((numeric_df - numeric_df.mean()) / numeric_df.std())
        report['outliers_zscore'] = (z_scores > 3).sum()

        # 🔹 Corrélation entre colonnes numériques
        correlation_matrix = numeric_df.corr()
        high_corr_pairs = [(col1, col2, correlation_matrix.loc[col1, col2])
                           for col1 in correlation_matrix.columns
                           for col2 in correlation_matrix.columns
                           if col1 != col2 and np.abs(correlation_matrix.loc[col1, col2]) > 0.8]
        report['highly_correlated_columns'] = high_corr_pairs

    else:
        report['outliers_iqr'] = "No numerical columns"
        report['outliers_zscore'] = "No numerical columns"
        report['highly_correlated_columns'] = "No numerical columns"

    # 🔹 Vérification des types de données
    report['data_types'] = df.dtypes

    # 🔹 Nombre de valeurs uniques
    report['unique_values'] = df.nunique()
    report['uniqueness'] = (df.nunique() / len(df) * 100).round(2)

    # 🔹 Détection des doublons
    report['duplicates'] = df.duplicated().sum()

    # 🔹 Vérification des doublons basés sur `id_column`
    if id_column in df.columns:
        report['duplicates_by_id'] = df.duplicated(subset=[id_column]).sum()
    else:
        report['duplicates_by_id'] = 'ID column not found'

    # 🔹 Vérification de la fraîcheur des données (`timeliness`)
    if date_column and date_column in df.columns:
        date_series = pd.to_datetime(df[date_column], errors='coerce')
        if date_series.isna().all():
            report['timeliness'] = 'All dates are invalid'
        else:
            report['timeliness'] = (date_series.max() - date_series.min()).days
    else:
        report['timeliness'] = 'Date column not provided or invalid'

    return report


def save_data_quality_report(report):
    try:
        # Créer un fichier texte pour enregistrer le rapport de qualité des données
        report_file_path = os.path.join(REPORT_DIR, 'data_quality_report.txt')

        with open(report_file_path, 'w') as f:
            f.write("=== Data Quality Report ===\n\n")
            f.write(f"Total Missing Values: {report['total_missing']}\n\n")

            f.write("=== Missing Values per Variable ===\n")
            for var, missing in report['missing_per_variable'].items():
                f.write(f"{var}: {missing}\n")

            f.write("\n=== Outliers detected in variables ===\n")
            for var, outliers in report['outliers'].items():
                f.write(f"{var}: {outliers} outliers\n")

            f.write("\n=== Unique Values per Variable ===\n")
            for var, unique in report['unique_values'].items():
                f.write(f"{var}: {unique} unique values\n")

            f.write("\n=== Uniqueness (Percentage of Unique Values) ===\n")
            for var, uniqueness in report['uniqueness'].items():
                f.write(f"{var}: {uniqueness:.2f}% unique\n")

            f.write("\n=== Duplicates Analysis ===\n")
            f.write(f"Total Duplicates: {report['duplicates']}\n")
            f.write(f"Duplicates based on ID column: {report['duplicates_by_id']}\n")

            f.write("\n=== Timeliness Analysis ===\n")
            f.write(f"Timeliness (Time Span in Days): {report['timeliness']}\n")

        return report_file_path  # Renvoie le chemin du fichier créé

    except Exception as e:
        print(f"Error saving data quality report: {e}")
        return None
