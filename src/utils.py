import sys
from pathlib import Path
script_dir = Path(__file__).resolve().parent
project_root = script_dir.parent
sys.path.append(str(project_root))


from langchain.vectorstores import Weaviate, Chroma, FAISS
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser

from dotenv import dotenv_values
import weaviate
from pypdf import PdfReader
import streamlit as st
import requests
import time

config = dotenv_values(".env")

OPENAI_API_KEY = config["OPENAI_API_KEY"]
WEAVIATE_URL = config["WEAVIATE_URL"]
WEAVIATE_API_KEY = config["WEAVIATE_API_KEY"]
AV_API_KEY = config["ALPHA_VANTAGE_API_KEY"]

def process_pdf(pdfs):
    docs = []
    text = ""
    for pdf in pdfs:
        file = PdfReader(pdf)
        for page in file.pages:
            text += str(page.extract_text())
        
        # docs.append(Document(page_content=text))

    text_splitter = CharacterTextSplitter(separator="\n",
    chunk_size=2000,
    chunk_overlap=300,
    length_function=len)
    # docs = text_splitter.split_documents(docs)
    docs = text_splitter.split_text(text)

    return docs


def vector_store(documents):
    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
    client = weaviate.Client(url=WEAVIATE_URL, auth_client_secret=weaviate.AuthApiKey(WEAVIATE_API_KEY))
    vectorstore = Weaviate.from_texts(documents, embeddings, client=client, by_text=False)
    return vectorstore

def chroma_db(splitted_text):
    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
    db = Chroma.from_texts(splitted_text, embeddings)
    return db

def faiss_db(splitted_text):
    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
    db = FAISS.from_texts(splitted_text, embeddings)
    db.save_local("faiss_db")
    return db

def model(query, db):
    llm = OpenAI(OPENAI_API_KEY)
    return llm.predict(query, db)

def format_json_to_multiline_string(data):
    result = []
    
    def recursive_format(data, indent_level=0):
        if isinstance(data, dict):
            for key, value in data.items():
                result.append("    " * indent_level + f"{key}:")
                recursive_format(value, indent_level + 1)
        elif isinstance(data, list):
            for item in data:
                result.append("    " * indent_level + f"- {item}")
        else:
            result.append("    " * indent_level + f"{data}")
    
    recursive_format(data)
    return "\n".join(result)

def get_total_revenue(symbol):
    time.sleep(3)
    url = "https://www.alphavantage.co/query"
    params = {
        "function": "INCOME_STATEMENT",
        "symbol": symbol,
        "apikey": AV_API_KEY
    }
    response = requests.get(url, params=params)
    data = response.json()
    return float(data["annualReports"][0]["totalRevenue"])

def get_total_debt(symbol):
    time.sleep(3)
    url = "https://www.alphavantage.co/query"
    params = {
        "function": "BALANCE_SHEET",
        "symbol": symbol,
        "apikey": AV_API_KEY
    }
    response = requests.get(url, params=params)
    data = response.json()
    short_term = float(data["annualReports"][0]["shortTermDebt"])
    time.sleep(3)
    long_term = float(data["annualReports"][0]["longTermDebt"])
    return short_term + long_term

def insights(type_of_data, data, pydantic_model):
    print(type_of_data)
    parser = PydanticOutputParser(pydantic_object=pydantic_model)
    with open("prompts/insights.prompt", "r") as f:
        template = f.read()

    prompt = PromptTemplate(
        template=template,
        input_variables=["type_of_data","inputs"],
        partial_variables={"output_format": parser.get_format_instructions()}
    )

    model = ChatOpenAI(openai_api_key=OPENAI_API_KEY, max_tokens=2000)

    data = format_json_to_multiline_string(data)

    formatted_input = prompt.format(type_of_data=type_of_data, inputs=data)
    print("-"*30)
    print("Formatted Input:")
    print(formatted_input)
    print("-"*30)

    response = model.predict(formatted_input)
    parsed_output = parser.parse(response)
    return parsed_output







