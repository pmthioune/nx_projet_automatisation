import time

def collect_data(progress_callback):
    progress_callback(25, "1/4 - Collecte des données terminée.")
    time.sleep(2)

def data_quality(progress_callback):
    progress_callback(50, "2/4 - Contrôle qualité des données terminé.")
    time.sleep(2)

def calculate_indicators(progress_callback):
    progress_callback(75, "3/4 - Calcul des indicateurs terminé.")
    time.sleep(2)

def generate_datapack(progress_callback):
    progress_callback(100, "4/4 - Génération du datapack terminée.")
    time.sleep(2)
