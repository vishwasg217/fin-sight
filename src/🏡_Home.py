import sys
from pathlib import Path
script_dir = Path(__file__).resolve().parent
project_root = script_dir.parent
sys.path.append(str(project_root))

import streamlit as st

st.set_page_config(page_title="FinSight", page_icon=":money_with_wings:", layout="wide")

st.title(":money_with_wings: FinSight \n\n **Financial Insights at Your Fingertip**")

st.balloons()
with open("docs/news.md", "r") as f:
    st.success(f.read())

with open("docs/main.md", "r") as f:
    st.info(f.read())

