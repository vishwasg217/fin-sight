import streamlit as st

st.set_page_config(page_title="FinSight", page_icon=":money_with_wings:", layout="wide")

st.title(":money_with_wings: FinSight \n\n **Financial Insights at Your Fingertip**")

st.balloons()

st.success("""
If you'd like to learn more about the technical details of FinSight, check out the LlamaIndex blogpost below where I do a deep dive into the project:
           
[How I built the Streamlit LLM Hackathon winning app — FinSight using LlamaIndex.](https://blog.llamaindex.ai/how-i-built-the-streamlit-llm-hackathon-winning-app-finsight-using-llamaindex-9dcf6c46d7a0)
        
""")

with open("docs/news.md", "r") as f:
    st.success(f.read())

with open("docs/main.md", "r") as f:
    st.info(f.read())

