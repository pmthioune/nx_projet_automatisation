import dash
import dash_bootstrap_components as dbc
import pandas as pd
import os

REPORT_DIR = r"C:\Users\FayçalOUSSEINIMALI\Desktop\DASH\Dash\nx_projet_automatisation\output"
if not os.path.exists(REPORT_DIR):
    os.makedirs(REPORT_DIR)

# Data Quality Report Function
def data_quality_report(df, id_column):
    """
    Generate a detailed data quality report for the given dataframe.

    Parameters:
        df (pandas.DataFrame): The dataframe to analyze.
        id_column (str): The name of the ID column for checking duplicates.

    Returns:
        dict: A dictionary with the data quality metrics.
    """
    report = {}

    # Total missing values in the dataframe
    report['total_missing'] = df.isnull().sum().sum()

    # Missing values per column
    report['missing_per_variable'] = df.isnull().sum()

    # Select only numeric columns for outlier detection
    numeric_df = df.select_dtypes(include=['number'])

    # Outlier detection using the Interquartile Range (IQR) method
    Q1 = numeric_df.quantile(0.25)
    Q3 = numeric_df.quantile(0.75)
    IQR = Q3 - Q1
    report['outliers'] = ((numeric_df < (Q1 - 1.5 * IQR)) | (numeric_df > (Q3 + 1.5 * IQR))).sum()

    # Count of unique values per column
    report['unique_values'] = df.nunique()

    # Check for duplicate rows
    report['duplicates'] = df.duplicated().sum()

    # Check for duplicates based on the ID column, if it exists
    if id_column in df.columns:
        report['duplicates_by_id'] = df.duplicated(subset=[id_column]).sum()
    else:
        report['duplicates_by_id'] = 'ID column not found'

    return report


def save_data_quality_report(report):
    try:
        # Créer un fichier texte pour enregistrer le rapport de qualité des données
        report_file_path = os.path.join(REPORT_DIR, 'data_quality_report.txt')

        with open(report_file_path, 'w') as f:
            f.write(f"Total Missing Values: {report['total_missing']}\n\n")
            f.write("Missing Values per Variable:\n")
            for var, missing in report['missing_per_variable'].items():
                f.write(f"{var}: {missing}\n")

            f.write("\nOutliers detected in variables:\n")
            for var, outliers in report['outliers'].items():
                f.write(f"{var}: {outliers} outliers\n")

            f.write("\nUnique Values per Variable:\n")
            for var, unique in report['unique_values'].items():
                f.write(f"{var}: {unique} unique values\n")

            f.write("\nDuplicates Detected: " + str(report['duplicates']) + "\n")

        return report_file_path  # Renvoie le chemin du fichier créé

    except Exception as e:
        print(f"Error saving data quality report: {e}")
        return None