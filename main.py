import streamlit as st

apikey = st.secrets["openai_api_key"]
st.write(apikey)