import requests, logging, time
from bs4 import BeautifulSoup
from datetime import datetime

def extract_data(base_url: str = "https://fashion-studio.dicoding.dev", delay: int = 1, max_retries: int = 3) -> list:
    raw_data, page, ts = [], 1, datetime.now().isoformat()
    logging.info(f"Memulai ekstraksi dari {base_url}...")

    with requests.Session() as session:  # Gunakan Session agar koneksi lebih efisien
        while True:
            url = f"{base_url}/page{page}" if page > 1 else base_url
            
            # --- Jaringan & Error Handling ---
            for _ in range(max_retries):
                try:
                    res = session.get(url, timeout=10)
                    if res.status_code == 404: break
                    res.raise_for_status()
                    break 
                except requests.RequestException:
                    time.sleep(delay)
            else:
                logging.error(f"Gagal mengambil hal {page}. Berhenti."); break
            
            if res.status_code == 404: break

            # --- Parsing HTML ---
            soup = BeautifulSoup(res.text, 'html.parser')
            if not (products := soup.find_all('div', class_='collection-card')): break
            
            # --- Ekstraksi Data (Sangat Dipadatkan) ---
            for i in products:
                # Helper function singkat untuk mencari teks spesifik di elemen <p>
                p_texts = [p.text.strip() for p in i.find_all('p')]
                get_p = lambda kw: next((t for t in p_texts if kw in t), None)
                
                raw_data.append({
                    'Title': el.text.strip() if (el := i.find('h3', class_='product-title')) else None,
                    'Price': el.text.strip() if (el := i.find('span', class_='price')) else None,
                    'Rating': get_p('Rating:'), 'Colors': get_p('Colors'),
                    'Size': get_p('Size:'), 'Gender': get_p('Gender:'), 'Timestamp': ts
                })
                
            logging.info(f"Hal {page} selesai. Total: {len(raw_data)}")
            
            # --- Cek Kondisi Berhenti ---
            curr_info = soup.find('li', class_='page-item current')
            nxt = soup.find('li', class_='page-item next')
            
            if (curr_info and 'of' in curr_info.text and len(set(curr_info.text.split('of'))) == 1) or \
               (not nxt or 'disabled' in nxt.get('class', [])):
                break
                
            page += 1; time.sleep(delay)
            
    logging.info(f"Selesai! {len(raw_data)} data berhasil diekstrak.")
    return raw_data