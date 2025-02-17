
import os
from process import collect_data, data_quality, calculate_indicators, generate_datapack


# Stocke la progression et le message en cours
progress_state = {"progress": 0, "message": "En attente de démarrage..."}

def progress_callback(progress, message):
    """Met à jour la progression globale."""
    progress_state["progress"] = progress
    progress_state["message"] = message

def start_process():
    """Exécute le programme principal avec mises à jour."""
    collect_data(progress_callback)
    data_quality(progress_callback)
    calculate_indicators(progress_callback)
    generate_datapack(progress_callback)

def get_progress():
    """Renvoie la progression actuelle."""
    return progress_state

OUTPUT_DIR = '../../output'
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

INPUT_DIR = r"C:\Users\FayçalOUSSEINIMALI\Desktop\DASH\Dash\nx_projet_automatisation\input"
input_file = os.path.join(INPUT_DIR, 'demographic_data.csv')

LANGUAGES = {
    "fr": "Français",
    "en": "English"
}

