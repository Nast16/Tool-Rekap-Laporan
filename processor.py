import os
import pandas as pd
from validator import validate_data

def proses_folder(folder_path):
    all_valid_data = []
    all_error_data = []

    files = get_data_files(folder_path)

    for file in files:
        df = load_data(file)
        if df in None:
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

def clean_and_normalize(df):
    df = df.copy()

    df.columns = [col.strip() for col in df.columns]

    column_mapping = {
        "tgl": "Tanggal",
        "tanggal": "Tanggal",
        "date": "Tanggal",

        "qty": "Jumlah",
        "jumlah": "Jumlah",
        "quantity": "Jumlah",

        "harga": "Harga",
        "price": "Harga",

        "status": "Status Pembayaran",
        "status pembayaran": "Status Pembayaran",
        "payment status": "Status Pembayaran"
    }

    rename_dict = {}
    for col in df.columns:
        key = col.lower()
        if key in column_mapping:
            rename_dict[col] = column_mapping[key]
    
    df = df.rename(columns=rename_dict)

    df = df.dropna(how="all")

    if "Jumlah" in df.columns:
        df["Jumlah"] = pd.to_numeric(df["Jumlah"], errors="coerce")
    
    if "Harga" in df.columns:
        df["Harga"] = (
            df["Harga"]
            .astype(str)
            .str.replace(",", "")
            .str.replace("Rp", "", regex=False)
            .str.strip()
        )
        df["Harga"] = pd.to_numeric(df["Harga"], errors="coerce")

    if "Status Pembayaran" in df.columns:
        df["Status Pembayaran"] = (
            df["Status Pembayaran"]
            .astype(str)
            .str.strip()
            .str.upper()
        )
        
    return df

def export_results(df_valid, df_error, output_path):
    valid_path = os.path.join(output_path, "laporan_final.xlsx")
    error_path = os.path.join(output_path, "data_error.xlsx")

    df_valid.to_excel(valid_path, index=False)
    df_error.to_excel(error_path, index=False)