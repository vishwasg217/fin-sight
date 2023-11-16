import json
from io import BytesIO
import unittest
import os
from tqdm import tqdm
from dotenv import load_dotenv

from src.company_overview import company_overview
from src.income_statement import income_statement
from src.ticker_search import get_companies , get_ticker
from src.rag.ingestion import Ingestion

load_dotenv(".env")
os.environ['OPENAI_API_KEY'] = os.getenv("OPENAI_API_KEY")
os.environ['AV_API_KEY'] = os.getenv("AV_API_KEY")

import logging
from logger_config import setup_logging
setup_logging()
logger = logging.getLogger(__name__)


class TestCompanyOverview(unittest.TestCase):

    def test_company_overview(self):

        from data.test_data.test_company_overview_data import test_cases
        for symbol in tqdm(test_cases):
            with self.subTest(symbol=symbol):
                try:
                    logger.info(f"Testing {symbol}")
                    result = company_overview(symbol)
                    logger.info(result)
                    print("-"*30)
                    self.assertIsNotNone(result, f"company_overview returned None for {symbol}")
                    self.assertNotIn('Error', result, f"Error found in company_overview result for {symbol}: {result.get('Error')}")
                except Exception as e:
                    self.fail(f"company_overview raised an exception for {symbol}: {e}")


class TestIncomeStatement(unittest.TestCase):

    def test_income_statement(self):

        with open("data/test_data/test_income_statement_data.json", "r") as f:
            test_cases = json.load(f)

        for test_case in tqdm(test_cases[2:3]):
            with self.subTest(symbol=test_case['symbol'], fields_to_include=test_case['fields_to_include']):
                try:
                    logger.info(f"Testing {test_case['symbol']}")
                    result = income_statement(test_case['symbol'], test_case['fields_to_include'])
                    logger.info(result)
                    print("-"*30)
                    self.assertIsNotNone(result, f"income_statement returned None for {test_case['symbol']}")
                    self.assertNotIn('Error', result, f"Error found in income_statement result for {test_case['symbol']}: {result.get('Error')}")
                except Exception as e:
                    self.fail(f"income_statement raised an exception for {test_case['symbol']}: {e}")

class TestTickerSearch(unittest.TestCase):

    def test_get_companies(self):
        with self.subTest():
            try:
                companies = get_companies()
                logger.info(companies[:10])
            except Exception as e:
                self.fail(e)

    def test_get_ticker_symbol(self):
        with open('data/test_data/test_ticker_symbol_data.json', 'r') as f:
            test_cases = json.load(f)

        for test_case in tqdm(test_cases):
            with self.subTest():
                try:
                    ticker = get_ticker(test_case['company_name'])
                    logger.info(ticker)
                    self.assertEqual(ticker, test_case['ticker_symbol'])

                    logger.info(ticker)
                except Exception as e:
                    self.fail(f"get_ticker() raised an exception for {test_case['company_name']}: {e}")

class TestIngestion(unittest.TestCase):

    def test_extract(self):
        pdf_file_path = "data/streamlit/from_streamlit.pdf"  # Replace with the actual file path

        with open(pdf_file_path, 'rb') as file:
            pdf = file.read()

        
        ingestion_instance = Ingestion(pdf)
        ingestion_instance.extract()

        self.assertIsNotNone(ingestion_instance.pdf)

if __name__ == '__main__':
    unittest.main()

# command to run tests:
# python -m unittest test.py -k function_name