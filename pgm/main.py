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



