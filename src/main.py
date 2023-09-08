import sys
from pathlib import Path
script_dir = Path(__file__).resolve().parent
project_root = script_dir.parent
sys.path.append(str(project_root))


import streamlit as st

from utils import process_pdf, vector_store

st.title("Hello World")

pdfs = st.file_uploader("Upload a file", type=["pdf"], accept_multiple_files=True)
text = process_pdf(pdfs)
# st.write(text)
db = vector_store(text)
query = "what is classification?"
ans = db.similarity_search(query)
st.write(ans)

