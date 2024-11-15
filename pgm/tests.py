import pandas as pd
from data_processing.data_quality import DataQuality

# Exemple de dataset
data = pd.DataFrame({
    'id_client': [1, 2, 3, 4, 1, 2, 5],
    'annee': ['2023', '2023', '2024', '2024', '2023', '2024', '2023'],
    'secteur': ['A', 'A', 'B', 'B', 'A', 'B', 'C']
})

# Initialiser l'objet DataQuality
data_quality = DataQuality(data)

# Calculer les statistiques
stats = data_quality.calculate_obligors_stats('id_client', 'annee', 'secteur')

# Afficher les résultats
print("Total Distinct Obligors:", stats["total_distinct_obligors"])
print("Obligors per Cohort:")
print(stats["obligors_per_cohort"])
print("Obligors per Pole and Cohort:")
print(stats["obligors_per_pole_cohort"])
