import os
import pandas as pd
from validator import validate_data

def proses_folder(folder_path):
    all_valid_data = []
    all_error_data = []

    files = get_data_files(folder_path)

    for file in files:
        df = load_data(file)
        if ds in None:
            continue

        df = clean_and_normalize(df)

        df_valid, df_error = validate_data(df)

        all_valid_data.append(df_valid)
        all_error_data.append(df_error)
    
    final_valid_df = pd.concat(all_valid_data, ignore_index=True) if all_valid_data else pd.DataFrame()
    final_error_df = pd.concat(all_error_data, ignore_index=True) if all_error_data else pd.DataFrame()

    export_results(final_valid_df, final_error_df, folder_path)

    return{
        "total_valid": len(final_valid_df),
        "total_error": len(final_error_df)
    }

def get_data_files(folder_path):
    return [
        os.path.join(folder_path, f)
        for f in os.listdir(folder_path)
        if f.endswith((".xlsx", ".csv"))
    ]

def load_data(file_path):
    try:
        if file_path.endswith(".csv"):
            return pd.read_csv(file_path)
        else:
            return pd.read_excel(file_path)
    except Exception as e:
        print(f"Gagal load {file_path}: {e}")
        return None
