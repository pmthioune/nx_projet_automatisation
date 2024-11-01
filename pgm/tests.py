# Initialisation de Spark
spark = SparkSession.builder.appName("DatapackSimplified").getOrCreate()

# Dossier de sortie pour les rapports
output_folder = "/path/to/output"

# Créer une instance de la classe Datapack
datapack_instance = Datapack(id_datapack=1, name="RACER", output_folder=output_folder)

# Exemple de données pour les indicateurs (DataFrame Spark)
data_pd = spark.createDataFrame([("A", 0.1), ("B", 0.2)], ["category", "value"])
data_lgd = spark.createDataFrame([("A", 0.3), ("B", 0.4)], ["category", "value"])

# Ajouter les indicateurs au datapack
datapack_instance.add_indicator("PD", data_pd)
datapack_instance.add_indicator("LGD", data_lgd)

# Exemple de données pour N-1
data_n_minus_1_pd = spark.createDataFrame([("A", 0.05), ("B", 0.15)], ["category", "value"])
data_n_minus_1_lgd = spark.createDataFrame([("A", 0.25), ("B", 0.35)], ["category", "value"])

# Effectuer l'analyse de gap entre N et N-1
datapack_instance.perform_gap_analysis(
    n_data={"PD": data_pd, "LGD": data_lgd},
    n_minus_1_data={"PD": data_n_minus_1_pd, "LGD": data_n_minus_1_lgd}
)

# Générer le dossier contenant les fichiers du datapack et de l'analyse de gap
report_folder = datapack_instance.generate_folder()

print(f"Les fichiers ont été générés dans : {report_folder}")

from pyspark.sql import SparkSession
from pyspark.sql import Row

# Initialiser la session Spark
spark = SparkSession.builder.appName("DataQualityTests").getOrCreate()

# Exemple de données avec valeurs manquantes, doublons et outliers
data = [
    Row(CA=10000, EAD=200000),
    Row(CA=None, EAD=150000),       # Valeur manquante pour CA
    Row(CA=12000, EAD=3000),        # Outlier sur EAD
    Row(CA=250000, EAD=1500000),
    Row(CA=250000, EAD=1500000),    # Doublon
    Row(CA=700000, EAD=100000),     # Outlier sur CA
]

df = spark.createDataFrame(data)

# Instancier la classe avec le DataFrame
dq_pyspark = DataQualityPySpark(df)

from pyspark.sql import SparkSession

# Configurer une session Spark avec des ressources spécifiques
spark = SparkSession.builder \
    .appName("NomDeLApplication") \
    .config("spark.executor.memory", "4g") \   # Mémoire par exécuteur
    .config("spark.executor.cores", "2") \     # Nombre de cœurs par exécuteur
    .config("spark.driver.memory", "2g") \     # Mémoire pour le driver
    .config("spark.num.executors", "4") \      # Nombre d'exécuteurs
    .getOrCreate()

# Vérifiez les paramètres alloués
print("Nombre d'exécuteurs:", spark.sparkContext._conf.get("spark.num.executors"))
print("Mémoire par exécuteur:", spark.sparkContext._conf.get("spark.executor.memory"))
print("Cœurs par exécuteur:", spark.sparkContext._conf.get("spark.executor.cores"))
print("Mémoire du driver:", spark.sparkContext._conf.get("spark.driver.memory"))

# Testez avec un DataFrame
data = [("Alice", 34), ("Bob", 45), ("Catherine", 29)]
df = spark.createDataFrame(data, ["Nom", "Âge"])
df.show()

# Arrêtez la session Spark une fois le travail terminé
spark.stop()

