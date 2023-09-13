from pypdf import PdfReader
import streamlit as st
from llama_index import Document
from llama_index.node_parser import SimpleNodeParser

node_parser = SimpleNodeParser.from_defaults(chunk_size=1024, chunk_overlap=20)

pdfs = st.file_uploader("pdf file")
docs = []
for pdf in [pdfs]:
        file = PdfReader(pdf)
        text = ""
        for page in file.pages:
            text += str(page.extract_text())
        
        docs.append(Document(text=text))

# nodes = node_parser.get_nodes_from_documents(docs, show_progress=False)
# print(nodes)

print(docs)