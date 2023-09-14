import sys
from pathlib import Path
script_dir = Path(__file__).resolve().parent
project_root = script_dir.parent
sys.path.append(str(project_root))

from langchain.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser

from llama_index import VectorStoreIndex, SimpleDirectoryReader, ServiceContext, StorageContext
from llama_index.vector_stores import WeaviateVectorStore
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

def get_vector_index(documents):
    print(documents)
    client = weaviate.Client(embedded_options=EmbeddedOptions())
    llm = get_model("Clarifai")
    vector_store = WeaviateVectorStore(weaviate_client=client, index_name="LlamaIndex")
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    service_context = ServiceContext.from_defaults(llm=llm)
    index = VectorStoreIndex.from_documents(documents, storage_context=storage_context, service_context=service_context)
    return index

template = """
You are tasked with analyzing the annual report of the company, and generate a list of {content}.
The {content} can vary anywhere between 5 - 10 points. The {content} should be in the form of a bulleted list.
provide statistics on the {content} if possible.
"""


if "process_doc" not in st.session_state:
        st.session_state.process_doc = False

pdfs = st.sidebar.file_uploader("Upload a PDF file")
if st.sidebar.button("Process Document"):
    with st.spinner("Processing Document..."):
        documents = process_pdf2(pdfs)
        st.session_state.index = get_vector_index(documents)
        st.session_state.process_doc = True

        
if st.session_state.process_doc:
    # company_name = st.text_input("Enter the company name")

    if st.button("Ask"):
        contents = ["Fiscal Year Highlights", "Risk Factors"] 

        prompt = PromptTemplate(template=template,
                            input_variables=["content"]
                            )
        engine = st.session_state.index.as_query_engine()

        for content in contents:
            formatted_input = prompt.format(content=content)
            response = engine.query(formatted_input)
            st.write(response.response)










