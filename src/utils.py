from cgitb import text
from pydoc import Doc
from re import split
import sys
from pathlib import Path
script_dir = Path(__file__).resolve().parent
project_root = script_dir.parent
sys.path.append(str(project_root))


from langchain.vectorstores import Weaviate
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.document_loaders import TextLoader, PyPDFLoader
from langchain.schema.document import Document

from dotenv import dotenv_values
import weaviate
from PyPDF2 import PdfReader

config = dotenv_values(".env")

OPENAI_API_KEY = config["OPENAI_API_KEY"]
WEAVIATE_URL = config["WEAVIATE_URL"]
WEAVIATE_API_KEY = config["WEAVIATE_API_KEY"]

def process_pdf(pdfs):
    docs = []
    for pdf in pdfs:
        file = PdfReader(pdf)
        text = ""
        for page in file.pages:
            text += str(page.extract_text())
        
        docs.append(Document(page_content=text))

    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    docs = text_splitter.split_documents(docs)
    return docs


def vector_store(documents):
    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
    client = weaviate.Client(url=WEAVIATE_URL, auth_client_secret=weaviate.AuthApiKey(WEAVIATE_API_KEY))
    vectorstore = Weaviate.from_documents(documents, embeddings, client=client, by_text=False)
    return vectorstore





