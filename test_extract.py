import unittest
from unittest.mock import patch, MagicMock
from utils.extract import scrape_product, extract_product_data, fetching_content
import requests
from bs4 import BeautifulSoup
import pandas as pd

class TestExtract(unittest.TestCase):

    @patch('utils.extract.requests.get')
    def test_fetching_content_success(self, mock_get):
        # Mocking a successful response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b"<html>Mocked</html>"
        mock_get.return_value = mock_response

        url = "https://fashion-studio.dicoding.dev/"
        result = fetching_content(url)
        self.assertEqual(result, b"<html>Mocked</html>")

    @patch('utils.extract.requests.get')
    def test_fetching_content_error(self, mock_get):
        # Mocking an error when making a request
        mock_get.side_effect = requests.exceptions.RequestException("Connection Error")
        result = fetching_content("https://badurl.com")
        self.assertIsNone(result)

    def test_extract_product_data(self):
        # HTML example for extracting product data
        html = """
        <div class="collection-card">
            <h3 class="product-title">Test Product</h3>
            <span class="price">$10</span>
            <p>Rating: 4.5 / 5</p>
            <p>3 Colors</p>
            <p>Size: M</p>
            <p>Gender: Male</p>
        </div>
        """
        # Parsing HTML and passing it to extract_product_data
        soup = BeautifulSoup(html, "html.parser")
        card = soup.find("div", class_="collection-card")
        result = extract_product_data(card)
        
        # Check if the extracted data matches expected values
        self.assertEqual(result["Title"], "Test Product")
        self.assertEqual(result["Price"], "$10")
        self.assertEqual(result["Rating"], "4.5 / 5")
        self.assertEqual(result["Colors"], "3")  # Expecting "3" instead of "3 Colors"
        self.assertEqual(result["Size"], "M")
        self.assertEqual(result["Gender"], "Male")

    @patch("utils.extract.fetching_content")
    @patch("utils.extract.extract_product_data")
    def test_scrape_product(self, mock_extract, mock_fetch):
        # Simulate the behavior of scraping
        mock_fetch.return_value = "<html><body><div class='collection-card'>Test Product</div></body></html>"
        mock_extract.return_value = {
            "Title": "Test Product",
            "Price": "$100",
            "Rating": "4.5 / 5",
            "Colors": "3",
            "Size": "M",
            "Gender": "Male",
            "Timestamp": "2025-05-06T12:00:00"
        }

        page_url = "https://fashion-studio.dicoding.dev/page{}"
        result_df = scrape_product("https://fashion-studio.dicoding.dev/", page_url, 1, 1)

        # Check if the result is a DataFrame and contains the expected data
        self.assertIsInstance(result_df, pd.DataFrame)
        self.assertEqual(result_df.shape[0], 1)  # Ensure only 1 product data is scraped
        self.assertIn("Title", result_df.columns)
        self.assertEqual(result_df["Title"].iloc[0], "Test Product")  # Validate the title

if __name__ == '__main__':
    unittest.main()
