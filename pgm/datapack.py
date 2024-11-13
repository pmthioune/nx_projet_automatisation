# data_processing/datapack.py
import os
from .exceptions import FolderCreationError
from .logger_config import logger

class Datapack:
    def __init__(self, name):
        self.name = name

    def generate_folder(self):
        folder_path = f"./output/{self.name}"
        try:
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
                logger.info(f"Folder created successfully at {folder_path}")
            else:
                logger.warning(f"Folder already exists at {folder_path}")
        except PermissionError as e:
            error_message = f"Permission denied: Cannot create folder at {folder_path}. Error: {e}"
            logger.error(error_message)
            raise FolderCreationError(error_message) from e
        except OSError as e:
            error_message = f"OS error occurred while creating folder at {folder_path}. Error: {e}"
            logger.error(error_message)
            raise FolderCreationError(error_message) from e
        except Exception as e:
            error_message = f"Unexpected error during folder creation at {folder_path}. Error: {e}"
            logger.error(error_message)
            raise FolderCreationError(error_message) from e
