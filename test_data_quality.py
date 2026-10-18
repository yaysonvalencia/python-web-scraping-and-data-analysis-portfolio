
import unittest
from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parent


class TestDataQuality(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.books = pd.read_csv(BASE_DIR / "week3_books.csv")
        cls.quotes = pd.read_csv(BASE_DIR / "quotes.csv")

    def test_book_record_count(self):
        """Verify expected source dataset size."""
        self.assertEqual(len(self.books), 105)

    def test_book_file_not_empty(self):
        """Verify book source contains records."""
        self.assertFalse(self.books.empty)

    def test_quotes_not_empty(self):
        """Verify scraped output contains records."""
        self.assertFalse(self.quotes.empty)

    def test_quote_record_count(self):
        """Verify saved quote sample size."""
        self.assertEqual(len(self.quotes), 40)

    def test_no_completely_empty_quote_rows(self):
        """Reject rows with no populated values."""
        self.assertFalse(
            self.quotes.isna().all(axis=1).any()
        )

    def test_no_duplicate_quote_rows(self):
        """Check for duplicate saved quote records."""
        self.assertEqual(
            self.quotes.duplicated().sum(), 0
        )


if __name__ == "__main__":
    unittest.main()
