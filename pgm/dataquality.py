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

    def check_duplicates(self, columns: list):
        """
        Vérifie la présence de doublons dans les données PySpark pour les colonnes spécifiées.

        :param columns: list, colonnes sur lesquelles la recherche de doublons sera effectuée.
        :return: DataFrame, les doublons détectés.
        """
        print(f"Vérification des doublons sur les colonnes: {columns}...")

        # Créer un DataFrame sans doublons
        unique_data = self.data.dropDuplicates(subset=columns)

        # Identifier les doublons en comparant le DataFrame d'origine avec celui sans doublons
        duplicates = self.data.exceptAll(unique_data)

        # Afficher et retourner les doublons
        if duplicates.count() > 0:
            print("Doublons détectés :")
            duplicates.show()
        else:
            print("Aucun doublon détecté.")

        return duplicates

    def check_outliers(self, columns_thresholds: dict):
        """
        Vérifie les valeurs hors des seuils (outliers) dans les colonnes spécifiées.

        :param columns_thresholds: dict, dictionnaire contenant les colonnes et leurs seuils sous forme de tuples (min, max).
                                   Exemple: {'CA': (10000, 500000), 'EAD': (5000, 2000000)}
        :return: DataFrame, contenant les valeurs qui sont des outliers.
        """
        outliers_conditions = []

        # Construction des conditions pour chaque colonne
        for column, (min_threshold, max_threshold) in columns_thresholds.items():
            outliers_conditions.append((col(column) < min_threshold) | (col(column) > max_threshold))

        # Combiner les conditions avec un OR logique
        outliers_condition = outliers_conditions[0]
        for condition in outliers_conditions[1:]:
            outliers_condition = outliers_condition | condition

        # Filtrer les lignes contenant des outliers
        outliers_df = self.data.filter(outliers_condition)

        # Afficher les résultats
        if outliers_df.count() > 0:
            print("Outliers détectés :")
            outliers_df.show()
        else:
            print("Aucun outlier détecté.")

        return outliers_df

    def generer_rapport(self):
        """
        Génère un rapport de qualité basé sur les tests effectués.

        :return: dict, rapport complet des vérifications de qualité des données.
        """
        print("Génération du rapport de qualité des données...")
        return self.rapport
