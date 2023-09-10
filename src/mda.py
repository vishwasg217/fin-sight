import sys
from pathlib import Path
script_dir = Path(__file__).resolve().parent
project_root = script_dir.parent
sys.path.append(str(project_root))


from langchain.vectorstores import FAISS
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.document_loaders import TextLoader, PyPDFLoader
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA

from dotenv import dotenv_values
import weaviate
from pypdf import PdfReader
import streamlit as st

config = dotenv_values(".env")

OPENAI_API_KEY = config["OPENAI_API_KEY"]
WEAVIATE_URL = config["WEAVIATE_URL"]
WEAVIATE_API_KEY = config["WEAVIATE_API_KEY"]

from src.utils import vector_store

model = ChatOpenAI(openai_api_key=OPENAI_API_KEY, max_tokens=2000)
embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)

db = FAISS.load_local("faiss_db", embeddings=embeddings)

qa = RetrievalQA.from_chain_type(llm=model, 
                    chain_type="map_reduce",
                    retriever=db.as_retriever(), 
                    return_source_documents=False)

query = ""

while True:
    if query == "exit":
        break
    query = input("Ask a question: ")
    ans = qa.run(query)
    print(ans)
