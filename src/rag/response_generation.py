from llama_index.query_engine import SubQuestionQueryEngine
from llama_index.tools import QueryEngineTool, ToolMetadata
from llama_index import ServiceContext

import nest_asyncio
import json

from sqlalchemy import create_engine

nest_asyncio.apply()

from src.utils import get_model

class ResponseGeneration():
    def __init__(self, engine) -> None:
        self.engine = engine
        self.llm = get_model("openai")
        self.service_context = ServiceContext.from_defaults(llm=self.llm)

    def create_engine(self):
        query_engine_tools = [
            QueryEngineTool(
                query_engine=self.engine,
                metadata=ToolMetadata(
                    name="Annual Report",
                    description=f"Provides information about the company from its annual report.",
                )
            )
        ]

        self.sub_question_query_engine = SubQuestionQueryEngine.from_defaults(
            query_engine_tools=query_engine_tools,
            service_context=self.service_context,
            verbose=True,
            use_async=True
        )

    
    def response_gen(self, section):
        with open("prompts/sections.json", "r") as f:
            sections = json.load(f)

        with open("prompts/rag.prompt", "r") as f:
            prompt_template = f.read()

        prompt = prompt_template.format(**sections[section])
        response = self.sub_question_query_engine.query(prompt)
        return response
    
    def node_score(nodes):
        total_score = 0
        node_count = 0
        for node in nodes:
            if node.score is not None:
                total_score += node.score
                node_count += 1

        avg_node_score = total_score/node_count

        return avg_node_score   
    
    def get_response(self, section):
        self.create_engine()
        response = self.response_gen(section)
        node_score = self.node_score(response.source_nodes)
        
        return response.response_txt, node_score






        
    