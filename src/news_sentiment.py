import sys
from pathlib import Path
script_dir = Path(__file__).resolve().parent
project_root = script_dir.parent
sys.path.append(str(project_root))

import streamlit as st
import requests
from datetime import datetime, timedelta
import pandas as pd
import os

# AV_API_KEY = st.secrets["av_api_key"]

AV_API_KEY = os.environ.get("AV_API_KEY")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

def classify_sentiment(mean_score):
    if mean_score <= -0.35:
        return "Bearish"
    elif -0.35 < mean_score <= -0.15:
        return "Somewhat-Bearish"
    elif -0.15 < mean_score < 0.15:
        return "Neutral"
    elif 0.15 <= mean_score < 0.35:
        return "Somewhat_Bullish"
    elif mean_score >= 0.35:
        return "Bullish"
    else:
        return "Undefined"

def top_news(symbol, max_feed):

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
    }

    # Send a GET request to the API
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        if not data:
            print(f"No data found for {symbol}")
            print(data)
            return None
        news = []

        if "Error Message" in data:
            return {"Error": data["Error Message"]}

        try:
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

        except Exception as e:
            print(e)
            return None
        
    else:
        print(f"Error: {response.status_code} - {response.text}")

    news = pd.DataFrame(news)
    news["sentiment_score"] = pd.to_numeric(news["sentiment_score"])
    mean_sentiment_score  = news["sentiment_score"].mean()
    mean_sentiment_class = classify_sentiment(mean_sentiment_score)

    return {
        "news": news,
        "mean_sentiment_score": mean_sentiment_score,
        "mean_sentiment_class": mean_sentiment_class
    }

if __name__ == "__main__":
    news = top_news("AAPL", 10)
    print(news)

