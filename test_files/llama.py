import sys
from pathlib import Path
script_dir = Path(__file__).resolve().parent
project_root = script_dir.parent
sys.path.append(str(project_root))

from langchain.prompts import PromptTemplate

from llama_index import VectorStoreIndex, SimpleDirectoryReader, ServiceContext, StorageContext
from llama_index.vector_stores import WeaviateVectorStore, FaissVectorStore
from weaviate.embedded import EmbeddedOptions

from src.utils import get_model, process_pdf2

import streamlit as st
import weaviate
import os
import openai

OPENAI_API_KEY = st.secrets["openai_api_key"]
WEAVIATE_URL = st.secrets["weaviate_url"]
WEAVIATE_API_KEY = st.secrets["weaviate_api_key"]

os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
openai.api_key = os.environ["OPENAI_API_KEY"]

if "process_doc" not in st.session_state:
        st.session_state.process_doc = False

def get_vector_index(nodes):
    print(nodes)
    client = weaviate.Client(embedded_options=EmbeddedOptions())
    llm = get_model("Clarifai")
    vector_store = WeaviateVectorStore(weaviate_client=client, index_name="LlamaIndex")
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    service_context = ServiceContext.from_defaults(llm=llm)
    index = VectorStoreIndex(nodes=nodes, storage_context=storage_context, service_context=service_context)
    return index

    

pdfs = st.file_uploader("Upload a PDF file")
if st.sidebar.button("Process Document"):
    with st.spinner("Processing Document..."):
        documents = process_pdf2(pdfs)
        st.session_state.process_doc = True


documents = SimpleDirectoryReader("data/microsoft").load_data()
print(documents)

template = """
You are tasked with analyzing the annual report of the company, and generate a list of Fiscal Year highlights.
The highlights can vary anywhere between 5 - 10 points. The highlights should be in the form of a bulleted list.
"""

# client = weaviate.Client(url=WEAVIATE_URL, auth_client_secret=weaviate.AuthApiKey(WEAVIATE_API_KEY))

client = weaviate.Client(embedded_options=EmbeddedOptions())

llm = get_model("Clarifai")

vector_store = WeaviateVectorStore(weaviate_client=client, index_name="LlamaIndex")
# vector_store = FaissVectorStore(index_name="LlamaIndex")
storage_context = StorageContext.from_defaults(vector_store=vector_store)
service_context = ServiceContext.from_defaults(llm=llm)
index = VectorStoreIndex.from_documents(documents, storage_context=storage_context, service_context=service_context)

engine = index.as_query_engine()

if st.session_state.process_doc:
    company_name = st.text_input("Enter the company name")

    if st.button("Ask"): 

        prompt = PromptTemplate(template=template)
        formatted_input = prompt.format()


        engine = st.session_state.index.as_query_engine()

        response = engine.query("provide some fiscal year highlights for apple in 2022")
        st.write(response.response)







