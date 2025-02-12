from import_data import data_loader
from data_quality import DataQuality
import time


def collect_data(progress_callback):
    progress_callback(25, "1/4 - Collecte des données terminée.")
    # Initialiser avec le chemin du répertoire
    instance_data = data_loader(r"C:\Users\FayçalOUSSEINIMALI\Desktop\DASH\Dash\nx_projet_automatisation\input")

    # Charger les données à partir du premier fichier trouvé dans le répertoire
    df = instance_data.load_data()
    df1 = instance_data.get_data()
    # Afficher les informations sur les données
    instance_data.show_info()
    # Prévisualiser les 10 premières lignes
    preview = instance_data.preview_data(20)
    print(preview)
    time.sleep(2)
    return df1


def data_quality(progress_callback):
    progress_callback(50, "2/4 - Contrôle qualité des données terminé.")
    # Initialiser la classe DataQuality
    dq = DataQuality(collect_data(progress_callback))
    # Générer le rapport
    dq.generate_report()
    # Afficher le rapport
    dq.show_report()
    time.sleep(2)


def calculate_indicators(progress_callback):
    progress_callback(75, "3/4 - Calcul des indicateurs terminé.")
    time.sleep(2)


def generate_datapack(progress_callback):
    progress_callback(100, "4/4 - Génération du datapack terminée.")
    time.sleep(2)
