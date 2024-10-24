class DataQuality:
    """
    Classe représentant l'analyse de la qualité des données pour un indicateur donné.

    Attributs:
    - data: dict ou DataFrame : Les données sur lesquelles effectuer les vérifications de qualité.
    - rapport: dict : Rapport des vérifications effectuées (contient les résultats des tests de qualité).

    Méthodes:
    - verifier_valeurs_manquantes(): Vérifie si les données contiennent des valeurs manquantes.
    - verifier_doublons(): Vérifie la présence de doublons dans les données.
    - detecter_outliers(): Identifie des valeurs aberrantes dans les données.
    - generer_rapport(): Compile les résultats des vérifications de qualité en un rapport détaillé.
    """

    def __init__(self, data):
        """
        Initialise l'instance avec les données à analyser.

        :param data: dict ou DataFrame, données brutes sur lesquelles les tests de qualité seront effectués.
        """
        self.data = data
        self.rapport = {}

    def check_missing_values(self):
        """
        Vérifie la présence de valeurs manquantes dans les colonnes du DataFrame PySpark.

        :return: DataFrame, rapport des colonnes avec des valeurs manquantes et leur quantité.
        """
        print("Vérification des valeurs manquantes dans le DataFrame PySpark...")
        missing_value_report = self.data.select(
            [(spark_sum(col(c).isNull().cast("int")).alias(c)) for c in self.data.columns]
        )

        # Affichage du rapport des colonnes contenant des valeurs manquantes
        missing_value_report.show()
        return missing_value_report

    def verifier_doublons(self):
        """
        Vérifie la présence de doublons dans les données.

        :return: int, nombre de doublons détectés.
        """
        print("Vérification des doublons...")
        # Simuler la détection de doublons
        unique_values = set(self.data.values())
        doublons = len(self.data) - len(unique_values)
        self.rapport['doublons'] = doublons
        return doublons

    def detecter_outliers(self, seuil_bas, seuil_haut):
        """
        Détecte les valeurs aberrantes dans les données en fonction des seuils donnés.

        :param seuil_bas: float, seuil minimal pour définir une valeur aberrante.
        :param seuil_haut: float, seuil maximal pour définir une valeur aberrante.
        :return: list, valeurs identifiées comme aberrantes.
        """
        print("Détection des valeurs aberrantes (outliers)...")
        # Simuler la détection d'outliers en se basant sur des seuils
        outliers = [value for value in self.data.values() if value < seuil_bas or value > seuil_haut]
        self.rapport['outliers'] = outliers
        return outliers

    def generer_rapport(self):
        """
        Génère un rapport de qualité basé sur les tests effectués.

        :return: dict, rapport complet des vérifications de qualité des données.
        """
        print("Génération du rapport de qualité des données...")
        return self.rapport
