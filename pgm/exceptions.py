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
