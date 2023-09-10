import sys
from pathlib import Path
script_dir = Path(__file__).resolve().parent
project_root = script_dir.parent
sys.path.append(str(project_root))


from langchain.vectorstores import Weaviate, Chroma, FAISS
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.document_loaders import TextLoader, PyPDFLoader
from langchain.schema.document import Document
from langchain.llms import OpenAI

from dotenv import dotenv_values
import weaviate
from pypdf import PdfReader
import streamlit as st

config = dotenv_values(".env")

OPENAI_API_KEY = config["OPENAI_API_KEY"]
WEAVIATE_URL = config["WEAVIATE_URL"]
WEAVIATE_API_KEY = config["WEAVIATE_API_KEY"]

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







