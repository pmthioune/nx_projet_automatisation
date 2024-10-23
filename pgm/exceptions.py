class DatapackException(Exception):
    """
    Classe de base pour toutes les exceptions liées au Datapack.
    Hérite de la classe Exception de Python.
    """

    def __init__(self, message):
        super().__init__(message)
        self.message = message


class DataQualityException(DatapackException):
    """
    Exception levée lorsqu'un problème de qualité des données est détecté.
    """

    def __init__(self, message="Erreur de qualité des données détectée."):
        super().__init__(message)


class DataNotFoundException(DatapackException):
    """
    Exception levée lorsqu'un fichier de données attendu est introuvable.
    """

    def __init__(self, message="Données introuvables."):
        super().__init__(message)


class FolderCreationException(DatapackException):
    """
    Exception levée lorsqu'une erreur se produit lors de la création d'un dossier.
    """

    def __init__(self, message="Erreur lors de la création du dossier."):
        super().__init__(message)


class GapAnalysisException(DatapackException):
    """
    Exception levée lorsqu'une erreur se produit lors de l'analyse de gap.
    """

    def __init__(self, message="Erreur lors de l'analyse de gap."):
        super().__init__(message)


class DatapackExceptionManager:
    """
    Gestionnaire d'exceptions pour capturer et gérer les erreurs liées aux opérations du Datapack.
    """

    @staticmethod
    def handle_exception(exception: DatapackException):
        """
        Gère les exceptions liées au Datapack.
        :param exception: Instance d'une exception de type DatapackException.
        :return: Message d'erreur spécifique.
        """
        if isinstance(exception, DataQualityException):
            print(f"DataQualityException: {exception.message}")
        elif isinstance(exception, DataNotFoundException):
            print(f"DataNotFoundException: {exception.message}")
        elif isinstance(exception, FolderCreationException):
            print(f"FolderCreationException: {exception.message}")
        elif isinstance(exception, GapAnalysisException):
            print(f"GapAnalysisException: {exception.message}")
        else:
            print(f"UnknownException: {exception.message}")


class Datapack:
    """
    Classe simplifiée Datapack avec gestion des exceptions.
    """

    def __init__(self, id_datapack: int, name: str):
        self.id_datapack = id_datapack
        self.name = name
        self.indicators = {}
        self.creation_date = datetime.now().strftime("%Y-%m-%d_%H-%M")
        self.gap_analysis_results = {}

    def generate_folder(self):
        """
        Méthode pour générer un dossier, avec gestion des exceptions en cas d'erreur.
        """
        try:
            # Obtenir le chemin du répertoire du script
            script_directory = os.path.dirname(os.path.abspath(__file__))

            # Chemin du dossier à créer avec date, heure et minute
            folder_name = f"datapack_{self.name}_{self.creation_date}"
            folder_path = os.path.join(script_directory, folder_name)

            # Créer le dossier de sortie s'il n'existe pas déjà
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
            else:
                raise FolderCreationException("Le dossier existe déjà.")

            return folder_path
        except Exception as e:
            # Gérer l'exception en utilisant le gestionnaire central
            DatapackExceptionManager.handle_exception(FolderCreationException(str(e)))

    def add_indicator(self, indicator_name: str, indicator_data: DataFrame):
        """
        Ajoute un indicateur au datapack avec gestion d'une éventuelle exception si les données sont manquantes.
        """
        try:
            if indicator_data is None:
                raise DataNotFoundException(f"Les données pour l'indicateur {indicator_name} sont manquantes.")

            self.indicators[indicator_name] = indicator_data
        except Exception as e:
            DatapackExceptionManager.handle_exception(DataNotFoundException(str(e)))

