# 🛒 ETL Pipeline: Dicoding Fashion Studio

Pipeline ETL otomatis berbasis Python untuk melakukan web scraping, transformasi data, dan pemuatan data multi-target secara simultan dari situs sandbox Dicoding Fashion Studio.

---

## 🛠️ Tech Stack & Fitur
* **Extract:** `requests.Session` (HTTP Keep-Alive) & `BeautifulSoup` (Scraping dinamis + Auto-retry & 404 handler).
* **Transform:** `pandas` (Vectorization cleaning, Regex extractor, konversi kurs otomatis ke IDR).
* **Load:** Multi-target loading ke **CSV Lokal**, **PostgreSQL** (`SQLAlchemy`), dan **Google Sheets Live** (`gspread`).
* **QA/Testing:** `pytest` & `unittest.mock` dengan cakupan kode (**Test Coverage > 80%**).

---

## 📂 Struktur Proyek
```text
├── tests/              # Unit Testing (Extract, Transform, Load)
├── utils/              # Modul Inti ETL (extract.py, transform.py, load.py)
├── main.py             # Driver Utama Pipeline (Walrus Operator)
├── requirements.txt    # Dependensi Proyek
└── .gitignore          # Pengaman API Key & Data Cache
```

---

## ⚙️ Setup & Eksekusi

### 1. Instalasi
```bash
cd D:\Dicoding\submision_ETL
pip install -r requirements.txt
```

### 2. Konfigurasi Google Sheets API
1. Letakkan file kredensial di root folder dengan nama `google-sheets-api.json`.
2. Buka file tersebut, salin email pada properti `"client_email"`.
3. Buka Google Sheets target lu, klik **Share (Bagikan)**, lalu tambahkan email tersebut sebagai **Editor**.

### 3. Jalankan Pipeline
```bash
python3 main.py
```

---

## 🧪 Testing & Coverage

Jalankan perintah berikut di terminal untuk memvalidasi kode dan memeriksa persentase cakupan tes:

```bash
# Jalankan seluruh unit test
python3 -m pytest tests

# Jalankan test coverage & tampilkan laporan
coverage run -m pytest tests
coverage report -m
```

---
🔒 *Catatan: File `google-sheets-api.json`, `product.csv`, dan berkas database lokal otomatis diabaikan oleh `.gitignore` demi keamanan kredensial.*