import sys
from pathlib import Path
script_dir = Path(__file__).resolve().parent
project_root = script_dir.parent
sys.path.append(str(project_root))

import streamlit as st
import requests
from datetime import datetime, timedelta
import json


AV_API_KEY = st.secrets["av_api_key"]
symbol = "MSFT"

current_datetime = datetime.now()
one_year_ago = current_datetime - timedelta(days=365)
formatted_time_from = one_year_ago.strftime("%Y%m%dT%H%M")
print("time_from=", formatted_time_from)




url = "https://www.alphavantage.co/query"
params = {
    "function": "NEWS_SENTIMENT",
    "tickers": symbol,
    "apikey": AV_API_KEY,
    "sort": "RELEVANCE",
    "limit": "5"
}

# Send a GET request to the API
response = requests.get(url, params=params)
if response.status_code == 200:
    data = response.json()
    json_object = json.dumps(data)
    with open("sample.json", "w") as f:
        f.write(json_object)
    
else:
    print(f"Error: {response.status_code} - {response.text}")

print(len(data["feed"]))