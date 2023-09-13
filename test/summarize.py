import sys
from pathlib import Path
script_dir = Path(__file__).resolve().parent
project_root = script_dir.parent
sys.path.append(str(project_root))

from langchain.chains.question_answering import load_qa_chain
from langchain.document_loaders import PyPDFLoader
from langchain.llms import OpenAI


from dotenv import dotenv_values

config = dotenv_values(".env")
OPENAI_API_KEY = config["OPENAI_API_KEY"]

# load document
loader = PyPDFLoader("AAPL.pdf")
documents = loader.load()

llm = OpenAI(openai_api_key=OPENAI_API_KEY)

### For multiple documents 
# loaders = [....]
# documents = []
# for loader in loaders:
#     documents.extend(loader.load())

chain = load_qa_chain(llm=llm, chain_type="map_reduce")
query = "what is the total number of AI publications?"
print(chain.run(input_documents=documents, question=query))

