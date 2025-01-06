import os

class Indicator:
    def __init__(self, name, data, family, period):
        self.name = name
        self.data = data
        self.family = family
        self.period = period
        self.indicator_results = {}

    def calculate_indicator(self, id_indicator):
        """
        Méthode placeholder pour le calcul des indicateurs.
        À implémenter dans les classes dérivées.
        """
        raise NotImplementedError("Cette méthode doit être implémentée dans les sous-classes.")

    def generate_indicator(self, output_folder):
        """
        Génère des fichiers CSV pour les indicateurs calculés.
        :param output_folder: Chemin vers le dossier où les fichiers CSV seront enregistrés.
        """
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        for id_indicator, result in self.indicator_results.items():
            file_path = os.path.join(output_folder, f"{id_indicator}.csv")
            with open(file_path, "w") as f:
                f.write("Indicator,Value\n")
                f.write(f"{id_indicator},{result}\n")
        print(f"Les indicateurs ont été générés dans le dossier : {output_folder}")

    def to_dict(self):
        return {
            "name": self.name,
            "family": self.family,
            "period": self.period,
            "indicator_results": self.indicator_results
        }
