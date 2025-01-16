def process_indicators(instances, rating_system):
    for instance in instances:
        instance[rating_system].get_indicator()

# Appel de la fonction
process_indicators(
    [
        ind1_instance,
        ind2_instance,
        ind3_instance,
        indő_instance,
        ind7_instance,
        ind8_instance,
        ind9_instance
    ],
    rating_system
)
