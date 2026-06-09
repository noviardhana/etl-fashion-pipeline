import pandas as pd
from unittest.mock import patch
from utils.load import load_to_csv, load_to_postgresql, load_to_google_sheets

# Bikin dummy DataFrame untuk dites
dummy_df = pd.DataFrame({'Title': ['Baju'], 'Price': [100000]})

@patch('utils.load.pd.DataFrame.to_csv')
@patch('utils.load.Path.mkdir')
def test_load_to_csv(mock_mkdir, mock_to_csv):
    load_to_csv(dummy_df, 'dummy/path.csv')
    
    # Pastikan fungsi bikin folder dan fungsi save ke csv dipanggil oleh kode lu
    mock_mkdir.assert_called()
    mock_to_csv.assert_called_once_with('dummy/path.csv', index=False, date_format='%Y-%m-%d %H:%M:%S')

def test_load_to_csv_kosong():
    # Ngetes kondisi DataFrame kosong
    assert load_to_csv(pd.DataFrame(), 'dummy.csv') is None

@patch('utils.load.pd.DataFrame.to_sql')
@patch('utils.load.create_engine')
def test_load_to_postgresql(mock_engine, mock_to_sql):
    load_to_postgresql(dummy_df, 'tabel_dummy', 'sqlite:///:memory:')
    
    # Pastikan engine DB dibuat dan to_sql dieksekusi
    mock_engine.assert_called_once()
    mock_to_sql.assert_called_once()

def test_load_to_postgresql_kosong():
    assert load_to_postgresql(pd.DataFrame(), 'tabel', 'url') is None

@patch('utils.load.gspread.service_account')
@patch('utils.load.set_with_dataframe')
def test_load_to_google_sheets(mock_set_df, mock_gspread):
    # Setup rantai mock untuk autentikasi dan memanggil worksheet
    mock_gc = mock_gspread.return_value
    mock_sh = mock_gc.open_by_url.return_value
    mock_worksheet = mock_sh.sheet1
    
    load_to_google_sheets(dummy_df, 'http://dummy.url', 'dummy.json')
    
    # Validasi bahwa fungsi bawaan gspread dan set_with_dataframe beneran dipanggil
    mock_gspread.assert_called_once_with(filename='dummy.json')
    mock_gc.open_by_url.assert_called_once_with('http://dummy.url')
    mock_worksheet.clear.assert_called_once()
    mock_set_df.assert_called_once_with(mock_worksheet, dummy_df)

def test_load_to_google_sheets_kosong():
    # Test kondisi df kosong agar tidak memicu eksekusi
    assert load_to_google_sheets(pd.DataFrame(), 'url', 'json') is None