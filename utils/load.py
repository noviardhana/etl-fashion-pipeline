import pandas as pd
import logging
from pathlib import Path
from sqlalchemy import create_engine
import gspread
from gspread_dataframe import set_with_dataframe

def load_to_csv(df: pd.DataFrame, file_path: str) -> None:
    if df.empty: return logging.warning("[CSV] DataFrame kosong! Load dibatalkan.")
    
    try:
        # Pathlib membuat folder otomatis dengan sintaks yang jauh lebih bersih dari os.makedirs
        Path(file_path).parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(file_path, index=False, date_format='%Y-%m-%d %H:%M:%S')
        logging.info(f"[CSV] Sukses! {len(df)} baris data disimpan ke: {file_path}")
    except Exception as e:
        logging.error(f"[CSV] Error saat menyimpan CSV: {e}")

def load_to_postgresql(df: pd.DataFrame, table_name: str, db_url: str) -> None:
    if df.empty: return logging.warning("[POSTGRES] DataFrame kosong! Load dibatalkan.")
    
    try:
        # create_engine langsung disisipkan ke dalam 'con'
        # Tambahan chunksize=1000 mencegah error batas maksimal parameter di PostgreSQL jika data raksasa
        df.to_sql(
            name=table_name, con=create_engine(db_url), 
            if_exists='replace', index=False, 
            method='multi', chunksize=1000
        )
        logging.info(f"[POSTGRES] Sukses! {len(df)} baris data masuk ke tabel '{table_name}'.")
    except Exception as e:
        # Menggabungkan blok try-except karena Exception menangkap sqlalchemy error & error biasa
        logging.error(f"[POSTGRES] Terjadi error database/sistem: {e}")

def load_to_google_sheets(df: pd.DataFrame, sheet_url: str, credentials_path: str) -> None:
    """Menyimpan DataFrame ke dalam Google Sheets."""
    logging.info(f"[G-SHEETS] Memulai proses load data ke Google Sheets...")

    if df.empty:
        return logging.warning("[G-SHEETS] DataFrame kosong! Load dibatalkan.")
    
    try:
        # Autentikasi pakai file json Service Account lu
        gc = gspread.service_account(filename=credentials_path)
        
        # Buka spreadsheet berdasarkan URL
        sh = gc.open_by_url(sheet_url)
        worksheet = sh.sheet1 # Mengambil sheet pertama (Sheet1)
        
        # Hapus data lama biar ke-replace secara rapi
        worksheet.clear()
        
        # Masukkan DataFrame ke dalam Google Sheets
        set_with_dataframe(worksheet, df)
        logging.info(f"[G-SHEETS] Sukses! {len(df)} baris data dimasukkan ke Google Sheets.")
        
    except Exception as e:
        logging.error(f"[G-SHEETS] Terjadi kesalahan: {e}")