import pandas as pd

REQUIRED_COLUMNS = [
    "Tanggal",
    "Jumlah",
    "Harga",
    "Status Pembayaran"
]

def validate_data(df: pd.DataFrame):
    df = df.copy()

    # Memastikan kolom yang dibutuhkan ada
    for col in REQUIRED_COLUMNS:
        if col not in df.columns:
            df[col] = None
    
    df["error_reason"] = ""

    # Memvalidasi Jumlah
    df.loc[df["Jumlah"].isnull() | (df["Jumlah"] <= 0), "error_reason"] += "Jumlah tidak valid; "

    # Memvalidasi Harga
    df.loc[df["Harga"].isnull() | (df["Harga"] <= 0), "error_reason"] += "Harga tidak valid; "

    # Memvalidasi Tanggal
    df["Tanggal"] = pd.to_datetime(df["Tanggal"], errors="coerce")
    df.loc[df["Tanggal"].isnull(), "error_reason"] += "Tanggal tidak valid; "

    # Memvalidasi Status Pembayaran
    df.loc[df["Status Pembayaran"].isnull() | (df["Status Pembayaran"].astype(str).str.strip() == ""), "error_reason"] += "Status pembayaran kosong; "

    # Memisahkan Data
    df_error = df[df["error_reason"] != ""]
    df_valid = df[df["error_reason"] == ""].drop(columns=["error_reason"])

    return df_valid.reset_index(drop=True), df_error.reset_index(drop=True)