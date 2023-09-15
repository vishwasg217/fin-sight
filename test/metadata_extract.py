import sys
from pathlib import Path


import weaviate
from weaviate.embedded import EmbeddedOptions

script_dir = Path(__file__).resolve().parent
project_root = script_dir.parent
sys.path.append(str(project_root))

import streamlit as st
import os
import openai


from src.utils import process_pdf2, get_model
from src.pydantic_models import FiscalYearHighlights, StrategyOutlookFutureDirection, RiskManagement, CorporateGovernanceSocialResponsibility, InnovationRnD


from llama_index import SimpleDirectoryReader
from llama_index.node_parser.extractors import (
    MetadataExtractor,
    TitleExtractor,
    SummaryExtractor,
    KeywordExtractor,
    EntityExtractor
)
from llama_index.node_parser import SimpleNodeParser
from llama_index.text_splitter import TokenTextSplitter
from llama_index.indices.service_context import ServiceContext
from llama_index.storage.storage_context import StorageContext
from llama_index.vector_stores.weaviate import WeaviateVectorStore
from llama_index import VectorStoreIndex

from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import PromptTemplate

OPENAI_API_KEY = st.secrets["openai_api_key"]
WEAVIATE_URL = st.secrets["weaviate_url"]
WEAVIATE_API_KEY = st.secrets["weaviate_api_key"]

os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
openai.api_key = os.environ["OPENAI_API_KEY"]


def get_vector_index(nodes):
    print(nodes)
    client = weaviate.Client(embedded_options=EmbeddedOptions())
    llm = get_model("Clarifai")
    vector_store = WeaviateVectorStore(weaviate_client=client, index_name="LlamaIndex")
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    service_context = ServiceContext.from_defaults(llm=llm)
    index = VectorStoreIndex(nodes, storage_context=storage_context, service_context=service_context)
    return index

template = """
You are given the task of generating insights for {section} from the annual report of {company}. 

Given below is the output format, which has the subsections.
Write atleast 50 words for each subsection.
Incase you don't have enough info you can just write: No information available
---
{output_format}
---

"""

def report_insights(engine, section,company_name, pydantic_model):
    parser = PydanticOutputParser(pydantic_object=pydantic_model)
    prompt_template = PromptTemplate(
        template=template,
        input_variables=["section", "company"],
        partial_variables={"output_format": parser.get_format_instructions()}
    )

    formatted_input = prompt_template.format(section=section, company=company_name)
    print(formatted_input)

    response = engine.query(formatted_input)
    parsed_response = parser.parse(response.response)
    print(parsed_response)
    return parsed_response

text_splitter = TokenTextSplitter(separator=" ", chunk_size=512, chunk_overlap=128)


llm = get_model("Clarifai")
metadata_extractor = MetadataExtractor(
    extractors =[
        TitleExtractor(nodes=5, llm=llm),
        # EntityExtractor(prediction_threshold=0.5),
        # SummaryExtractor(summaries=["prev", "self"], llm=llm),
        # KeywordExtractor(keywords=1, llm=llm),
    ]
)
node_parser = SimpleNodeParser.from_defaults(
    text_splitter=text_splitter,
    metadata_extractor=metadata_extractor,
)


pdfs = st.file_uploader("Upload a PDF file")
# st.write(pdfs.getvalue().decode(errors="ignore"))
# documents = uber_docs = SimpleDirectoryReader(input_dir="data/apple").load_data()

if "process" in st.session_state:
    st.session_state.process = None

if "total_nodes" not in st.session_state:
    st.session_state.total_nodes = None

if "fiscal_year_highlights" not in st.session_state:
    st.session_state.fiscal_year_highlights = None


if st.sidebar.button("Process Document"):
    documents = process_pdf2(pdfs)
    st.session_state.process = True

    st.write(len(documents))

    # for x in range(0, 4):
    #     front_page = 
    # doc_len = len(documents)
    # content = documents[4:doc_len]

    # total_docs = front_page + content

    

if st.session_state.process:
    st.session_state.total_nodes = node_parser.get_nodes_from_documents(documents, show_progress=True)


    # if st.session_state.total_nodes:
        # st.write(type(st.session_state.total_nodes[1]))

        # # st.write(st.session_state.total_nodes[1].metadata)

        # st.write(len(st.session_state.total_nodes))
        # for x in st.session_state.total_nodes:
        #     st.write(x)
        #     st.write(x.metadata)

        
if st.session_state.total_nodes:

    st.session_state.index = get_vector_index(st.session_state.total_nodes)

    company_name = st.text_input("Enter the company name")

    if st.button("Ask"):

        engine = st.session_state.index.as_query_engine()

        with st.spinner("Fiscal Year Highlights..."):
            st.session_state.fiscal_year_highlights = report_insights(engine, "Fiscal Year Highlights", company_name, FiscalYearHighlights)

    tab1, tab2, tab3, tab4 = st.tabs(["Fiscal Year Highlights", "Strategy Outlook and Future Direction", "Risk Management", "Innovation and R&D"])

    if st.session_state.fiscal_year_highlights:
        
        with tab1:
            st.write("## Fiscal Year Highlights")
            st.write("### Performance Highlights")
            st.write(st.session_state.fiscal_year_highlights.performance_highlights)
            st.write("### Major Events")
            st.write(st.session_state.fiscal_year_highlights.major_events)
            st.write("### Challenges Encountered")
            st.write(st.session_state.fiscal_year_highlights.challenges_encountered)
            st.write("### Milestone Achievements")
            st.write(st.session_state.fiscal_year_highlights.milestone_achievements)
