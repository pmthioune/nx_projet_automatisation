# exceptions.py

class CustomException(Exception):
    """Exception de base pour les erreurs spécifiques au projet."""
    pass

class DatapackError(CustomException):
    """Exception pour les erreurs spécifiques à la classe Datapack."""
    def __init__(self, message="Erreur dans le traitement du Datapack"):
        self.message = message
        super().__init__(self.message)

class DataError(CustomException):
    """Exception pour les erreurs spécifiques à la classe Data."""
    def __init__(self, message="Erreur dans la collecte ou traitement des données"):
        self.message = message
        super().__init__(self.message)

class IndicatorError(CustomException):
    """Exception pour les erreurs spécifiques à la classe Indicator."""
    def __init__(self, message="Erreur dans le calcul ou traitement de l'indicateur"):
        self.message = message
        super().__init__(self.message)

class DataQualityError(CustomException):
    """Exception pour les erreurs spécifiques à la classe DataQuality."""
    def __init__(self, message="Erreur dans l'analyse de la qualité des données"):
        self.message = message
        super().__init__(self.message)
