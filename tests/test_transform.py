import pandas as pd
from utils.transform import transform_data

def test_transform_data_sukses():
    # Simulasi data mentah
    raw_data = [
        {'Title': 'Baju Keren', 'Price': 'Rp 100.000', 'Rating': 'Rating: 4.5 / 5', 'Colors': '2 Colors', 'Size': 'Size: M', 'Gender': 'Gender: Men', 'Timestamp': '2026-01-01'},
        {'Title': 'Unknown Product', 'Price': 'Price Unavailable', 'Rating': 'Not Rated', 'Colors': None, 'Size': None, 'Gender': None, 'Timestamp': '2026-01-01'}
    ]
    
    df = transform_data(raw_data)
    
    assert not df.empty
    assert len(df) == 1 
    
    # PERBAIKAN: Angka diubah menjadi 1600000 agar sesuai dengan hitungan Pandas (100.0 * 16000)
    assert df.iloc[0]['Price'] == 1600000 
    assert df.iloc[0]['Rating'] == 4.5
    assert df.iloc[0]['Size'] == 'M'

def test_transform_data_kosong():
    df = transform_data([])
    assert df.empty