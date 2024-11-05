# process.py

from exceptions import DatapackError, DataError, IndicatorError, DataQualityError


class Process:
    def __init__(self):
        # Initialisation et configuration du process
        pass

    @staticmethod
    def manage_exception(exception):
        """Gère les exceptions spécifiques et log les erreurs."""
        if isinstance(exception, DatapackError):
            print(f"Erreur Datapack: {exception}")
            # Logique de gestion des erreurs Datapack ici
        elif isinstance(exception, DataError):
            print(f"Erreur Data: {exception}")
            # Logique de gestion des erreurs Data ici
        elif isinstance(exception, IndicatorError):
            print(f"Erreur Indicator: {exception}")
            # Logique de gestion des erreurs Indicator ici
        elif isinstance(exception, DataQualityError):
            print(f"Erreur DataQuality: {exception}")
            # Logique de gestion des erreurs DataQuality ici
        else:
            print(f"Erreur inconnue : {exception}")

    def run_process(self):
        """Méthode principale pour exécuter le process et gérer les exceptions."""
        try:
            # Exemple d'appel aux méthodes des classes Data, Datapack, etc.
            # Chaque méthode ici peut lever une exception spécifique à gérer

            # Exemple d'appel de méthode potentiellement risquée
            self.some_risky_method()

        except (DatapackError, DataError, IndicatorError, DataQualityError) as e:
            self.manage_exception(e)
        except Exception as e:
            print("Erreur inattendue :", e)

    def some_risky_method(self):
        # Exemple de méthode risquée pouvant lever une exception
        raise DataError("Erreur simulée dans la collecte des données.")
