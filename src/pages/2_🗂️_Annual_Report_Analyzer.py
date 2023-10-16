import sys
from pathlib import Path
from token import OP
script_dir = Path(__file__).resolve().parent
project_root = script_dir.parent
sys.path.append(str(project_root))


from langchain.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser

from llama_index import VectorStoreIndex, ServiceContext, StorageContext
from llama_index.vector_stores import FaissVectorStore
from llama_index.tools import QueryEngineTool, ToolMetadata
from llama_index.query_engine import SubQuestionQueryEngine
from llama_index.embeddings import OpenAIEmbedding

from src.utils import get_model, process_pdf2, generate_pydantic_model
from src.pydantic_models import FiscalYearHighlights, StrategyOutlookFutureDirection, RiskManagement, CorporateGovernanceSocialResponsibility, InnovationRnD
# from src.fields import (
#     fiscal_year_fields, fiscal_year_attributes, 
#     strat_outlook_fields, strat_outlook_attributes, 
#     risk_management_fields, risk_management_attributes, 
#     innovation_fields, innovation_attributes
# )

from src.fields2 import (
    fiscal_year, fiscal_year_attributes,
    strat_outlook, strat_outlook_attributes,
    risk_management, risk_management_attributes,
    innovation, innovation_attributes
)

import streamlit as st
import weaviate
import os
import openai
import faiss

st.set_page_config(page_title="Annual Report Analyzer", page_icon=":card_index_dividers:", initial_sidebar_state="expanded", layout="wide")

st.title(":card_index_dividers: Annual Report Analyzer")
st.info("""
Begin by uploading the annual report of your chosen company in PDF format. Afterward, click on 'Process PDF'. Once the document has been processed, tap on 'Analyze Report' and the system will start its magic. After a brief wait, you'll be presented with a detailed analysis and insights derived from the report for your reading.
""")

# OPENAI_API_KEY = st.secrets["openai_api_key"]

# os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
# openai.api_key = os.environ["OPENAI_API_KEY"]


def get_vector_index(documents, vector_store):
    print(documents)
    llm = get_model("openai", OPENAI_API_KEY)
    if vector_store == "faiss":
        d = 1536
        faiss_index = faiss.IndexFlatL2(d)
        vector_store = FaissVectorStore(faiss_index=faiss_index)
        storage_context = StorageContext.from_defaults(vector_store=vector_store)
        # embed_model = OpenAIEmbedding()
        # service_context = ServiceContext.from_defaults(embed_model=embed_model)
        service_context = ServiceContext.from_defaults(llm=llm) 
        index = VectorStoreIndex.from_documents(documents, 
            service_context=service_context,
            storage_context=storage_context
        )
    elif vector_store == "simple":
        index = VectorStoreIndex.from_documents(documents)


    return index



def generate_insight(engine, insight_name, section_name, output_format):

    with open("prompts/report.prompt", "r") as f:
        template = f.read()

    prompt_template = PromptTemplate(
        template=template,
        input_variables=['insight_name', 'section_name', 'output_format']
    )

    formatted_input = prompt_template.format(insight_name=insight_name, section_name=section_name, output_format=output_format)
    print(formatted_input)
    response = engine.query(formatted_input)
    return response
    


def report_insights(engine, section_name, fields_to_include, section_num):

    fields = None
    attribs = None

    if section_num == 1:
        fields = fiscal_year
        attribs = fiscal_year_attributes
    elif section_num == 2:
        fields = strat_outlook
        attribs = strat_outlook_attributes
    elif section_num == 3:
        fields = risk_management
        attribs = risk_management_attributes
    elif section_num == 4:
        fields = innovation
        attribs = innovation_attributes

    ins = {}
    for i, field in enumerate(attribs):
        if fields_to_include[i]:
            response = generate_insight(engine, field, section_name, str({field: fields[field]}))
            ins[field] = response
            
    return ins

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

if "all_report_outputs" not in st.session_state:
    st.session_state.all_report_outputs = None

OPENAI_API_KEY = st.sidebar.text_input("OpenAI API Key", type="password")

if not OPENAI_API_KEY:
    st.error("Please enter your OpenAI API Key")

if OPENAI_API_KEY:
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
            

        st.toast("Document Processsed!")


    if st.session_state.process_doc:

        col1, col2 = st.columns([0.25, 0.75])

        with col1:
            st.write("""
                ### Select Insights
            """)
            
            with st.expander("**Fiscal Year Highlights**", expanded=True):
                performance_highlights = st.toggle("Performance Highlights", value=True)
                major_events = st.toggle("Major Events", value=True)
                challenges_encountered = st.toggle("Challenges Encountered", value=True)

                fiscal_year_highlights_list = [performance_highlights, major_events, challenges_encountered]

            with st.expander("**Strategy Outlook and Future Direction**", expanded=True):
                strategic_initiatives = st.toggle("Strategic Initiatives", value=True)
                market_outlook = st.toggle("Market Outlook", value=True)
                product_roadmap = st.toggle("Product Roadmap", value=True)

                strategy_outlook_future_direction_list = [strategic_initiatives, market_outlook, product_roadmap]

            with st.expander("**Risk Management**", expanded=True):
                risk_factors = st.toggle("Risk Factors", value=True)
                risk_mitigation = st.toggle("Risk Mitigation", value=True)

                risk_management_list = [risk_factors, risk_mitigation]

            with st.expander("**Innovation and R&D**", expanded=True):
                r_and_d_activities = st.toggle("R&D Activities", value=True)
                innovation_focus = st.toggle("Innovation Focus", value=True)

                innovation_and_rd_list = [r_and_d_activities, innovation_focus]


        
            

        with col2:
            if st.button("Analyze Report"):
                engine = get_query_engine(st.session_state.index.as_query_engine(similarity_top_k=3))

                with st.status("**Analyzing Report...**"):

                    st.write("Fiscal Year Highlights...")
                    st.session_state.fiscal_year_highlights = report_insights(engine, "Fiscal Year Highlights", fiscal_year_highlights_list, 1)

                    st.write("Strategy Outlook and Future Direction...")
                    st.session_state.strategy_outlook_future_direction = report_insights(engine, "Strategy Outlook and Future Direction", strategy_outlook_future_direction_list, 2)

                    st.write("Risk Management...")
                    st.session_state.risk_management = report_insights(engine, "Risk Management", risk_management_list, 3)
                    
                    st.write("Innovation and R&D...")
                    st.session_state.innovation_and_rd = report_insights(engine, "Innovation and R&D", innovation_and_rd_list, 4)

                    if st.session_state.fiscal_year_highlights and st.session_state.strategy_outlook_future_direction and st.session_state.risk_management and st.session_state.innovation_and_rd:
                        st.session_state.all_report_outputs = True

                    st.toast("Report Analysis Complete!")
            

        # if st.session_state.all_report_outputs:
        #     st.toast("Report Analysis Complete!")
            
            tab1, tab2, tab3, tab4 = st.tabs(["Fiscal Year Highlights", "Strategy Outlook and Future Direction", "Risk Management", "Innovation and R&D"])

            if st.session_state.fiscal_year_highlights:
                

                with tab1:
                    st.write("## Fiscal Year Highlights")
                    try: 
                        if performance_highlights:
                            st.write("### Performance Highlights")
                            st.write(st.session_state.fiscal_year_highlights.performance_highlights)
                    except:
                        st.error("This insight has not been generated")

                    try:
                        if major_events:
                            st.write("### Major Events")
                            st.write(st.session_state.fiscal_year_highlights.major_events)
                    except:
                        st.error("This insight has not been generated")
                    try:
                        if challenges_encountered:
                            st.write("### Challenges Encountered")
                            st.write(st.session_state.fiscal_year_highlights.challenges_encountered)
                    except:
                        st.error("This insight has not been generated")
                    # st.write("### Milestone Achievements")
                    # st.write(str(st.session_state.fiscal_year_highlights.milestone_achievements))


            if st.session_state.strategy_outlook_future_direction:
                with tab2:
                    st.write("## Strategy Outlook and Future Direction")
                    try:
                        if strategic_initiatives:
                            st.write("### Strategic Initiatives")
                            st.write(st.session_state.strategy_outlook_future_direction.strategic_initiatives)
                    except:
                        st.error("This insight has not been generated")

                    try:
                        if market_outlook:
                            st.write("### Market Outlook")
                            st.write(st.session_state.strategy_outlook_future_direction.market_outlook)

                    except:
                        st.error("This insight has not been generated")

                    try:
                        if product_roadmap:
                            st.write("### Product Roadmap")
                            st.write(st.session_state.strategy_outlook_future_direction.product_roadmap)

                    except:
                        st.error("This insight has not been generated")

            if st.session_state.risk_management:
                with tab3:
                    st.write("## Risk Management")

                    try:
                        if risk_factors:
                            st.write("### Risk Factors")
                            st.write(st.session_state.risk_management.risk_factors)
                    except:
                        st.error("This insight has not been generated")

                    try:
                        if risk_mitigation:
                            st.write("### Risk Mitigation")
                            st.write(st.session_state.risk_management.risk_mitigation)
                    except:
                        st.error("This insight has not been generated")


            if st.session_state.innovation_and_rd:
                with tab4:
                    st.write("## Innovation and R&D")

                    try:
                        if r_and_d_activities:
                            st.write("### R&D Activities")
                            st.write(st.session_state.innovation_and_rd.r_and_d_activities)
                    except:
                        st.error("This insight has not been generated")

                    try:
                        if innovation_focus:
                            st.write("### Innovation Focus")
                            st.write(st.session_state.innovation_and_rd.innovation_focus)
                    except:
                        st.error("This insight has not been generated")
