import sys
from pathlib import Path
script_dir = Path(__file__).resolve().parent
project_root = script_dir.parent
sys.path.append(str(project_root))

from langchain.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser

from llama_index import VectorStoreIndex, ServiceContext, StorageContext
from llama_index.vector_stores import WeaviateVectorStore, FaissVectorStore, ChromaVectorStore
from llama_index.embeddings import OpenAIEmbedding
from weaviate.embedded import EmbeddedOptions
from llama_index.tools import QueryEngineTool, ToolMetadata
from llama_index.query_engine import SubQuestionQueryEngine

from src.utils import get_model, process_pdf2
from src.pydantic_models import FiscalYearHighlights, StrategyOutlookFutureDirection, RiskManagement, CorporateGovernanceSocialResponsibility, InnovationRnD

import streamlit as st
import weaviate
import os
import openai
import faiss
# import chromadb

st.set_page_config(page_title="Annual Report Analyzer", page_icon=":card_index_dividers:", initial_sidebar_state="expanded")

st.title(":card_index_dividers: Annual Report Analyzer")
st.info("""
Begin by uploading the annual report of your chosen company in PDF format. Afterward, click on 'Process PDF'. Once the document has been processed, tap on 'Analyze Report' and the system will start its magic. After a brief wait, you'll be presented with a detailed analysis and insights derived from the report for your reading.
""")

OPENAI_API_KEY = st.secrets["openai_api_key"]
WEAVIATE_URL = st.secrets["weaviate_url"]
WEAVIATE_API_KEY = st.secrets["weaviate_api_key"]

os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
openai.api_key = os.environ["OPENAI_API_KEY"]



def get_vector_index(documents, vector_store):
    print(documents)
    llm = get_model("Clarifai")
    if vector_store == "weaviate":
        client = weaviate.Client(embedded_options=EmbeddedOptions())
        
        vector_store = WeaviateVectorStore(weaviate_client=client, index_name="LlamaIndex")
        storage_context = StorageContext.from_defaults(vector_store=vector_store)
        service_context = ServiceContext.from_defaults(llm=llm)
        index = VectorStoreIndex.from_documents(documents, storage_context=storage_context, service_context=service_context)
    elif vector_store == "faiss":
        d = 1536
        faiss_index = faiss.IndexFlatL2(d)
        vector_store = FaissVectorStore(faiss_index=faiss_index)
        storage_context = StorageContext.from_defaults(vector_store=vector_store)
        service_context = ServiceContext.from_defaults(llm=llm)
        index = VectorStoreIndex.from_documents(documents, storage_context=storage_context)
    elif vector_store == "simple":
        index = VectorStoreIndex.from_documents(documents)
    # elif vector_store == "chroma":
    #     chroma_client = chromadb.EphemeralClient()
    #     chroma_collection = chroma_client.create_collection("quickstart")
    #     embed_model = OpenAIEmbedding()
    #     vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    #     storage_context = StorageContext.from_defaults(vector_store=vector_store)
    #     service_context = ServiceContext.from_defaults(embed_model=embed_model)
    #     index = VectorStoreIndex.from_documents(
    #         documents, storage_context=storage_context, service_context=service_context
    #     )


    return index

with open("prompts/report.prompt", "r") as f:
    template = f.read()

def report_insights(engine, section, pydantic_model):
    parser = PydanticOutputParser(pydantic_object=pydantic_model)
    prompt_template = PromptTemplate(
        template=template,
        input_variables=["section"],
        partial_variables={"output_format": parser.get_format_instructions()}
    )

    formatted_input = prompt_template.format(section=section)
    print(formatted_input)

    response = engine.query(formatted_input)
    parsed_response = parser.parse(response.response)
    print(parsed_response)
    return parsed_response

def get_query_engine(engine):
    query_engine_tools = [
        QueryEngineTool(
            query_engine=engine,
            metadata=ToolMetadata(
                name="Annual Report",
                description=f"Provides information about the company from its annual report.",
            ),
        ),
    ]
    s_engine = SubQuestionQueryEngine.from_defaults(query_engine_tools=query_engine_tools)
    return s_engine

sections = {
    "Fiscal Year Highlights": FiscalYearHighlights,
    "Strategy Outlook and Future Direction": StrategyOutlookFutureDirection,
    "Risk Management": RiskManagement,
    # "Corporate Governance and Social Responsibility": CorporateGovernanceSocialResponsibility,
    "Innovation and R&D": InnovationRnD
}


if "process_doc" not in st.session_state:
        st.session_state.process_doc = False

if "fiscal_year_highlights" not in st.session_state:
    st.session_state.fiscal_year_highlights = None

if "strategy_outlook_future_direction" not in st.session_state:
    st.session_state.strategy_outlook_future_direction = None

if "risk_management" not in st.session_state:
    st.session_state.risk_management = None

if "innovation_and_rd" not in st.session_state:
    st.session_state.innovation_and_rd = None


pdfs = st.sidebar.file_uploader("Upload the annual report in PDF format", type="pdf")
st.sidebar.info("""
Example reports you can upload here: 
- [Apple Inc.](https://s2.q4cdn.com/470004039/files/doc_financials/2022/q4/_10-K-2022-(As-Filed).pdf)
- [Microsoft Corporation](https://microsoft.gcs-web.com/static-files/07cf3c30-cfc3-4567-b20f-f4b0f0bd5087)
- [Tesla Inc.](https://digitalassets.tesla.com/tesla-contents/image/upload/IR/TSLA-Q4-2022-Update)
""")

if st.sidebar.button("Process Document"):
    with st.spinner("Processing Document..."):
        documents = process_pdf2(pdfs)
        st.session_state.index = get_vector_index(documents, vector_store="faiss")
        st.session_state.process_doc = True


if st.session_state.process_doc:
    # company_name = st.text_input("Enter the company name")

    if st.button("Analyze Report"):

        engine = get_query_engine(st.session_state.index.as_query_engine(similarity_top_k=3))

        with st.spinner("Fiscal Year Highlights..."):
            st.session_state.fiscal_year_highlights = report_insights(engine, "Fiscal Year Highlights", FiscalYearHighlights)

        with st.spinner("Strategy Outlook and Future Direction..."):
            st.session_state.strategy_outlook_future_direction = report_insights(engine, "Strategy Outlook and Future Direction", StrategyOutlookFutureDirection)

        with st.spinner("Risk Management..."):
            st.session_state.risk_management = report_insights(engine, "Risk Management", RiskManagement)
        
        with st.spinner("Innovation and R&D..."):
            st.session_state.innovation_and_rd = report_insights(engine, "Innovation and R&D", InnovationRnD)
        
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
            st.write(str(st.session_state.fiscal_year_highlights.milestone_achievements))


    if st.session_state.strategy_outlook_future_direction:
        with tab2:
            st.write("## Strategy Outlook and Future Direction")
            st.write("### Strategic Initiatives")
            st.write(st.session_state.strategy_outlook_future_direction.strategic_initiatives)
            st.write("### Market Outlook")
            st.write(st.session_state.strategy_outlook_future_direction.market_outlook)
            st.write("### Product Roadmap")
            st.write(st.session_state.strategy_outlook_future_direction.product_roadmap)

    if st.session_state.risk_management:
        with tab3:
            st.write("## Risk Management")
            st.write("### Risk Factors")
            st.write(st.session_state.risk_management.risk_factors)
            st.write("### Risk Mitigation")
            st.write(st.session_state.risk_management.risk_mitigation)

    if st.session_state.innovation_and_rd:
        with tab4:
            st.write("## Innovation and R&D")
            st.write("### R&D Activities")
            st.write(st.session_state.innovation_and_rd.r_and_d_activities)
            st.write("### Innovation Focus")
            st.write(st.session_state.innovation_and_rd.innovation_focus)
        
            
             

        










