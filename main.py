import logging
import pandas as pd
from pathlib import Path
from utils.extract import extract_data
from utils.transform import transform_data
# Tambahkan import load_to_google_sheets
from utils.load import load_to_csv, load_to_postgresql, load_to_google_sheets

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def run_etl():
    logging.info("=== ETL PIPELINE DIMULAI ===")
    
    # Konfigurasi Path & DB
    base_dir = Path(__file__).parent
    csv_path = base_dir / 'product.csv'
    db_url = "postgresql://developer:supersecretpassword@localhost:5432/product"
    
    # Konfigurasi Google Sheets
    g_sheets_url = "https://docs.google.com/spreadsheets/d/18up0uMVW_t_r-913c0Go9tM0qUZEcOxaTVrqnWBzFMI/edit?usp=sharing"
    g_sheets_creds = str(base_dir / 'google-sheets-api.json')
    
    try:
        # 1. EXTRACT (Gabung assignment & validasi pakai Walrus Operator ':=')
        if not (raw_data := extract_data()):
            return logging.error("[ETL] Batal: Data mentah gagal diekstrak.")

        # 2. TRANSFORM
        if (df := transform_data(raw_data)).empty:
            return logging.error("[ETL] Batal: DataFrame hasil transformasi kosong.")

        # Konversi Timestamp jika kolom tersedia
        if 'Timestamp' in df.columns:
            df['Timestamp'] = pd.to_datetime(df['Timestamp'])

        # 3. LOAD
        load_to_csv(df, str(csv_path))
        load_to_postgresql(df, "product_data", db_url)
        
        # --- Eksekusi Load ke Google Sheets ---
        # Bikin salinan khusus untuk Google Sheets dan ubah Timestamp menjadi teks
        df_gsheets = df.copy()
        if 'Timestamp' in df_gsheets.columns:
            df_gsheets['Timestamp'] = df_gsheets['Timestamp'].astype(str)
            
        load_to_google_sheets(df_gsheets, g_sheets_url, g_sheets_creds)
        
        logging.info("=== ETL PIPELINE SELESAI DENGAN SUKSES ===")
        
    except Exception as e:
        logging.error(f"[ETL] Kegagalan fatal pada pipeline: {e}")

if __name__ == "__main__":
    run_etl()