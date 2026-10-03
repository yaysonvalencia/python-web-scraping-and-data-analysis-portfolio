"""Collect dynamically loaded quote text from a public scraping practice site."""

from pathlib import Path
import time

import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


OUTPUT_PATH = Path(__file__).parent / "quotes.csv"
TARGET_URL = "https://quotes.toscrape.com/scroll"


def collect_quotes(scroll_cycles: int = 3, wait_seconds: int = 2) -> pd.DataFrame:
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)
    try:
        driver.get(TARGET_URL)
        for _ in range(scroll_cycles):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(wait_seconds)

        records = []
        for element in driver.find_elements(By.CLASS_NAME, "quote"):
            records.append(
                {
                    "quote": element.find_element(By.CLASS_NAME, "text").text,
                    "author": element.find_element(By.CLASS_NAME, "author").text,
                }
            )
        return pd.DataFrame(records).drop_duplicates()
    finally:
        driver.quit()


if __name__ == "__main__":
    quotes = collect_quotes()
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    quotes.to_csv(OUTPUT_PATH, index=False)
    print(f"Exported {len(quotes)} records to {OUTPUT_PATH}")
