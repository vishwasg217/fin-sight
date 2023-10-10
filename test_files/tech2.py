import sys
from pathlib import Path
script_dir = Path(__file__).resolve().parent
project_root = script_dir.parent
sys.path.append(str(project_root))

from src.utils import get_model
import faiss
import streamlit as st
import os
import openai


from llama_index import (
    VectorStoreIndex,
    SummaryIndex,
    SimpleKeywordTableIndex,
    SimpleDirectoryReader,
    ServiceContext,
    StorageContext
)
from llama_index.schema import IndexNode
from llama_index.tools import QueryEngineTool, ToolMetadata
from llama_index.llms import OpenAI
from llama_index.agent import OpenAIAgent
from llama_index.query_engine import SubQuestionQueryEngine
from llama_index.vector_stores import FaissVectorStore

from langchain.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser

from src.pydantic_models import FiscalYearHighlights, StrategyOutlookFutureDirection, RiskManagement, CorporateGovernanceSocialResponsibility, InnovationRnD


OPENAI_API_KEY = st.secrets["openai_api_key"]
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
openai.api_key = os.environ["OPENAI_API_KEY"]

# llm = OpenAI(temperature=0, model="gpt-3.5-turbo")
llm = get_model("Clarifai")
service_context = ServiceContext.from_defaults(llm=llm)

document = SimpleDirectoryReader("data/apple").load_data()
# print(document)

d = 1536
faiss_index = faiss.IndexFlatL2(d)
vector_store = FaissVectorStore(faiss_index=faiss_index)
storage_context = StorageContext.from_defaults(vector_store=vector_store)
vector_index = VectorStoreIndex.from_documents(document,
    service_context=service_context,
    storage_context=storage_context
)

# summary_index = SummaryIndex.from_documents(document,
#     service_context=service_context,
#     storage_context=storage_context
# )

vector_query_engine = vector_index.as_query_engine()
# summary_query_engine = summary_index.as_query_engine(similarity_top_k=3)

query_engine_tools = [
    QueryEngineTool(
        query_engine=vector_query_engine,
        metadata=ToolMetadata(
            name="Vector Query Engine",
            description="Provides information about the company from it's annual report."
        )
    ),
    # QueryEngineTool(
    #     query_engine=summary_query_engine,
    #     metadata=ToolMetadata(
    #         name="Summary Query Engine",
    #         description="Provides Summarization of different sections of the annual report for the company."
    #     )
    # )
]

s_engine = SubQuestionQueryEngine.from_defaults(query_engine_tools=query_engine_tools)


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

response = report_insights(s_engine, "Fiscal Year Highlights", FiscalYearHighlights)
print(response)

# query = ""

# while query != "exit":
#     query = input("Enter query: ")
#     response = s_engine.query(query)
#     print(response)
#     print("-"*30)
