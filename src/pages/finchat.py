import sys
from pathlib import Path
script_dir = Path(__file__).resolve().parent
project_root = script_dir.parent
sys.path.append(str(project_root))


from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferWindowMemory
from langchain.chains import ConversationalRetrievalChain

import streamlit as st
from dotenv import dotenv_values

from src.utils import process_pdf, vector_store

# config = dotenv_values(".env")

# OPENAI_API_KEY = config["OPENAI_API_KEY"]

OPENAI_API_KEY = st.secrets["openai_api_key"]


def handle_query(query: str):
    result = st.session_state.conversation({"question": query, "chat_history": ""})
    history = st.session_state.memory.load_memory_variables({})['chat_history']
    print(st.session_state.memory.load_memory_variables({})['chat_history'])
    for i, msg in enumerate(history):
        if i%2 == 0:
            st.write("hello")
            st.chat_message("user").write(msg.content)
        else:
            st.chat_message("assistant").write(msg.content)


if __name__ == "__main__":

    if "memory" not in st.session_state:
            st.session_state.memory = None

    if "conversation" not in st.session_state:
            st.session_state.conversation = None

    st.divider()
    
    model = ChatOpenAI(openai_api_key=OPENAI_API_KEY, model_name="gpt-3.5-turbo")

    if "process_pdf" not in st.session_state:
        st.session_state.process_pdf = False

    pdfs = st.sidebar.file_uploader("Upload a PDF file", type=["pdf"], accept_multiple_files=True)
    if st.sidebar.button("Process PDF"):
        st.session_state.process_pdf = True
        with st.spinner("Processing PDF..."):
            splitted_text = process_pdf(pdfs)
            db = vector_store(splitted_text)
        st.session_state.memory = ConversationBufferWindowMemory(memory_key='chat_history', return_messages=True, k=5)
        st.session_state.conversation = ConversationalRetrievalChain.from_llm(llm=model,
                                                                            chain_type="map_reduce", 
                                                                            retriever=db.as_retriever(), 
                                                                            memory=st.session_state.memory)

    if st.session_state.process_pdf:
        query = st.chat_input("Ask a question")
        if query:
            handle_query(query)