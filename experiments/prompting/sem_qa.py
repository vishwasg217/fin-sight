import sys
from pathlib import Path
script_dir = Path(__file__).resolve().parent
project_root = script_dir.parent
sys.path.append(str(project_root))


import pandas as pd
from llama_index import SimpleDirectoryReader
from platform import node
from llama_index.node_parser import UnstructuredElementNodeParser, SimpleNodeParser
from llama_index.retrievers import RecursiveRetriever
from llama_index.query_engine import RetrieverQueryEngine
from llama_index import VectorStoreIndex
from llama_index.tools import QueryEngineTool, ToolMetadata
from llama_index.query_engine import SubQuestionQueryEngine
from llama_index import ServiceContext
from llama_index.llms import OpenAI

import nest_asyncio

nest_asyncio.apply()

import streamlit as st
import os

OPENAI_API_KEY = st.secrets["openai_api_key"]
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)
pd.set_option("display.max_colwidth", None)


company = input("Enter company name: ")

# load pdfs
if company == "apple":
    reader = SimpleDirectoryReader(
        input_files=["data/apple/AAPL.pdf"]
    )
    docs = reader.load_data()


elif company =="meta":
    reader = SimpleDirectoryReader(
        input_files=["data/meta/meta.pdf"]
    )

    docs = reader.load_data()


# node_parser = UnstructuredElementNodeParser()
node_parser = SimpleNodeParser()

nodes = node_parser.get_nodes_from_documents(docs, show_progress=True)
# base_nodes, node_mappings = node_parser.get_base_nodes_and_mappings(nodes)


vector_index = VectorStoreIndex(nodes)
vector_retriever = vector_index.as_retriever(similarity_top_k=3)
query_engine = vector_index.as_query_engine(similarity_top_k=3)

# recursive_retriever = RecursiveRetriever(
#     "vector",
#     retriever_dict={"vector": vector_retriever},
#     node_dict=aapl_node_mappings,
#     verbose=True,
# )
# query_engine = RetrieverQueryEngine.from_args(recursive_retriever)


llm = OpenAI(model="gpt-3.5-turbo", api_key=OPENAI_API_KEY)
service_context = ServiceContext.from_defaults(llm=llm)

query_engine_tool = [
    QueryEngineTool(
        query_engine=query_engine,
        metadata=ToolMetadata(
            name = company,
            description=f"provides information about {company} financials for the year 2022",
        ),
    )
]

sub_query_engine = SubQuestionQueryEngine.from_defaults(
    query_engine_tools=query_engine_tool,
    service_context=service_context,
    use_async=True
)

query = """
You are tasked with generating performance_highlights insight about the company for the Fiscal Year Highlights section from the annual report of the company:

Given below is the output format, which has the subsections.
Must use bullet points.
Always use $ symbol for money values, and round it off to millions or billions accordingly

Incase you don't have enough info you can just write: No information available
---
{'performance_highlights': 'Key performance and financial stats over the fiscal year. Provide the Revenue Growth, Net Profit Margin, Market Share expansion, Cost Savings and Efficiency, Dividend Distribution'}

"""

query = ""

while query != "exit":
    query = input("ENTER QUERY: ")
    response = sub_query_engine.query(query)
    print("-"*50)
    print(str(response))
    print("-"*50)

{
  "Business": "Item 1: ",
  "Risk Factors": "Item 1A, Item 7A",
  "MD&A": "Item 7",
  "Financial Statements": "Item 8",
  "Management's Report on Internal Control Over Financial Reporting": "Item 9A",
  "Report of Independent Registered Public Accounting Firm": "Item 8",
  "Corporate Governance": "Item 10"
}

