import argparse
from datetime import datetime

def main(id_datapack, name_datapack, start_date, end_date):
    """
    Fonction principale qui traite les paramètres fournis.
    """
    # Conversion des dates en objets datetime (si nécessaire)
    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")

    # Afficher les paramètres reçus
    print(f"ID du datapack : {id_datapack}")
    print(f"Nom du datapack : {name_datapack}")
    print(f"Date de début d'extraction : {start_date}")
    print(f"Date de fin d'extraction : {end_date}")

    # Exemple de traitement
    print("\nTraitement en cours...")
    # Ajoutez votre logique métier ici
    print(f"Datapack '{name_datapack}' (ID : {id_datapack}) traité avec succès entre {start_date.date()} et {end_date.date()}.")

if __name__ == "__main__":
    # Initialisation d'argparse pour capturer les paramètres
    parser = argparse.ArgumentParser(description="Programme principal pour traiter les datapacks.")
    parser.add_argument("id_datapack", type=int, help="ID du datapack à traiter (entier).")
    parser.add_argument("name_datapack", type=str, help="Nom du datapack.")
    parser.add_argument("start_date", type=str, help="Date de début d'extraction (format YYYY-MM-DD).")
    parser.add_argument("end_date", type=str, help="Date de fin d'extraction (format YYYY-MM-DD).")

    # Parsing des arguments
    args = parser.parse_args()

    # Appel de la fonction principale avec les arguments
    main(args.id_datapack, args.name_datapack, args.start_date, args.end_date)
