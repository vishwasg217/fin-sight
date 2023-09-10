import sys
from pathlib import Path
script_dir = Path(__file__).resolve().parent
project_root = script_dir.parent
sys.path.append(str(project_root))


import streamlit as st
from dotenv import dotenv_values

from src.utils import process_pdf, vector_store

config = dotenv_values(".env")
OPENAI_API_KEY = config["OPENAI_API_KEY"]

def summarize(query):
    pass
