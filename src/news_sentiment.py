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

def latest_news(symbol, max_feed):

    current_datetime = datetime.now()
    one_year_ago = current_datetime - timedelta(days=365)
    formatted_time_from = one_year_ago.strftime("%Y%m%dT%H%M")
    print("time_from=", formatted_time_from)

    url = "https://www.alphavantage.co/query"
    params = {
        "function": "NEWS_SENTIMENT",
        "tickers": symbol,
        "apikey": AV_API_KEY,
        "sort": "LATEST",
    }

    # Send a GET request to the API
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()

        news = []

        for i in data["feed"][:max_feed]:
            temp = {}
            temp["title"] = i["title"]
            temp["url"] = i["url"]
            temp["authors"] = i["authors"]

            topics = []
            for j in i["topics"]:
                topics.append(j["topic"])
            temp["topics"] = topics

            sentiment_score = ""
            sentiment_label = ""
            for j in i["ticker_sentiment"]:
                if j["ticker"] == symbol:
                    sentiment_score = j["ticker_sentiment_score"]
                    sentiment_label = j["ticker_sentiment_label"]
                    break
            temp["sentiment_score"] = sentiment_score
            temp["sentiment_label"] = sentiment_label
            
            news.append(temp)

        
    else:
        print(f"Error: {response.status_code} - {response.text}")

    return news

if __name__ == "__main__":
    news = latest_news("AAPL")
    for i in news:
        print(i)

