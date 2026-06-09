import unittest
from unittest.mock import patch, Mock
from utils.extract import extract_data

class TestExtract(unittest.TestCase):

    @patch("utils.extract.requests.Session")
    def test_extract_data_success(self, mock_session_class):
        # 1. Bikin objek Response palsu
        mock_response = Mock()
        mock_response.status_code = 200
        # Pakai str murni untuk menghindari error BeautifulSoup Dammit
        mock_response.text = str('''
        <div class="collection-card">
            <h3 class="product-title">Jaket Hacker</h3>
            <span class="price">Rp 500.000</span>
            <p>Rating: 5.0 / 5</p>
        </div>
        <li class="page-item current">1 of 1</li>
        ''')
        
        # 2. Bikin objek Session palsu yang mengembalikan respon palsu saat get() dipanggil
        mock_session_instance = Mock()
        mock_session_instance.get.return_value = mock_response
        
        # 3. Setup agar 'with requests.Session() as session' memakai instance palsu ini
        mock_session_class.return_value.__enter__.return_value = mock_session_instance

        # 4. Eksekusi
        result = extract_data()

        # 5. Validasi
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['Title'], 'Jaket Hacker')

    @patch("utils.extract.requests.Session")
    def test_extract_data_mentok_404(self, mock_session_class):
        # 1. Bikin objek Response 404
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.text = "" # Beri string kosong agar aman
        
        # 2. Bikin objek Session
        mock_session_instance = Mock()
        mock_session_instance.get.return_value = mock_response
        
        # 3. Setup Context Manager (__enter__)
        mock_session_class.return_value.__enter__.return_value = mock_session_instance
        
        # 4. Eksekusi & Validasi
        result = extract_data()
        self.assertEqual(result, [])

if __name__ == "__main__":
    unittest.main()