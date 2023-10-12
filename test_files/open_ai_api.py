import sys
from pathlib import Path
from typing import Literal

script_dir = Path(__file__).resolve().parent
project_root = script_dir.parent
sys.path.append(str(project_root))

import os
import openai
import streamlit as st
from pydantic import BaseModel, Field

OPENAI_API_KEY = st.secrets["openai_api_key"]


# # Load your API key from an environment variable or secret management service
openai.api_key = os.getenv("OPENAI_API_KEY")

# chat_completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": "who is lionel messi?"}])
# print(chat_completion)

# from llama_index.llms import OpenAI
from langchain.chat_models import ChatOpenAI

llm = ChatOpenAI(openai_api_key=OPENAI_API_KEY, model_name="gpt-4")

response = llm.predict("who is virat kohli?")
print(type(response))
print(response)