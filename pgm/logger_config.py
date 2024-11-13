# data_processing/logger_config.py
import logging
import os

# Chemin du fichier de logs
log_file_path = os.path.join(os.path.dirname(__file__), "debug.log")

# Configuration du logger global
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("DataProcessingApp")

# Ajout d'un gestionnaire de fichier pour les logs
file_handler = logging.FileHandler(log_file_path)
file_handler.setLevel(logging.DEBUG)  # Niveau de log pour le fichier
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger.addHandler(file_handler)

# Optionnel : Si vous souhaitez également afficher les logs dans la console
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)  # Niveau de log pour la console
stream_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger.addHandler(stream_handler)
