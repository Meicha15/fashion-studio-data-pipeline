import unittest
from unittest.mock import patch, MagicMock
from utils.load import store_to_postgre, store_to_google_sheets, store_to_csv
import pandas as pd

class TestLoad(unittest.TestCase):

    @patch('utils.load.create_engine')
    @patch('pandas.DataFrame.to_sql')
    def test_store_to_postgre_failure(self, mock_to_sql, mock_create_engine):
        """Uji kegagalan saat menyimpan data ke PostgreSQL."""
        mock_connection = MagicMock()
        mock_create_engine.return_value.connect.return_value = mock_connection
        mock_to_sql.side_effect = Exception("Database connection error")

        data = {'Title': ['Product 1'], 'Price': [160000], 'Rating': [4.5], 'Colors': [3], 'Size': ['M'], 'Gender': ['Male']}
        df = pd.DataFrame(data)

        # Menangkap exception yang dilemparkan dan memverifikasi pesan error
        with self.assertRaises(Exception) as context:
            store_to_postgre(df, "postgresql://localhost:5432/testdb")

        # Memastikan pesan exception sesuai dengan yang dilemparkan oleh kode
        self.assertEqual(str(context.exception), "Error in saving to PostgreSQL: Database connection error")
        
        # Memastikan bahwa `to_sql` dipanggil sekali, meskipun terjadi error
        mock_to_sql.assert_called_once()

        # Memastikan bahwa `create_engine` dipanggil dengan URL yang benar
        mock_create_engine.assert_called_once_with("postgresql://localhost:5432/testdb")
    
    @patch('utils.load.build')
    @patch('pandas.DataFrame.to_sql')
    def test_store_to_google_sheets(self, mock_to_sql, mock_build):
        """Uji penyimpanan data ke Google Sheets"""
        mock_service = MagicMock()
        mock_sheets = MagicMock()
        mock_service.spreadsheets.return_value = mock_sheets
        mock_build.return_value = mock_service

        data = {'Title': ['Product 1'], 'Price': [160000], 'Rating': [4.5], 'Colors': [3], 'Size': ['M'], 'Gender': ['Male']}
        df = pd.DataFrame(data)

        SPREADSHEET_ID = '1a20oW2CHLPMPpFtIJGZk5Y-ERt63aCXymBOhZ6xBb6g'
        RANGE_NAME = 'Sheet1!A1:G'
        
        # Memanggil fungsi untuk menyimpan data ke Google Sheets
        store_to_google_sheets(df, SPREADSHEET_ID, RANGE_NAME)

        # Memastikan bahwa method `values().update` pada mock telah dipanggil sekali
        mock_service.spreadsheets.return_value.values().update.assert_called_once()

    @patch('pandas.DataFrame.to_csv')
    def test_store_to_csv(self, mock_to_csv):
        """Uji penyimpanan data ke file CSV"""
        data = {'Title': ['Product 1'], 'Price': [160000], 'Rating': [4.5], 'Colors': [3], 'Size': ['M'], 'Gender': ['Male']}
        df = pd.DataFrame(data)

        file_path = "products_data.csv"
        
        # Memanggil fungsi untuk menyimpan data ke CSV
        store_to_csv(df, file_path)

        # Memastikan bahwa method `to_csv` pada mock telah dipanggil sekali dengan argumen yang benar
        mock_to_csv.assert_called_once_with(file_path, index=False)

if __name__ == '__main__':
    unittest.main()