import sys
from pathlib import Path
script_dir = Path(__file__).resolve().parent
project_root = script_dir.parent
sys.path.append(str(project_root))

from llama_index import VectorStoreIndex, SimpleDirectoryReader, ServiceContext
from llama_index.vector_stores import WeaviateVectorStore, FaissVectorStore
from langchain.chains import RetrievalQA

from src.utils import get_model

import streamlit as st
import weaviate
import os
import openai

OPENAI_API_KEY = st.secrets["openai_api_key"]
WEAVIATE_URL = st.secrets["weaviate_url"]
WEAVIATE_API_KEY = st.secrets["weaviate_api_key"]

os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
openai.api_key = os.environ["OPENAI_API_KEY"]


documents = SimpleDirectoryReader("data").load_data()
print(documents)

from llama_index.storage.storage_context import StorageContext

client = weaviate.Client(url=WEAVIATE_URL, auth_client_secret=weaviate.AuthApiKey(WEAVIATE_API_KEY))
llm = get_model("Clarifai")

vector_store = WeaviateVectorStore(weaviate_client=client, index_name="LlamaIndex")
# vector_store = FaissVectorStore(index_name="LlamaIndex")
storage_context = StorageContext.from_defaults(vector_store=vector_store)
service_context = ServiceContext.from_defaults(llm=llm)
index = VectorStoreIndex.from_documents(documents, storage_context=storage_context, service_context=service_context)


engine = index.as_query_engine(streaming=True)


query = ""
while True:
    print("-"*30)
    query = input("Ask a question: ")
    if query == "exit":
        break
    ans = engine.query(query)
    print(ans)
    print("-"*30)







