from langchain.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser

from llama_index import VectorStoreIndex, ServiceContext, StorageContext
from llama_index.vector_stores import FaissVectorStore
from llama_index.tools import QueryEngineTool, ToolMetadata
from llama_index.query_engine import SubQuestionQueryEngine
from llama_index.embeddings import OpenAIEmbedding
from llama_index.schema import Document
from llama_index.node_parser import UnstructuredElementNodeParser

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
import os
import faiss
import time
from pypdf import PdfReader


st.set_page_config(page_title="Annual Report Analyzer", page_icon=":card_index_dividers:", initial_sidebar_state="expanded", layout="wide")

st.title(":card_index_dividers: Annual Report Analyzer")
st.info("""
Begin by uploading the annual report of your chosen company in PDF format. Afterward, click on 'Process PDF'. Once the document has been processed, tap on 'Analyze Report' and the system will start its magic. After a brief wait, you'll be presented with a detailed analysis and insights derived from the report for your reading.
""")

def process_pdf(pdf):
    file = PdfReader(pdf)

    document_list = []
    for page in file.pages:
        document_list.append(Document(text=str(page.extract_text())))

    node_paser = UnstructuredElementNodeParser()
    nodes = node_paser.get_nodes_from_documents(document_list, show_progress=True)
    
    return nodes


def get_vector_index(nodes, vector_store):
    print(nodes)
    llm = get_model("openai")
    if vector_store == "faiss":
        d = 1536
        faiss_index = faiss.IndexFlatL2(d)
        vector_store = FaissVectorStore(faiss_index=faiss_index)
        storage_context = StorageContext.from_defaults(vector_store=vector_store)
        # embed_model = OpenAIEmbedding()
        # service_context = ServiceContext.from_defaults(embed_model=embed_model)
        service_context = ServiceContext.from_defaults(llm=llm) 
        index = VectorStoreIndex(nodes, 
            service_context=service_context,
            storage_context=storage_context
        )
    elif vector_store == "simple":
        index = VectorStoreIndex.from_documents(nodes)


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
    return response.response
    


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

    return {
        "insights": ins
    }

def get_query_engine(engine):
    llm = get_model("openai")
    service_context = ServiceContext.from_defaults(llm=llm)

    query_engine_tools = [
        QueryEngineTool(
            query_engine=engine,
            metadata=ToolMetadata(
                name="Annual Report",
                description=f"Provides information about the company from its annual report.",
            ),
        ),
    ]


    s_engine = SubQuestionQueryEngine.from_defaults(
        query_engine_tools=query_engine_tools,
        service_context=service_context
    )
    return s_engine


for insight in fiscal_year_attributes:
    if insight not in st.session_state:
        st.session_state[insight] = None

for insight in strat_outlook_attributes:
    if insight not in st.session_state:
        st.session_state[insight] = None

for insight in risk_management_attributes:
    if insight not in st.session_state:
        st.session_state[insight] = None

for insight in innovation_attributes:
    if insight not in st.session_state:
        st.session_state[insight] = None

if "end_time" not in st.session_state:
    st.session_state.end_time = None


if "process_doc" not in st.session_state:
        st.session_state.process_doc = False


st.sidebar.info("""
You can get your OpenAI API key [here](https://openai.com/blog/openai-api)
""")
OPENAI_API_KEY = st.sidebar.text_input("OpenAI API Key", type="password")
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

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
            nodes = process_pdf(pdfs)
            st.session_state.index = get_vector_index(nodes, vector_store="faiss")
            st.session_state.process_doc = True
            

        st.toast("Document Processsed!")


    if st.session_state.process_doc:

        col1, col2 = st.columns([0.25, 0.75])

        with col1:
            st.write("""
                ### Select Insights
            """)
            
            with st.expander("**Fiscal Year Highlights**", expanded=True):
                performance_highlights = st.toggle("Performance Highlights")
                major_events = st.toggle("Major Events")
                challenges_encountered = st.toggle("Challenges Encountered")

                fiscal_year_highlights_list = [performance_highlights, major_events, challenges_encountered]

            with st.expander("**Strategy Outlook and Future Direction**", expanded=True):
                strategic_initiatives = st.toggle("Strategic Initiatives")
                market_outlook = st.toggle("Market Outlook")
                product_roadmap = st.toggle("Product Roadmap")

                strategy_outlook_future_direction_list = [strategic_initiatives, market_outlook, product_roadmap]

            with st.expander("**Risk Management**", expanded=True):
                risk_factors = st.toggle("Risk Factors")
                risk_mitigation = st.toggle("Risk Mitigation")

                risk_management_list = [risk_factors, risk_mitigation]

            with st.expander("**Innovation and R&D**", expanded=True):
                r_and_d_activities = st.toggle("R&D Activities")
                innovation_focus = st.toggle("Innovation Focus")

                innovation_and_rd_list = [r_and_d_activities, innovation_focus]


        with col2:
            if st.button("Analyze Report"):
                engine = get_query_engine(st.session_state.index.as_query_engine(similarity_top_k=3))
                start_time = time.time()

                with st.status("**Analyzing Report...**"):


                    if any(fiscal_year_highlights_list):
                        st.write("Fiscal Year Highlights...")

                        for i, insight in enumerate(fiscal_year_attributes):
                            if st.session_state[insight]:
                                fiscal_year_highlights_list[i] = False

                        response = report_insights(engine, "Fiscal Year Highlights", fiscal_year_highlights_list, 1)

                        for key, value in response["insights"].items():
                            st.session_state[key] = value

                    if any(strategy_outlook_future_direction_list):
                        st.write("Strategy Outlook and Future Direction...")

                        for i, insight in enumerate(strat_outlook_attributes):
                            if st.session_state[insight]:
                                strategy_outlook_future_direction_list[i] = False
                        response = report_insights(engine, "Strategy Outlook and Future Direction", strategy_outlook_future_direction_list, 2)

                        for key, value in response["insights"].items():
                            st.session_state[key] = value


                    if any(risk_management_list):
                        st.write("Risk Management...")

                        for i, insight in enumerate(risk_management_attributes):
                            if st.session_state[insight]:
                                risk_management_list[i] = False
                        
                        response = report_insights(engine, "Risk Management", risk_management_list, 3)

                        for key, value in response["insights"].items():
                            st.session_state[key] = value

                    if any(innovation_and_rd_list):
                        st.write("Innovation and R&D...")

                        for i, insight in enumerate(innovation_attributes):
                            if st.session_state[insight]:
                                innovation_and_rd_list[i] = False

                        response = report_insights(engine, "Innovation and R&D", innovation_and_rd_list, 4)
                        st.session_state.innovation_and_rd = response

                        for key, value in response["insights"].items():
                            st.session_state[key] = value

                    st.session_state["end_time"] = "{:.2f}".format((time.time() - start_time))



                    st.toast("Report Analysis Complete!")
            
            if st.session_state.end_time:
                st.write("Report Analysis Time: ", st.session_state.end_time, "s")


        # if st.session_state.all_report_outputs:
        #     st.toast("Report Analysis Complete!")
            
            tab1, tab2, tab3, tab4 = st.tabs(["Fiscal Year Highlights", "Strategy Outlook and Future Direction", "Risk Management", "Innovation and R&D"])

            
                

            with tab1:
                st.write("## Fiscal Year Highlights")
                try: 
                    if performance_highlights:
                        if st.session_state['performance_highlights']:
                            st.write("### Performance Highlights")
                            st.write(st.session_state['performance_highlights'])
                        else:
                            st.error("fiscal Year Highlights insight has not been generated")
                except:
                    st.error("This insight has not been generated")

                try:
                    if major_events:
                        if st.session_state["major_events"]:
                            st.write("### Major Events")
                            st.write(st.session_state["major_events"])
                        else:
                            st.error("Major Events insight has not been generated")
                except:
                    st.error("This insight has not been generated")
                try:
                    if challenges_encountered:
                        if st.session_state["challenges_encountered"]:
                            st.write("### Challenges Encountered")
                            st.write(st.session_state["challenges_encountered"])
                        else:
                            st.error("Challenges Encountered insight has not been generated")
                except:
                    st.error("This insight has not been generated")
                # st.write("### Milestone Achievements")
                # st.write(str(st.session_state.fiscal_year_highlights.milestone_achievements))


            
            with tab2:
                st.write("## Strategy Outlook and Future Direction")
                try:
                    if strategic_initiatives:
                        if st.session_state["strategic_initiatives"]:
                            st.write("### Strategic Initiatives")
                            st.write(st.session_state["strategic_initiatives"])
                        else:
                            st.error("Strategic Initiatives insight has not been generated")
                except:
                    st.error("This insight has not been generated")

                try:
                    if market_outlook:
                        if st.session_state["market_outlook"]:
                            st.write("### Market Outlook")
                            st.write(st.session_state["market_outlook"])
                        else:
                            st.error("Market Outlook insight has not been generated")

                except:
                    st.error("This insight has not been generated")

                try:
                    if product_roadmap:
                        if st.session_state["product_roadmap"]:
                            st.write("### Product Roadmap")
                            st.write(st.session_state["product_roadmap"])
                        else:
                            st.error("Product Roadmap insight has not been generated")
                except:
                    st.error("This insight has not been generated")

            with tab3:
                st.write("## Risk Management")

                try:
                    if risk_factors:
                        if st.session_state["risk_factors"]:
                            st.write("### Risk Factors")
                            st.write(st.session_state["risk_factors"])
                        else:
                            st.error("Risk Factors insight has not been generated")
                except:
                    st.error("This insight has not been generated")

                try:
                    if risk_mitigation:
                        if st.session_state["risk_mitigation"]:
                            st.write("### Risk Mitigation")
                            st.write(st.session_state["risk_mitigation"])
                        else:
                            st.error("Risk Mitigation insight has not been generated")
                except:
                    st.error("This insight has not been generated")


            with tab4:
                st.write("## Innovation and R&D")

                try:
                    if r_and_d_activities:
                        if st.session_state["r_and_d_activities"]:
                            st.write("### R&D Activities")
                            st.write(st.session_state["r_and_d_activities"])
                        else:
                            st.error("R&D Activities insight has not been generated")
                except:
                    st.error("This insight has not been generated")

                try:
                    if innovation_focus:
                        if st.session_state["innovation_focus"]:
                            st.write("### Innovation Focus")
                            st.write(st.session_state["innovation_focus"])
                        else:
                            st.error("Innovation Focus insight has not been generated")
                except:
                    st.error("This insight has not been generated")
