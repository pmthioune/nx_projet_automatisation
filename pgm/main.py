import sys


def main(id_datapack, name_datapack, start_date, end_date, indicateurs):
    print(f"📌 Exécution du programme pour : {name_datapack}")
    print(f"➡️ ID Datapack : {id_datapack}")
    print(f"📅 Période : {start_date} → {end_date}")
    print(f"📊 Indicateurs sélectionnés : {', '.join(indicateurs)}")

    # 🔹 Simulation de calculs
    for i in range(5):
        print(f"🔄 Traitement {i + 1}/5 en cours...")
        sys.stdout.flush()  # ⚠️ Nécessaire pour que Dash capte l'avancement
        time.sleep(2)

    print("✅ Traitement terminé !")


if __name__ == "__main__":
    args = sys.argv[1:]  # Récupérer les arguments depuis Dash
    id_datapack = int(args[0])
    name_datapack = args[1]
    start_date = args[2]
    end_date = args[3]
    indicateurs = args[4:]

    main(id_datapack, name_datapack, start_date, end_date, indicateurs)
