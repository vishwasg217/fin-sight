import sys
from pathlib import Path
script_dir = Path(__file__).resolve().parent
project_root = script_dir.parent
sys.path.append(str(project_root))

from langchain.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser

from src.pydantic_models import ExecutiveOverview
from src.utils import get_model

template = """
You are given the task of generating insights for {section} from the annual report. 

Given below is the output format, which has the subsections.
Make sure each subsection has exactly three points
---
{output_format}
---

"""


def executive_overview(engine, section, pydantic_model):
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
    return parsed_response




