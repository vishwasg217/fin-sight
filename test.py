import json
import unittest
import os
from tqdm import tqdm
from dotenv import load_dotenv

from src.company_overview import company_overview
from src.income_statement import income_statement
from src.ticker_search import get_companies , get_ticker
from src.rag.ingestion import Ingestion
from src.rag.retrieval import Retrieve

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
        path_or_url = ["data/streamlit/from_streamlit.pdf", "https://d18rn0p25nwr6d.cloudfront.net/CIK-0000320193/b4266e40-1de6-4a34-9dfb-8632b8bd57e0.pdf"]

        for path in path_or_url:
            with self.subTest(path=path):
                try:
                    ingestion_instance = Ingestion(path_or_url=path)
                    ingestion_instance.extract()
                    logger.info(f"Extraction successful")
                except Exception as e:
                    self.fail(f"extract() raised an exception for {path}: {e}")    

    def test_get_documents(self):
        with self.subTest():
            path_or_url = "https://d18rn0p25nwr6d.cloudfront.net/CIK-0000320193/b4266e40-1de6-4a34-9dfb-8632b8bd57e0.pdf"
            ingestion_instance = Ingestion(path_or_url=path_or_url)
            ingestion_instance.extract()
            docs = ingestion_instance.get_documents()
            for doc in docs[:5]:
                logger.info(f"Metadata: {doc.metadata}\n\nContent: {doc.page_content}")

    
    def test_get_mapped_sections(self):
        with self.subTest():
            path_or_url = "https://d18rn0p25nwr6d.cloudfront.net/CIK-0000320193/b4266e40-1de6-4a34-9dfb-8632b8bd57e0.pdf"
            ingestion_instance = Ingestion(path_or_url=path_or_url)
            ingestion_instance.extract()
            mapped_sections = ingestion_instance.get_mapped_sections()

            for k, v in mapped_sections.items():
                logger.info(f"{k}: {v}")

    def test_add_item_metadata(self):
        with self.subTest():
            path_or_url = "https://d18rn0p25nwr6d.cloudfront.net/CIK-0000320193/b4266e40-1de6-4a34-9dfb-8632b8bd57e0.pdf"
            ingestion_instance = Ingestion(path_or_url=path_or_url)
            ingestion_instance.extract()
            documents = ingestion_instance.get_documents()
            mapped_sections = ingestion_instance.get_mapped_sections()
            items = ingestion_instance.add_item_metadata(documents, mapped_sections)

            for item in items[:5]:
                logger.info(item)

    def test_ingest(self):
        with self.subTest():
            path_or_url = "https://d18rn0p25nwr6d.cloudfront.net/CIK-0000320193/b4266e40-1de6-4a34-9dfb-8632b8bd57e0.pdf"
            ingestion_instance = Ingestion(path_or_url=path_or_url)
            chunks = ingestion_instance.ingest()

            for chunk in chunks[:5]:
                logger.info(chunk)

class TestRetrieve(unittest.TestCase):

    def test_convert_chunks_to_nodes(self):
        with self.subTest():
            path = "data/test_data/test_retrieval_microsoft.json"
            with open(path, "r") as f:
                chunks = json.load(f)

            retrieve_obj = Retrieve(chunks)
            nodes = retrieve_obj.convert_chunks_to_nodes()
            for node in nodes[:5]:
                logger.info(node)
        

    def test_get_vector_index_engine(self):
        with self.subTest():
            path = "data/test_data/test_retrieval_microsoft.json"
            with open(path, "r") as f:
                chunks = json.load(f)

            retrieve_obj = Retrieve(chunks)
            nodes = retrieve_obj.convert_chunks_to_nodes()
            engine = retrieve_obj.get_vector_index_engine(nodes)

            self.assertIsNotNone(engine, "get_vector_index_engine() returned None")

    def test_get_sub_question_query_engine(self):
        with self.subTest():
            path = "data/test_data/test_retrieval_microsoft.json"
            with open(path, "r") as f:
                chunks = json.load(f)

            retrieve_obj = Retrieve(chunks)
            nodes = retrieve_obj.convert_chunks_to_nodes()
            engine = retrieve_obj.get_vector_index_engine(nodes)
            sub_question_query_engine = retrieve_obj.get_sub_question_query_engine(engine)

            self.assertIsNotNone(sub_question_query_engine, "get_sub_question_query_engine() returned None")


    def test_engine(self):
        with self.subTest():
            path = "data/test_data/test_retrieval_microsoft.json"
            with open(path, "r") as f:
                chunks = json.load(f)

            retrieve_obj = Retrieve(chunks)
            engine = retrieve_obj.engine()

            self.assertIsNotNone(engine, "engine() returned None")


    


if __name__ == '__main__':
    unittest.main()

# command to run tests:
# python -m unittest test.py -k function_name