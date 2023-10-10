import sys
from pathlib import Path
script_dir = Path(__file__).resolve().parent
project_root = script_dir.parent
sys.path.append(str(project_root))

from langchain.llms import Clarifai

import streamlit as st

CLARIFY_AI_PAT = st.secrets["clarify_ai_pat"]
USER_ID = 'openai'
APP_ID = 'chat-completion'
MODEL_ID = 'GPT-4'
MODEL_VERSION_ID = 'ad16eda6ac054796bf9f348ab6733c72'

llm = Clarifai(pat=CLARIFY_AI_PAT, user_id=USER_ID, app_id=APP_ID, model_id=MODEL_ID, model_version_id=MODEL_VERSION_ID)

query = ""

while True:
    query = input("Enter the query: ")
    if query == "exit":
        break
    result = llm.predict(query)
    print(result)
    print("------------------")


st.text_input()