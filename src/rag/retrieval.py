from llama_index.schema import TextNode
from llama_index import ServiceContext
from llama_index.llms import OpenAI
from llama_index import VectorStoreIndex
from llama_index.query_engine import SubQuestionQueryEngine, RetrieverQueryEngine
from llama_index.tools import QueryEngineTool, ToolMetadata
import nest_asyncio

nest_asyncio.apply()

import os

from src.utils import get_model


class Retrieve():

    def __init__(self, chunks):
        self.chunks = chunks
        self.llm = get_model("openai")
        self.service_context = ServiceContext.from_defaults(llm=self.llm)

    def convert_chunks_to_nodes(self):
        nodes = []
        for chunk in self.chunks:
            node = TextNode()
            node.text = chunk['content']
            node.metadata = chunk['metadata']
            nodes.append(node)

        return nodes
    
    def get_vector_index_engine(self, nodes):
        OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

        vector_index = VectorStoreIndex(
            nodes=nodes, 
            service_context=self.service_context,
        )

        engine = vector_index.as_query_engine(similarity_top_k=2)

        return engine
    
    def get_sub_question_query_engine(self, engine):
        query_enginer_tools = [
        QueryEngineTool(
            query_engine=engine,
            metadata = ToolMetadata(
                name="Annual Report",
                description=f"Provides information about the company from its annual report.",
                )
        )
        ]

        sub_question_query_engine = SubQuestionQueryEngine.from_defaults(
            query_engine_tools=query_enginer_tools,
            service_context=self.service_context,
            verbose=True,
            use_async=True
        )

        return sub_question_query_engine
    
    def engine(self):
        nodes = self.convert_chunks_to_nodes()
        engine = self.get_vector_index_engine(nodes)
        sub_question_query_engine = self.get_sub_question_query_engine(engine)
        return sub_question_query_engine
    
    

