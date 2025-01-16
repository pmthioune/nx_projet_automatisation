def process_indicators(instances, rating_system, method_name):
    """
    Applique une méthode donnée (`get_indicator` ou `generate_indicator`) sur une liste d'instances.

    Args:
        instances (list): Liste des instances sur lesquelles appliquer la méthode.
        rating_system (str): Nom du système de notation.
        method_name (str): Nom de la méthode à exécuter ('get_indicator' ou 'generate_indicator').
    """
    for instance in instances:
        try:
            # Vérifier si la méthode existe dans l'instance
            method = getattr(instance[rating_system], method_name, None)
            if method and callable(method):
                method()  # Appeler la méthode
                print(f"{method_name} executed successfully for {instance}.")
            else:
                print(f"Method '{method_name}' not found or not callable for {instance}.")
        except Exception as e:
            print(f"Error executing '{method_name}' for {instance}: {e}")
