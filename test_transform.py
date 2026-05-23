import unittest
import pandas as pd
from utils.transform import transform_data

class TestTransform(unittest.TestCase):
    def test_transform_data(self):
        # Create a simple dataframe for testing
        data = {
            'Title': ['Product 1', 'Product 2'],
            'Price': ['$10', '$20'],
            'Rating': ['⭐ 4.5 / 5', '⭐ 3.5 / 5'],
            'Colors': ['3 Colors', '5 Colors'],
            'Size': ['M', 'L'],
            'Gender': ['Male', 'Female']
        }
        df = pd.DataFrame(data)

        # Apply the transformation
        transformed_df = transform_data(df)

        # Test if the 'Price' is transformed correctly
        self.assertTrue('Price' in transformed_df.columns)
        self.assertEqual(transformed_df['Price'][0], 160000)

        # Test if 'Rating' has been converted to a float
        self.assertEqual(transformed_df['Rating'][0], 4.5)

if __name__ == '__main__':
    unittest.main()
