# Récupération des données depuis le dossier
dataframes = Data.retrieve_data(folder_path_n)

# Initialisation des résultats pour PD et LGD
results = {
    'pd': {
        'missing_values_rates': pd.DataFrame(),
        'outlier_rates': pd.DataFrame(),
        'duplicates': pd.DataFrame(),
        'nb_duplicates': 0,
    },
    'lgd': {
        'missing_values_rates': pd.DataFrame(),
        'outlier_rates': pd.DataFrame(),
        'duplicates': pd.DataFrame(),
        'nb_duplicates': 0,
    }
}

# Parcours des clés et classification dans les résultats
for key, df in dataframes.items():
    key_lower = key.lower()
    category = 'pd' if 'pd' in key_lower else 'lgd' if 'lgd' in key_lower else None

    if category:
        if 'missing_values_rates' in key_lower:
            results[category]['missing_values_rates'] = df
        elif 'outlier_rates' in key_lower:
            results[category]['outlier_rates'] = df
        elif 'duplicates' in key_lower:
            results[category]['duplicates'] = df
            results[category]['nb_duplicates'] = df.shape[0]

# Accès aux résultats
missing_values_rates_pd_df = results['pd']['missing_values_rates']
outlier_rates_pd_df = results['pd']['outlier_rates']
duplicates_pd_df = results['pd']['duplicates']
nb_duplicates_pd = results['pd']['nb_duplicates']

missing_values_rates_lgd_df = results['lgd']['missing_values_rates']
outlier_rates_lgd_df = results['lgd']['outlier_rates']
duplicates_lgd_df = results['lgd']['duplicates']
nb_duplicates_lgd = results['lgd']['nb_duplicates']
