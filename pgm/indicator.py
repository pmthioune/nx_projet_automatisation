class Indicator:
    def __init__(self, name, data, family, period):
        """
        Classe de base pour les indicateurs.

        :param name: Nom de l'indicateur
        :param data: Données d'entrée (DataFrame ou autre structure)
        :param family: Famille d'indicateur (par ex. "Default Rates", "Migration Matrix", etc.)
        :param period: Période de calcul (par ex. "N", "N-1")
        """
        self.name = name
        self.data = data
        self.family = family
        self.period = period

    def calculate(self):
        """
        Méthode générique pour le calcul d'un indicateur.
        À surcharger dans les classes dérivées.
        """
        raise NotImplementedError("La méthode calculate() doit être implémentée dans la classe dérivée.")

    def to_dict(self):
        """
        Retourne un dictionnaire contenant les informations de l'indicateur et le résultat du calcul.
        """
        try:
            result = self.calculate()
            return {
                "name": self.name,
                "family": self.family,
                "period": self.period,
                "result": result
            }
        except NotImplementedError as e:
            return {
                "name": self.name,
                "family": self.family,
                "period": self.period,
                "error": str(e)
            }

class DefaultRatesNumber(Indicator):
    def __init__(self, name, data, family, period):
        """
        Classe pour le calcul des taux de défaut en nombre.
        :param name: Nom de l'indicateur
        :param data: Données d'entrée
        :param family: Famille d'indicateurs (par ex. "Default Rates")
        :param period: Période (N, N-1)
        """
        super().__init__(name, data, family, period)
        self.nb_columns = len(data.columns)
        self.nb_years = len(data)  # Exemple : basé sur le nombre de lignes de données.
        self.end_year = int(data.columns[-1][5:9])  # Extraction de la dernière année des colonnes.
        self.last_month = int(data.columns[-1][9:11])  # Extraction du dernier mois des colonnes.
        self.indicator_results = {}  # Dictionnaire pour stocker les résultats des indicateurs

    def calculate_indicator(self, id_indicator):
        """
        Calcule un indicateur spécifique basé sur l'id_indicator.
        :param id_indicator: Identifiant de l'indicateur (par exemple, "default_rate", "sains_total").
        """
        try:
            if id_indicator == "default_rate":
                sains_total = self.data["sains"].sum()
                defaults_total = self.data["defaults"].sum()
                result = defaults_total / (sains_total + defaults_total) if (sains_total + defaults_total) > 0 else 0
                self.indicator_results[id_indicator] = result
            elif id_indicator == "sains_total":
                result = self.data["sains"].sum()
                self.indicator_results[id_indicator] = result
            elif id_indicator == "defaults_total":
                result = self.data["defaults"].sum()
                self.indicator_results[id_indicator] = result
            else:
                raise ValueError(f"Indicateur inconnu : {id_indicator}")
        except KeyError as e:
            raise ValueError(f"Colonne manquante dans les données : {e}")

    def calculate_all_indicators(self):
        """
        Calcule tous les indicateurs disponibles (par exemple, default_rate, sains_total, defaults_total).
        """
        for id_indicator in ["default_rate", "sains_total", "defaults_total"]:
            self.calculate_indicator(id_indicator)

    def to_dict(self):
        """
        Retourne un dictionnaire contenant les résultats des indicateurs et les attributs spécifiques.
        """
        result = super().to_dict()  # Appelle la méthode to_dict() de la classe parente.
        result.update({
            "nb_columns": self.nb_columns,
            "nb_years": self.nb_years,
            "end_year": self.end_year,
            "last_month": self.last_month,
            "indicator_results": self.indicator_results
        })
        return result
