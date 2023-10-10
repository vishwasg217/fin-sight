import sys
from pathlib import Path
script_dir = Path(__file__).resolve().parent
project_root = script_dir.parent
sys.path.append(str(project_root))

import camelot
import tabula
import pandas as pd
from llama_index import Document, SummaryIndex

# https://en.wikipedia.org/wiki/The_World%27s_Billionaires
from llama_index import VectorStoreIndex, ServiceContext, LLMPredictor
from llama_index.query_engine import PandasQueryEngine, RetrieverQueryEngine
from llama_index.retrievers import RecursiveRetriever
from llama_index.schema import IndexNode
from llama_index.llms import OpenAI
from llama_index import download_loader

from pathlib import Path
from typing import List

from src.utils import get_model

PDFReader = download_loader("PDFReader")
loader = PDFReader()
pdf =  loader.load_data(file=Path("data/apple/AAPL.pdf"))



# print(pdf)

pages = ['32', '33', '34', '35', '36']
table_titles = ['Consolidated Statements of Operations', 'Consolidated Statements of Comprehensive Income', 'Consolidated Balance Sheets',  'Consolidated Statements of Shareholders’ Equity', 'Consolidated Statements of Cash Flows']

table1 = tabula.read_pdf("data/apple/AAPL.pdf",output_format="dataframe", pages="32")
print(type(table1))
print(len(table1))
print(pd.DataFrame(table1))


# def get_tables(path, pages, table_titles):
#     tables = {}
#     for i, page in enumerate(pages):
#         table = tabula.read_pdf(path, pages=f"{page}")
        
#         tables[table_titles[i]] = table

#     return tables


# tables = get_tables("data/apple/AAPL.pdf", pages, table_titles)

# # iterate through json object
# for key, value in tables.items():
#     print("-"*30)
#     print("Title: ",key)
#     print(value)


