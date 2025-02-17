import pandas as pd
import os

def load_data(file_path):
    if os.path.exists(file_path):
        return pd.read_csv(file_path)
    else:
        raise FileNotFoundError(f"File not found: {file_path}")




