import unittest
import pandas as pd

from app import prepare_data


class TestSalesAnalytics(unittest.TestCase):

    def test_revenue_calculation(self):
        df = pd.DataFrame({
            "date": ["2026-01-01"],
            "product": ["Keyboard"],
            "category": ["Accessories"],
            "region": ["North"],
            "quantity": [2],
            "unit_price": [50]
        })

        result = prepare_data(df)

        self.assertEqual(result.iloc[0]["revenue"], 100)

    def test_invalid_rows_are_removed(self):
        df = pd.DataFrame({
            "date": ["2026-01-01", "invalid"],
            "product": ["Mouse", "Keyboard"],
            "category": ["Accessories", "Accessories"],
            "region": ["North", "South"],
            "quantity": [2, 1],
            "unit_price": [20, 50]
        })

        result = prepare_data(df)

        self.assertEqual(len(result), 1)

    def test_missing_column_raises_error(self):
        df = pd.DataFrame({
            "date": ["2026-01-01"],
            "product": ["Mouse"]
        })

        with self.assertRaises(ValueError):
            prepare_data(df)


if __name__ == "__main__":
    unittest.main()
