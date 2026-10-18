import unittest
import pandas as pd

from data_utils import prepare_data


class TestSalesAnalytics(unittest.TestCase):
    def test_revenue_calculation(self):
        df = pd.DataFrame({
            "date": ["2026-01-01"],
            "product": ["Keyboard"],
            "category": ["Accessories"],
            "region": ["North"],
            "quantity": [2],
            "unit_price": [50],
        })
        result = prepare_data(df)
        self.assertEqual(result.iloc[0]["revenue"], 100)
        self.assertEqual(result.iloc[0]["month"], "2026-01")

    def test_invalid_rows_are_removed(self):
        df = pd.DataFrame({
            "date": ["2026-01-01", "invalid", "2026-01-03"],
            "product": ["Mouse", "Keyboard", "   "],
            "category": ["Accessories", "Accessories", "Accessories"],
            "region": ["North", "South", "West"],
            "quantity": [2, 1, 1],
            "unit_price": [20, 50, 10],
        })
        result = prepare_data(df)
        self.assertEqual(len(result), 1)
        self.assertEqual(result.iloc[0]["product"], "Mouse")

    def test_column_names_are_normalized(self):
        df = pd.DataFrame({
            " Date ": ["2026-01-01"],
            "Product": ["Mouse"],
            "Category": ["Accessories"],
            "Region": ["North"],
            "Quantity": [2],
            "Unit Price": [20],
        })
        result = prepare_data(df)
        self.assertEqual(result.iloc[0]["revenue"], 40)

    def test_duplicate_normalized_columns_raise_error(self):
        df = pd.DataFrame([["2026-01-01", "Mouse"]], columns=["Product", " product "])
        with self.assertRaisesRegex(ValueError, "Duplicate column names"):
            prepare_data(df)

    def test_missing_column_raises_error(self):
        df = pd.DataFrame({"date": ["2026-01-01"], "product": ["Mouse"]})
        with self.assertRaisesRegex(ValueError, "Missing required columns"):
            prepare_data(df)


if __name__ == "__main__":
    unittest.main()
