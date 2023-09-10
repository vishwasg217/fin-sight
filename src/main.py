import sys
from pathlib import Path
script_dir = Path(__file__).resolve().parent
project_root = script_dir.parent
sys.path.append(str(project_root))

from langchain.chains import RetrievalQA
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI


import streamlit as st
from dotenv import dotenv_values

from src.utils import process_pdf, vector_store, chroma_db, faiss_db

config = dotenv_values(".env")

OPENAI_API_KEY = config["OPENAI_API_KEY"]




if __name__ == "__main__":
    if "memory" not in st.session_state:
            st.session_state.memory = None

    if "conversation" not in st.session_state:
            st.session_state.conversation = None

    st.divider()
    
    model = ChatOpenAI(openai_api_key=OPENAI_API_KEY, max_tokens=2000)

    if "process_pdf" not in st.session_state:
        st.session_state.process_pdf = False

    pdfs = st.sidebar.file_uploader("Upload a PDF file", type=["pdf"], accept_multiple_files=True)
    if st.sidebar.button("Process PDF"):
        st.session_state.process_pdf = True
        with st.spinner("Processing PDF..."):
            splitted_text = process_pdf(pdfs)
            db = faiss_db(splitted_text)
            st.session_state.qa = RetrievalQA.from_llm(llm=model, 
                                                    retriever=db.as_retriever(), 
                                                    return_source_documents=False,
                                                    )
        

    if st.session_state.process_pdf:
        query = st.text_input("Ask a question")
        if st.button("Ask"):
            ans = st.session_state.qa.run(query)
            st.write(ans)

