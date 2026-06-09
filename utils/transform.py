import pandas as pd
import logging

def transform_data(raw_data: list) -> pd.DataFrame:
    if not raw_data:
        logging.warning("Data mentah kosong. Transformasi dibatalkan.")
        return pd.DataFrame()

    try:
        df = pd.DataFrame(raw_data).drop_duplicates()
        logging.info(f"Mulai transformasi. Data awal: {len(df)} baris.")

        # 1. Filter Data Kotor (Sangat dipadatkan dengan isin & dropna)
        # Kumpulkan semua nilai "kotor" ke dalam satu list
        dirty_vals = ["Unknown Product", "Invalid Rating / 5", "Not Rated", "Price Unavailable"]
        # Hapus baris yang mengandung dirty_vals di kolom mana pun, LALU hapus yang nilainya NaN
        df = df[~df.isin(dirty_vals).any(axis=1)].dropna(subset=['Title', 'Price', 'Rating'])

        # 2. Konversi Tipe Data & Ekstraksi Teks (Chaining yang rapi)
        if 'Rating' in df.columns:
            # expand=False memastikan hasil extract() adalah Series 1D, bukan DataFrame
            df['Rating'] = df['Rating'].astype(str).str.extract(r'([\d.]+)', expand=False).astype(float)
            
        if 'Price' in df.columns:
            # Bersihkan teks -> Ubah ke Numerik -> Kali 16.000 -> Isi kosong dengan 0 -> Jadikan integer
            clean_p = df['Price'].astype(str).str.replace(r'[^\d.]', '', regex=True)
            df['Price'] = pd.to_numeric(clean_p, errors='coerce').fillna(0).mul(16000).astype(int)

        if 'Colors' in df.columns:
            df['Colors'] = df['Colors'].astype(str).str.extract(r'(\d+)', expand=False).fillna(0).astype(int)

        # 3. Size & Gender (Potong prefix dengan pemisah titik dua ': ')
        # Mengubah "Size: M" menjadi "M" langsung pakai fungsi split
        for col in ['Size', 'Gender']:
            if col in df.columns:
                df[col] = df[col].astype(str).str.split(': ').str[-1].str.strip()

        # 4. Filter & Susun Urutan Kolom Dinamis
        target_cols = ['Title', 'Price', 'Rating', 'Colors', 'Size', 'Gender', 'Timestamp']
        final_cols = [c for c in target_cols if c in df.columns]

        logging.info(f"Transformasi sukses. Data bersih: {len(df)} baris.")
        return df[final_cols]

    except Exception as e:
        logging.error(f"Terjadi kesalahan fatal pada transformasi: {e}")
        return pd.DataFrame()